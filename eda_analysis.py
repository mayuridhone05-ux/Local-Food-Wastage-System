# ============================================================
# LOCAL FOOD WASTAGE MANAGEMENT SYSTEM
# FILE 1: EDA Analysis & Charts
# ============================================================
# HOW TO RUN: Open terminal in VS Code and type:
#   python eda_analysis.py
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ── Make a folder to save all charts ────────────────────────
os.makedirs("charts", exist_ok=True)

# ── Load all 4 datasets ─────────────────────────────────────
# pd.read_csv() reads a CSV file and turns it into a table (called DataFrame)
providers = pd.read_csv("data/providers_data.csv")
receivers = pd.read_csv("data/receivers_data.csv")
food      = pd.read_csv("data/food_listings_data.csv")
claims    = pd.read_csv("data/claims_data.csv")

print("✅ All datasets loaded successfully!")
print(f"   Providers : {len(providers)} rows")
print(f"   Receivers : {len(receivers)} rows")
print(f"   Food Items: {len(food)} rows")
print(f"   Claims    : {len(claims)} rows")

# Set a clean visual style for all charts
sns.set_theme(style="whitegrid")
COLORS = ["#2ecc71", "#3498db", "#e74c3c", "#f39c12", "#9b59b6", "#1abc9c"]


# ============================================================
# SECTION 1: UNIVARIATE ANALYSIS
# (Looking at ONE column at a time)
# ============================================================
print("\n📊 Drawing Univariate Charts...")

