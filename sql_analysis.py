# ============================================================
# LOCAL FOOD WASTAGE MANAGEMENT SYSTEM
# FILE 2: SQL Analysis (15+ Queries)
# ============================================================
# HOW TO RUN: Open terminal in VS Code and type:
#   python sql_analysis.py
# ============================================================

import pandas as pd
import sqlite3     # sqlite3 is built into Python — no install needed!

# ── Step 1: Load CSVs ───────────────────────────────────────
providers = pd.read_csv("data/providers_data.csv")
receivers = pd.read_csv("data/receivers_data.csv")
food      = pd.read_csv("data/food_listings_data.csv")
claims    = pd.read_csv("data/claims_data.csv")

# ── Step 2: Create a database in memory ─────────────────────
# connect() creates a database. ":memory:" means it lives in RAM, not a file.
conn = sqlite3.connect(":memory:")

# to_sql() pushes each DataFrame into the database as a table
providers.to_sql("providers",  conn, index=False, if_exists="replace")
receivers.to_sql("receivers",  conn, index=False, if_exists="replace")
food.to_sql("food_listings",   conn, index=False, if_exists="replace")
claims.to_sql("claims",        conn, index=False, if_exists="replace")

print("✅ Database created with 4 tables!")
print("="*60)

# ── Helper function to run and print any SQL query ──────────
def run_query(title, query, top_n=None):
    """
    Runs a SQL query and prints the result neatly.
    title  = label to display
    query  = the SQL string
    top_n  = how many rows to show (None = all)
    """
    print(f"\n{'─'*60}")
    print(f"📌 {title}")
    print(f"{'─'*60}")
    result = pd.read_sql_query(query, conn)
    if top_n:
        print(result.head(top_n).to_string(index=False))
    else:
        print(result.to_string(index=False))
    return result


# ============================================================
# QUERY 1: Total number of providers
# ============================================================
run_query(
    "Q1: Total Number of Providers",
    "SELECT COUNT(*) AS Total_Providers FROM providers"
)

# ============================================================
# QUERY 2: Providers grouped by type
# ============================================================
run_query(
    "Q2: Number of Providers by Type",
    """
    SELECT Type, COUNT(*) AS Count
    FROM providers
    GROUP BY Type
    ORDER BY Count DESC
    """
)

# ============================================================
# QUERY 3: Receivers grouped by type
# ============================================================
run_query(
    "Q3: Number of Receivers by Type",
    """
    SELECT Type, COUNT(*) AS Count
    FROM receivers
    GROUP BY Type
    ORDER BY Count DESC
    """
)

# ============================================================
# QUERY 4: Top 10 locations by number of food listings
# ============================================================
run_query(
    "Q4: Top 10 Locations by Food Listings",
    """
    SELECT Location, COUNT(*) AS Food_Listings
    FROM food_listings
    GROUP BY Location
    ORDER BY Food_Listings DESC
    LIMIT 10
    """
)

# ============================================================
# QUERY 5: Total food quantity donated by each provider type
# ============================================================
run_query(
    "Q5: Total Quantity Donated by Provider Type",
    """
    SELECT Provider_Type, SUM(Quantity) AS Total_Quantity
    FROM food_listings
    GROUP BY Provider_Type
    ORDER BY Total_Quantity DESC
    """
)

# ============================================================
# QUERY 6: Most common food type listed
# ============================================================
run_query(
    "Q6: Most Common Food Type",
    """
    SELECT Food_Type, COUNT(*) AS Count
    FROM food_listings
    GROUP BY Food_Type
    ORDER BY Count DESC
    """
)

# ============================================================
# QUERY 7: Most common meal type listed
# ============================================================
run_query(
    "Q7: Most Common Meal Type",
    """
    SELECT Meal_Type, COUNT(*) AS Count
    FROM food_listings
    GROUP BY Meal_Type
    ORDER BY Count DESC
    """
)

