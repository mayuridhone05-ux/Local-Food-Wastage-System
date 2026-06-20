# 🥗 Local Food Wastage Management System
> An end-to-end data analytics and web application built to combat food insecurity and reduce food wastage by connecting surplus food providers directly with NGOs and receivers.
> 
### 📍 ** [LIVE INTERACTIVE DASHBOARD](https://local-food-wastage-system-drkcv2fgcpgpvaug8nb6vt.streamlit.app/)**
## 📌 The Business Problem
Food wastage is a critical global issue. While restaurants, supermarkets, and households discard massive amounts of surplus food daily, numerous communities struggle with severe food insecurity.
This project addresses this gap by developing a **Local Food Wastage Management System**—a centralized, data-driven platform where surplus food is tracked, provider locations are mapped, and distribution claims are monitored in real-time.
## 🛠️ Project Architecture & Features
This project showcases a full-stack data workflow, from raw CSV data to an in-memory SQL database, culminating in an interactive Streamlit frontend.
### 1. Interactive Streamlit Dashboard (app.py)
 * **Dynamic Slicers:** Users can instantly filter the entire database by Location, Provider Type, Meal Type, and Food Type.
 * **Live KPI Tracking:** Real-time metrics tracking total active providers, total food quantity available, and real-time claim completion percentages.
 * **Provider Contact Integration:** Generates accessible contact tables to facilitate direct, offline coordination between NGOs and food providers.
### 2. In-Memory SQL Analytics (sql_analysis.py)
 * Designed a transient **SQLite3 database** to process and join 4 distinct datasets.
 * Engineered **17 complex analytical queries** to identify logistical trends, including:
   * *Which provider types contribute the highest volume of food?*
   * *Which meal types carry the highest "wastage risk" (most pending claims)?*
   * *What is the completion vs. cancellation rate of distribution requests?*
 * Built an interactive **"SQL Query Explorer"** directly into the frontend, allowing users to run these queries live with the click of a button.
### 3. Exploratory Data Analysis (eda_analysis.py)
 * Generated automated, programmatic data visualizations using matplotlib and seaborn.
 * Mapped Provider & Receiver distributions, generated Food Type vs. Meal Type quantity heatmaps, and tracked claim status breakdowns.
## 🗄️ Data Schema
The system aggregates and relates data across 4 core tables:
 1. **providers_data.csv:** Details of restaurants, grocery stores, and supermarkets. *(Key: Provider_ID)*
 2. **receivers_data.csv:** Details of NGOs, community centers, and individuals. *(Key: Receiver_ID)*
 3. **food_listings_data.csv:** Quantities, expiry dates, and categories of available food. *(Foreign Key: Provider_ID)*
 4. **claims_data.csv:** Tracking the status (Pending/Completed/Cancelled) of distribution requests. *(Foreign Keys: Food_ID, Receiver_ID)*
## 💡 Strategic Business Insights
Based on the EDA and SQL querying, the following data-driven insights were discovered:
 * 🏆 **Top Contributor:** Restaurants dominate the platform, donating the most food overall (**6,923 units**).
 * 🥗 **Highest Availability:** Vegetarian items and Breakfast meals possess the highest listing frequency across the application.
 * 🤝 **Top Receivers:** Non-Governmental Organizations (NGOs) are the most active claimers, successfully claiming 272 orders.
 * ⚠️ **Wastage Risk Identification:** Lunch items experience the highest volume of *Pending* claims (**89 pending**), highlighting a critical need for better midday distribution logistics.
 * 📉 **Distribution Gap:** With **33.6%** of claims resulting in cancellation, there is a clear business recommendation to automate coordination alerts/SMS notifications between NGOs and providers before food expires.
## 💻 Repository Structure
```text
├── data/
│   ├── providers_data.csv
│   ├── receivers_data.csv
│   ├── food_listings_data.csv
│   └── claims_data.csv
├── app.py                  # Main Streamlit web application
├── sql_analysis.py         # 17 Advanced SQL queries & executions
├── eda_analysis.py         # Automated Python visualization scripts
├── requirements.txt        # Deployment dependencies
└── README.md               # Project documentation

```
## 🚀 How to Run Locally
To run this project on your local machine:
 1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Local-Food-Wastage-System.git 
   
   ```
 2. **Install the required libraries:**
   ```bash
   pip install -r requirements.txt
   
   ```
 3. **Run the standalone Analysis Scripts (Optional):**
   ```bash
   python sql_analysis.py
   python eda_analysis.py
   
   ```
 4. **Launch the Streamlit Web Application:**
   ```bash
   streamlit run app.py
   
   ```