# ── Chart 1: Provider Type Distribution ─────────────────────
# value_counts() counts how many times each value appears
provider_counts = providers["Type"].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(provider_counts.index, provider_counts.values, color=COLORS)
plt.title("Provider Type Distribution", fontsize=15, fontweight="bold")
plt.xlabel("Provider Type")
plt.ylabel("Number of Providers")
for i, v in enumerate(provider_counts.values):
    plt.text(i, v + 2, str(v), ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("charts/01_provider_type_distribution.png", dpi=150)
plt.close()
print("   ✅ Chart 1: Provider Type Distribution saved")

# ── Chart 2: Receiver Type Distribution ─────────────────────
receiver_counts = receivers["Type"].value_counts()

plt.figure(figsize=(8, 5))
plt.pie(
    receiver_counts.values,
    labels=receiver_counts.index,
    autopct="%1.1f%%",       # shows percentage on each slice
    colors=COLORS,
    startangle=140
)
plt.title("Receiver Type Distribution", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/02_receiver_type_distribution.png", dpi=150)
plt.close()
print("   ✅ Chart 2: Receiver Type Distribution saved")

# ── Chart 3: Food Type Distribution ─────────────────────────
food_type_counts = food["Food_Type"].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(food_type_counts.index, food_type_counts.values, color=COLORS[:3])
plt.title("Food Type Distribution", fontsize=15, fontweight="bold")
plt.xlabel("Food Type")
plt.ylabel("Count")
for i, v in enumerate(food_type_counts.values):
    plt.text(i, v + 2, str(v), ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("charts/03_food_type_distribution.png", dpi=150)
plt.close()
print("   ✅ Chart 3: Food Type Distribution saved")

# ── Chart 4: Meal Type Distribution ─────────────────────────
meal_counts = food["Meal_Type"].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(meal_counts.index, meal_counts.values, color=COLORS)
plt.title("Meal Type Distribution", fontsize=15, fontweight="bold")
plt.xlabel("Meal Type")
plt.ylabel("Count")
for i, v in enumerate(meal_counts.values):
    plt.text(i, v + 2, str(v), ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("charts/04_meal_type_distribution.png", dpi=150)
plt.close()
print("   ✅ Chart 4: Meal Type Distribution saved")


# ============================================================
# SECTION 2: BIVARIATE ANALYSIS
# (Looking at TWO columns together)
# ============================================================
print("\n📊 Drawing Bivariate Charts...")

# ── Chart 5: Top 10 Locations by Food Listings ──────────────
# groupby() groups data by a column, then count() counts entries per group
top_locations = (
    food.groupby("Location")["Food_ID"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
plt.barh(top_locations.index, top_locations.values, color=COLORS[1])
plt.title("Top 10 Locations by Food Listings", fontsize=15, fontweight="bold")
plt.xlabel("Number of Food Listings")
plt.gca().invert_yaxis()   # puts the highest bar at the top
plt.tight_layout()
plt.savefig("charts/05_top_locations_food_listings.png", dpi=150)
plt.close()
print("   ✅ Chart 5: Top Locations by Food Listings saved")

# ── Chart 6: Provider Type vs Total Quantity ─────────────────
# sum() adds up all values in the group
ptype_qty = food.groupby("Provider_Type")["Quantity"].sum().sort_values(ascending=False)

plt.figure(figsize=(9, 5))
plt.bar(ptype_qty.index, ptype_qty.values, color=COLORS)
plt.title("Provider Type vs Total Quantity Donated", fontsize=15, fontweight="bold")
plt.xlabel("Provider Type")
plt.ylabel("Total Quantity")
for i, v in enumerate(ptype_qty.values):
    plt.text(i, v + 20, str(v), ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("charts/06_provider_type_vs_quantity.png", dpi=150)
plt.close()
print("   ✅ Chart 6: Provider Type vs Quantity saved")

# ── Chart 7: Food Type vs Total Quantity ─────────────────────
ftype_qty = food.groupby("Food_Type")["Quantity"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
plt.bar(ftype_qty.index, ftype_qty.values, color=COLORS[:3])
plt.title("Food Type vs Total Quantity", fontsize=15, fontweight="bold")
plt.xlabel("Food Type")
plt.ylabel("Total Quantity")
for i, v in enumerate(ftype_qty.values):
    plt.text(i, v + 20, str(v), ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("charts/07_food_type_vs_quantity.png", dpi=150)
plt.close()
print("   ✅ Chart 7: Food Type vs Quantity saved")

# ── Chart 8: Meal Type vs Total Quantity ─────────────────────
meal_qty = food.groupby("Meal_Type")["Quantity"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
plt.bar(meal_qty.index, meal_qty.values, color=COLORS)
plt.title("Meal Type vs Total Quantity", fontsize=15, fontweight="bold")
plt.xlabel("Meal Type")
plt.ylabel("Total Quantity")
for i, v in enumerate(meal_qty.values):
    plt.text(i, v + 20, str(v), ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("charts/08_meal_type_vs_quantity.png", dpi=150)
plt.close()
print("   ✅ Chart 8: Meal Type vs Quantity saved")


# ============================================================
# SECTION 3: MULTIVARIATE ANALYSIS
# (Looking at THREE or more things together)
# ============================================================
print("\n📊 Drawing Multivariate Charts...")

# ── Chart 9: Food Type + Meal Type + Quantity (Heatmap) ─────
# pivot_table() reshapes data: rows=Food_Type, cols=Meal_Type, values=Quantity
pivot = food.pivot_table(
    index="Food_Type",
    columns="Meal_Type",
    values="Quantity",
    aggfunc="sum"           # adds up quantity for each combination
)

plt.figure(figsize=(10, 5))
sns.heatmap(
    pivot,
    annot=True,             # writes numbers inside boxes
    fmt=".0f",              # no decimal places
    cmap="YlGn",            # colour from yellow to green
    linewidths=0.5
)
plt.title("Food Type + Meal Type → Total Quantity (Heatmap)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/09_foodtype_mealtype_heatmap.png", dpi=150)
plt.close()
print("   ✅ Chart 9: Food Type + Meal Type Heatmap saved")

# ── Chart 10: Provider Type + Food Type + Quantity (Grouped Bar) ─
pivot2 = food.pivot_table(
    index="Provider_Type",
    columns="Food_Type",
    values="Quantity",
    aggfunc="sum"
)

pivot2.plot(kind="bar", figsize=(10, 6), color=COLORS[:3])
plt.title("Provider Type + Food Type → Total Quantity", fontsize=14, fontweight="bold")
plt.xlabel("Provider Type")
plt.ylabel("Total Quantity")
plt.xticks(rotation=20)
plt.legend(title="Food Type")
plt.tight_layout()
plt.savefig("charts/10_provider_foodtype_quantity.png", dpi=150)
plt.close()
print("   ✅ Chart 10: Provider + Food Type + Quantity saved")

# ── Chart 11: Top 10 Providers by Quantity ───────────────────
# merge() joins two tables together, like VLOOKUP in Excel
food_with_providers = food.merge(providers[["Provider_ID", "Name"]], on="Provider_ID", how="left")
top_providers = (
    food_with_providers.groupby("Name")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
plt.barh(top_providers.index, top_providers.values, color=COLORS[0])
plt.title("Top 10 Providers by Total Quantity Donated", fontsize=14, fontweight="bold")
plt.xlabel("Total Quantity")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("charts/11_top10_providers_quantity.png", dpi=150)
plt.close()
print("   ✅ Chart 11: Top 10 Providers saved")


# ============================================================
# SECTION 4: CLAIMS ANALYSIS
# ============================================================
print("\n📊 Drawing Claims Charts...")

# ── Chart 12: Claim Status Distribution ─────────────────────
status_counts = claims["Status"].value_counts()

plt.figure(figsize=(7, 5))
plt.pie(
    status_counts.values,
    labels=status_counts.index,
    autopct="%1.1f%%",
    colors=["#2ecc71", "#e74c3c", "#f39c12"],
    startangle=90,
    explode=[0.05, 0.05, 0.05]   # slightly separate each slice
)
plt.title("Claim Status Distribution", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/12_claim_status_distribution.png", dpi=150)
plt.close()
print("   ✅ Chart 12: Claim Status Distribution saved")

# ── Chart 13: Top 10 Receivers by Claims ────────────────────
claims_with_receivers = claims.merge(receivers[["Receiver_ID", "Name"]], on="Receiver_ID", how="left")
top_receivers = (
    claims_with_receivers.groupby("Name")["Claim_ID"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
plt.barh(top_receivers.index, top_receivers.values, color=COLORS[3])
plt.title("Top 10 Receivers by Number of Claims", fontsize=14, fontweight="bold")
plt.xlabel("Number of Claims")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("charts/13_top10_receivers.png", dpi=150)
plt.close()
print("   ✅ Chart 13: Top 10 Receivers saved")

# ── Chart 14: Claims per Provider (via food link) ───────────
claims_food = claims.merge(food[["Food_ID", "Provider_ID"]], on="Food_ID", how="left")
claims_food_prov = claims_food.merge(providers[["Provider_ID", "Name"]], on="Provider_ID", how="left")
top_claimed_providers = (
    claims_food_prov.groupby("Name")["Claim_ID"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
plt.barh(top_claimed_providers.index, top_claimed_providers.values, color=COLORS[4])
plt.title("Top 10 Providers by Number of Claims Received", fontsize=14, fontweight="bold")
plt.xlabel("Number of Claims")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("charts/14_top10_claimed_providers.png", dpi=150)
plt.close()
print("   ✅ Chart 14: Top Claimed Providers saved")

print("\n" + "="*55)
print("🎉 ALL CHARTS SAVED to the 'charts/' folder!")
print("="*55)
print("\n📌 BUSINESS INSIGHTS FROM YOUR DATA:")
print(f"   Total food quantity available : {food['Quantity'].sum():,} units")
print(f"   Average quantity per listing  : {food['Quantity'].mean():.1f} units")
print(f"   Most common food item         : {food['Food_Name'].value_counts().index[0]}")
print(f"   Most donated provider type    : {ptype_qty.index[0]} ({ptype_qty.values[0]:,} units)")
print(f"   Most listed food type         : {ftype_qty.index[0]}")
print(f"   Completed claims              : {status_counts.get('Completed', 0)} ({status_counts.get('Completed', 0)/len(claims)*100:.1f}%)")
print(f"   Pending claims                : {status_counts.get('Pending', 0)} ({status_counts.get('Pending', 0)/len(claims)*100:.1f}%)")
print(f"   Cancelled claims              : {status_counts.get('Cancelled', 0)} ({status_counts.get('Cancelled', 0)/len(claims)*100:.1f}%)")
