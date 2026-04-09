PhonePe Pulse: Strategic Business Insights Dashboard

Project Overview
This project is an interactive Business Intelligence (BI) Dashboard built to analyze 5+ years of digital transaction data from the PhonePe Pulse repository. The tool transforms raw, nested JSON data into a structured relational database and visualises it through 25 distinct strategic case studies, providing a "pulse" of India's digital payment landscape.

Tech Stack
Language: Python 3.10+
Database: SQLite3
Dashboard: Streamlit
Visualization: Plotly Express (Bar, Line, Pie, Treemap, Choropleth)
Data Processing: Pandas, JSON, OS

Project Architecture
Data Extraction (ETL): Scripted a robust pipeline to iterate through thousands of JSON files, standardise state names, and handle missing data (e.g., brand data post-2022).
Data Storage: Structured the processed data into three relational tables: aggregated_transaction, aggregated_user, and aggregated_insurance.
Insights Engine: Developed a multi-tab Streamlit interface that uses SQL-level filtering and aggregation to generate real-time reports.

Key Features & 25 Strategic Insights
The dashboard is divided into four main sections, with a deep-dive "Case Study" tab featuring:
1. Transaction Dynamics
Analysis of Top Growth States, Yearly Totals, and Quarterly Spending Pulses.
2. Device Dominance
Market Leader analysis and a Stacked Brand Composition chart to identify hardware diversity across states.
3. Insurance Penetration
Identifying "Blue Ocean" markets through Average Premium calculations and Policy Distribution trends.
4. Market Expansion (ATV)
Using Average Transaction Value (ATV) to distinguish between premium spending hubs (ATV > ₹1000) and micro-payment markets.
5. Registration Hubs
Pinpointing acquisition powerhouses and tracking user registration growth rates.

How to Run Locally

Clone the Data:
git clone https://github.com/PhonePe/pulse.git phonepe_pulse_data


Setup Environment:
pip install streamlit pandas plotly requests

Run Extraction:
python extraction.py


Launch Dashboard:
streamlit run app.py


This dashboard demonstrates how Data Engineering (ETL) and Data Analytics (SQL + Visualization) work together to turn raw numbers into business strategy. Each chart includes a "View SQL" expander to provide full transparency into the data logic.




