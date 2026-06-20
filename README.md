#🥗 Local Food Wastage Management System

A centralized, interactive platform built with Python and Streamlit to connect food providers with receivers, aimed at reducing food wastage and combating food insecurity through data-driven distribution.

🔴 👉 CLICK HERE TO VIEW THE LIVE STREAMLIT APP 👈 (Link to be added after deployment)

📌 Problem Statement

Food wastage is a critical global issue. While restaurants and households discard surplus food, numerous communities struggle with food insecurity. This project addresses this gap by developing a localized management system that tracks surplus food listings, maps provider locations, and monitors distribution claims.

🚀 Key Features & Deliverables

1. Interactive Streamlit Web Application

Dynamic Filtering: Users can filter food availability by City, Provider Type, Meal Type, and Food Category.

KPI Scorecards: Real-time metrics tracking total providers, active food listings, and claim completion percentages.

Provider Contact Integration: Generates accessible contact tables to facilitate direct coordination between NGOs and food providers.

2. In-Memory SQL Analytics

Built a transient SQLite3 database to process and analyze 4 distinct datasets (providers, receivers, food_listings, claims).

Executed 17 complex analytical queries to identify trends, such as:

Which provider types contribute the highest volume of food?

Which meal types carry the highest "wastage risk" (most pending claims)?

What is the completion vs. cancellation rate of food claims?

3. Exploratory Data Analysis (EDA)

Generated automated visualizations using matplotlib and seaborn.

Analyzed provider distributions, top receiver claims, and generated heatmaps of Food Type vs. Meal Type quantities.

🛠️ Data Architecture

The system aggregates data from 4 core tables:

Providers: Details of restaurants, grocery stores, and supermarkets.

Receivers: Details of NGOs, community centers, and individuals.

Food Listings: Quantities, expiry dates, and categories of available food.

Claims: Tracking the status (Pending/Completed/Cancelled) of distribution requests.

💡 Business Insights Generated

🏆 Top Provider Type: Restaurants donate the most food (6,923 units).

🥗 Highest Availability: Vegetarian items and Breakfast meals have the highest listing frequency.

⚠️ Wastage Risk: Lunch items experience the highest volume of Pending claims (89 pending), highlighting a need for better midday distribution logistics.

🤝 Distribution Gap: With nearly 33.6% of claims resulting in cancellation, there is a clear recommendation to automate coordination alerts between NGOs and providers.

💻 How to Run Locally

Clone this repository to your local machine.

Ensure you have Python installed, then install the dependencies:

pip install -r requirements.txt


Run the Streamlit application:

streamlit run app.py
