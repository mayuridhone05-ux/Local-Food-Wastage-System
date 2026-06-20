# ============================================================
# LOCAL FOOD WASTAGE MANAGEMENT SYSTEM
# FILE 3: Streamlit Dashboard
# ============================================================
# HOW TO RUN: Open terminal in VS Code and type:
#   streamlit run app.py
# ============================================================

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ── Page configuration (must be the FIRST streamlit command) ─
st.set_page_config(
    page_title="Food Wastage Management System",
    page_icon="🥗",
    layout="wide"
)

# ── Load Data ────────────────────────────────────────────────
@st.cache_data   # this caches data so app doesn't reload it every second
def load_data():
    providers = pd.read_csv("data/providers_data.csv")
    receivers = pd.read_csv("data/receivers_data.csv")
    food      = pd.read_csv("data/food_listings_data.csv")
    claims    = pd.read_csv("data/claims_data.csv")
    return providers, receivers, food, claims

providers, receivers, food, claims = load_data()

# ── Build SQL database ───────────────────────────────────────
@st.cache_resource
def get_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    providers.to_sql("providers",  conn, index=False, if_exists="replace")
    receivers.to_sql("receivers",  conn, index=False, if_exists="replace")
    food.to_sql("food_listings",   conn, index=False, if_exists="replace")
    claims.to_sql("claims",        conn, index=False, if_exists="replace")
    return conn

conn = get_db()

# ============================================================
# SIDEBAR — FILTERS
# ============================================================
st.sidebar.title("🔍 Filters")
st.sidebar.markdown("Use these filters to explore the data")

# City filter — uses food Location column
all_locations = sorted(food["Location"].unique())
selected_location = st.sidebar.selectbox(
    "📍 Select Location",
    options=["All"] + all_locations
)

# Provider Type filter
all_provider_types = sorted(food["Provider_Type"].unique())
selected_provider_type = st.sidebar.selectbox(
    "🏪 Select Provider Type",
    options=["All"] + all_provider_types
)

# Meal Type filter
all_meal_types = sorted(food["Meal_Type"].unique())
selected_meal_type = st.sidebar.selectbox(
    "🍽️ Select Meal Type",
    options=["All"] + all_meal_types
)

# Food Type filter
all_food_types = sorted(food["Food_Type"].unique())
selected_food_type = st.sidebar.selectbox(
    "🥗 Select Food Type",
    options=["All"] + all_food_types
)

# ── Apply filters to food dataframe ─────────────────────────
filtered_food = food.copy()
if selected_location != "All":
    filtered_food = filtered_food[filtered_food["Location"] == selected_location]
if selected_provider_type != "All":
    filtered_food = filtered_food[filtered_food["Provider_Type"] == selected_provider_type]
if selected_meal_type != "All":
    filtered_food = filtered_food[filtered_food["Meal_Type"] == selected_meal_type]
if selected_food_type != "All":
    filtered_food = filtered_food[filtered_food["Food_Type"] == selected_food_type]

# ============================================================
# MAIN TITLE
# ============================================================
st.title("🥗 Local Food Wastage Management System")
st.markdown("A centralized platform connecting **food providers** with **receivers** to reduce food wastage.")
st.markdown("---")

# ============================================================
# SECTION 1: KEY METRICS (top summary boxes)
# ============================================================
st.subheader("📊 Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Providers", len(providers))
with col2:
    st.metric("Total Receivers", len(receivers))
with col3:
    st.metric("Food Listings", len(filtered_food))
with col4:
    st.metric("Total Quantity", f"{filtered_food['Quantity'].sum():,}")
with col5:
    completed = claims[claims["Status"] == "Completed"].shape[0]
    st.metric("Completed Claims", f"{completed} ({completed/len(claims)*100:.0f}%)")

st.markdown("---")

# ============================================================
# SECTION 2: CHARTS — displayed in 2 columns side by side
# ============================================================
st.subheader("📈 Visual Analysis")

COLORS = ["#2ecc71", "#3498db", "#e74c3c", "#f39c12", "#9b59b6", "#1abc9c"]
sns.set_theme(style="whitegrid")