# ============================================================
# QUERY 8: Claim status breakdown with percentage
# ============================================================
run_query(
    "Q8: Claim Status Breakdown with Percentage",
    """
    SELECT
        Status,
        COUNT(*) AS Count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage
    FROM claims
    GROUP BY Status
    ORDER BY Count DESC
    """
)

# ============================================================
# QUERY 9: Top 10 providers by total quantity donated
# (joins food_listings with providers)
# ============================================================
run_query(
    "Q9: Top 10 Providers by Total Quantity Donated",
    """
    SELECT p.Name AS Provider_Name, p.Type, SUM(f.Quantity) AS Total_Quantity
    FROM food_listings f
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    GROUP BY p.Name, p.Type
    ORDER BY Total_Quantity DESC
    LIMIT 10
    """
)

# ============================================================
# QUERY 10: Top 10 receivers by number of claims made
# ============================================================
run_query(
    "Q10: Top 10 Receivers by Number of Claims",
    """
    SELECT r.Name AS Receiver_Name, r.Type, COUNT(c.Claim_ID) AS Total_Claims
    FROM claims c
    JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
    GROUP BY r.Name, r.Type
    ORDER BY Total_Claims DESC
    LIMIT 10
    """
)

# ============================================================
# QUERY 11: Provider with most COMPLETED claims
# ============================================================
run_query(
    "Q11: Top 10 Providers with Most Completed Claims",
    """
    SELECT p.Name AS Provider_Name, COUNT(c.Claim_ID) AS Completed_Claims
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    WHERE c.Status = 'Completed'
    GROUP BY p.Name
    ORDER BY Completed_Claims DESC
    LIMIT 10
    """
)

# ============================================================
# QUERY 12: Average quantity per food item
# ============================================================
run_query(
    "Q12: Average Quantity per Food Item (Food Name)",
    """
    SELECT Food_Name, ROUND(AVG(Quantity), 2) AS Avg_Quantity, SUM(Quantity) AS Total_Quantity
    FROM food_listings
    GROUP BY Food_Name
    ORDER BY Total_Quantity DESC
    """
)

# ============================================================
# QUERY 13: Number of claims per food listing
# ============================================================
run_query(
    "Q13: Top 10 Most Claimed Food Items",
    """
    SELECT f.Food_Name, COUNT(c.Claim_ID) AS Number_of_Claims
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY f.Food_Name
    ORDER BY Number_of_Claims DESC
    LIMIT 10
    """
)

# ============================================================
# QUERY 14: Total quantity donated by each individual provider
# ============================================================
run_query(
    "Q14: Total Donated Quantity per Provider (Top 10)",
    """
    SELECT p.Name, SUM(f.Quantity) AS Total_Donated
    FROM food_listings f
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    GROUP BY p.Name
    ORDER BY Total_Donated DESC
    LIMIT 10
    """
)

# ============================================================
# QUERY 15: Food type + Meal type combination counts
# ============================================================
run_query(
    "Q15: Food Type + Meal Type Combinations",
    """
    SELECT Food_Type, Meal_Type, COUNT(*) AS Count, SUM(Quantity) AS Total_Quantity
    FROM food_listings
    GROUP BY Food_Type, Meal_Type
    ORDER BY Total_Quantity DESC
    """
)

# ============================================================
# QUERY 16: Meal type with highest wastage risk (most pending claims)
# ============================================================
run_query(
    "Q16: Meal Type with Most Pending Claims (Wastage Risk)",
    """
    SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Pending_Claims
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    WHERE c.Status = 'Pending'
    GROUP BY f.Meal_Type
    ORDER BY Pending_Claims DESC
    """
)

# ============================================================
# QUERY 17: Which receiver type claims the most food
# ============================================================
run_query(
    "Q17: Receiver Type by Total Claims",
    """
    SELECT r.Type AS Receiver_Type, COUNT(c.Claim_ID) AS Total_Claims
    FROM claims c
    JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
    GROUP BY r.Type
    ORDER BY Total_Claims DESC
    """
)

print("\n" + "="*60)
print("🎉 ALL 17 SQL QUERIES COMPLETED SUCCESSFULLY!")
print("="*60)

conn.close()