# Row 1
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Provider Type Distribution**")
    ptype = providers["Type"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(ptype.index, ptype.values, color=COLORS)
    ax.set_xlabel("Provider Type")
    ax.set_ylabel("Count")
    plt.xticks(rotation=15, fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_b:
    st.markdown("**Claim Status Distribution**")
    status = claims["Status"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.pie(status.values, labels=status.index, autopct="%1.1f%%",
           colors=["#2ecc71", "#e74c3c", "#f39c12"], startangle=90)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Row 2
col_c, col_d = st.columns(2)

with col_c:
    st.markdown("**Food Type vs Total Quantity**")
    ftype_qty = filtered_food.groupby("Food_Type")["Quantity"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(ftype_qty.index, ftype_qty.values, color=COLORS[:3])
    ax.set_xlabel("Food Type")
    ax.set_ylabel("Total Quantity")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_d:
    st.markdown("**Meal Type vs Total Quantity**")
    meal_qty = filtered_food.groupby("Meal_Type")["Quantity"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(meal_qty.index, meal_qty.values, color=COLORS)
    ax.set_xlabel("Meal Type")
    ax.set_ylabel("Total Quantity")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Row 3 — Heatmap
st.markdown("**Food Type + Meal Type → Quantity Heatmap**")
if len(filtered_food) > 0:
    pivot = filtered_food.pivot_table(
        index="Food_Type", columns="Meal_Type",
        values="Quantity", aggfunc="sum"
    )
    fig, ax = plt.subplots(figsize=(10, 3))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGn", ax=ax, linewidths=0.5)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
else:
    st.info("No data available for selected filters.")

st.markdown("---")

# ============================================================
# SECTION 3: PROVIDER CONTACT INFORMATION
# ============================================================
st.subheader("📞 Provider Contact Information")

# Merge food with provider info
food_with_prov = filtered_food.merge(
    providers[["Provider_ID", "Name", "City", "Contact"]],
    on="Provider_ID", how="left"
)

# Group to show one row per provider
provider_info = (
    food_with_prov.groupby(["Name", "City", "Contact"])
    .agg(Total_Quantity=("Quantity", "sum"), Food_Items=("Food_ID", "count"))
    .reset_index()
    .sort_values("Total_Quantity", ascending=False)
)

st.dataframe(
    provider_info.head(20),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ============================================================
# SECTION 4: SQL QUERY EXPLORER
# ============================================================
st.subheader("🗄️ SQL Query Explorer")
st.markdown("Select a question below to run a live SQL query on the database.")

query_options = {
    "Top 10 Providers by Total Quantity Donated": """
        SELECT p.Name AS Provider, p.Type, SUM(f.Quantity) AS Total_Quantity
        FROM food_listings f JOIN providers p ON f.Provider_ID = p.Provider_ID
        GROUP BY p.Name, p.Type ORDER BY Total_Quantity DESC LIMIT 10
    """,
    "Top 10 Receivers by Number of Claims": """
        SELECT r.Name AS Receiver, r.Type, COUNT(c.Claim_ID) AS Total_Claims
        FROM claims c JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY r.Name ORDER BY Total_Claims DESC LIMIT 10
    """,
    "Claim Status Breakdown with Percentage": """
        SELECT Status, COUNT(*) AS Count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage
        FROM claims GROUP BY Status ORDER BY Count DESC
    """,
    "Most Claimed Food Items": """
        SELECT f.Food_Name, COUNT(c.Claim_ID) AS Claims
        FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Food_Name ORDER BY Claims DESC
    """,
    "Provider Type vs Total Quantity": """
        SELECT Provider_Type, SUM(Quantity) AS Total_Quantity, COUNT(*) AS Listings
        FROM food_listings GROUP BY Provider_Type ORDER BY Total_Quantity DESC
    """,
    "Meal Type with Most Pending Claims (Wastage Risk)": """
        SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Pending_Claims
        FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID
        WHERE c.Status = 'Pending'
        GROUP BY f.Meal_Type ORDER BY Pending_Claims DESC
    """,
    "Receiver Type by Total Claims": """
        SELECT r.Type AS Receiver_Type, COUNT(c.Claim_ID) AS Total_Claims
        FROM claims c JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY r.Type ORDER BY Total_Claims DESC
    """,
    "Food Type + Meal Type Combination Summary": """
        SELECT Food_Type, Meal_Type, COUNT(*) AS Count, SUM(Quantity) AS Total_Quantity
        FROM food_listings GROUP BY Food_Type, Meal_Type ORDER BY Total_Quantity DESC
    """
}

selected_query = st.selectbox("Choose a query:", list(query_options.keys()))

if st.button("▶ Run Query"):
    result_df = pd.read_sql_query(query_options[selected_query], conn)
    st.dataframe(result_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================
# SECTION 5: RAW DATA VIEWER
# ============================================================
st.subheader("📋 View Raw Data")

tab1, tab2, tab3, tab4 = st.tabs(["Providers", "Receivers", "Food Listings", "Claims"])
with tab1:
    st.dataframe(providers, use_container_width=True, hide_index=True)
with tab2:
    st.dataframe(receivers, use_container_width=True, hide_index=True)
with tab3:
    st.dataframe(filtered_food, use_container_width=True, hide_index=True)
with tab4:
    st.dataframe(claims, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================
# SECTION 6: BUSINESS INSIGHTS & RECOMMENDATIONS
# ============================================================
st.subheader("💡 Business Insights & Recommendations")

col_i1, col_i2 = st.columns(2)

with col_i1:
    st.markdown("### 📌 Key Insights")
    st.markdown(f"""
- 🏆 **Top Provider Type:** Restaurants donate the most food (**6,923 units**)
- 🥗 **Most Listed Food Type:** Vegetarian items lead with **336 listings**
- 🍳 **Most Listed Meal Type:** Breakfast has the highest listings (**254**)
- 🤝 **Top Receiver Type:** NGOs claim the most food (**272 claims**)
- ✅ **Completed Claims:** Only **33.9%** of claims are completed — room for improvement
- ⚠️ **Pending Claims:** **32.5%** of claims are still pending — a wastage risk
- 🍚 **Most Claimed Food:** Rice is the most claimed item (**122 claims**)
- 🍽️ **Wastage Risk Meal:** Lunch has the most pending claims (**89 pending**)
    """)

with col_i2:
    st.markdown("### 🚀 Recommendations")
    st.markdown("""
1. **Partner more NGOs in high-food locations** — many listings go unclaimed
2. **Automate expiry alerts** — notify receivers before food expires
3. **Recognize top providers** — Barry Group & Miller Inc contribute the most
4. **Reduce Lunch wastage** — Lunch has highest pending claims; prioritize its distribution
5. **Increase NGO capacity** — NGOs claim the most; expanding their reach will reduce wastage
6. **Follow up on Cancelled claims** — 33.6% cancellations indicate coordination gaps
    """)

st.markdown("---")
st.markdown("🌱 *Built with Python · SQL · Streamlit | Local Food Wastage Management System*")
