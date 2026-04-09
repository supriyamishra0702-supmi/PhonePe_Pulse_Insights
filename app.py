import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import json
import os

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="PhonePe Pulse Analysis", layout="wide", page_icon="📊")
st.title("📊 PhonePe Pulse: Strategic Business Insights")
st.markdown("---")

# 2. SQL ENGINE & CACHING
@st.cache_data
def fetch_data(query):
    try:
        conn = sqlite3.connect("phonepe_pulse.db")
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"⚠️ Database Error: {e}")
        return pd.DataFrame()

@st.cache_data
def load_geojson():
    if os.path.exists('india_states.json'):
        with open('india_states.json', 'r') as f:
            return json.load(f)
    return None

# 3. SIDEBAR FILTERS
st.sidebar.header("🧭 Navigation & Filters")

years_list = fetch_data("SELECT DISTINCT Year FROM aggregated_transaction ORDER BY Year DESC")
if not years_list.empty:
    years = years_list['Year'].tolist()
    selected_year = st.sidebar.selectbox("Select Year", years)
    
    states_list = fetch_data("SELECT DISTINCT State FROM aggregated_transaction ORDER BY State")
    states = ["All India"] + states_list['State'].tolist()
    selected_state = st.sidebar.selectbox("Select Region", states)
else:
    st.sidebar.error("Database not found! Run extraction.py first.")
    st.stop()

# 4. DASHBOARD LAYOUT
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ India Map", "📈 Market Analysis", "🏆 Leaderboards", "🎯 Strategic Case Studies"])

# --- TAB 1: GEOSPATIAL ---
with tab1:
    st.subheader(f"Transaction Intensity ({selected_year})")
    india_geojson = load_geojson()
    if india_geojson:
        map_df = fetch_data(f"SELECT State, SUM(Transaction_amount) as Amount FROM aggregated_transaction WHERE Year = {selected_year} GROUP BY State")
        map_df['State'] = map_df['State'].replace({
            "Andaman & Nicobar Islands": "Andaman & Nicobar Island", 
            "Dadra & Nagar Haveli & Daman & Diu": "Dadara & Nagar Havelli",
            "Delhi": "NCT of Delhi"
        })
        fig_map = px.choropleth(map_df, geojson=india_geojson, featureidkey='properties.ST_NM', locations='State', color='Amount', color_continuous_scale="Viridis")
        fig_map.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_map, use_container_width=True)

# --- TAB 2: ANALYSIS ---
with tab2:
    query = f"SELECT * FROM aggregated_transaction WHERE Year = {selected_year}"
    if selected_state != "All India": query += f" AND State = '{selected_state}'"
    df_main = fetch_data(query)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Payment Category Share")
        if not df_main.empty: st.plotly_chart(px.pie(df_main, values='Transaction_amount', names='Transaction_type', hole=0.4), use_container_width=True)
    with col2:
        st.subheader("Quarterly Performance")
        if not df_main.empty:
            q_df = df_main.groupby('Quarter')['Transaction_amount'].sum().reset_index()
            st.plotly_chart(px.bar(q_df, x='Quarter', y='Transaction_amount'), use_container_width=True)

# --- TAB 3: LEADERBOARD ---
with tab3:
    st.subheader(f"Top 10 States ({selected_year})")
    top_df = fetch_data(f"SELECT State, SUM(Transaction_amount) as Value FROM aggregated_transaction WHERE Year = {selected_year} GROUP BY State ORDER BY Value DESC LIMIT 10")
    if not top_df.empty: st.plotly_chart(px.bar(top_df, x='Value', y='State', orientation='h', color='Value'), use_container_width=True)

# --- TAB 4: THE 25 INSIGHTS ---
with tab4:
    st.header("🎯 Strategic Deep-Dives")
    case = st.selectbox("Select Case Study", ["1. Transaction Dynamics", "2. Device Dominance", "3. Insurance Penetration", "4. Market Expansion (ATV)", "5. Registration Hubs"])

    if case == "1. Transaction Dynamics":
        i1, i2, i3, i4, i5 = st.tabs(["Top Growth", "YoY Total", "Quarterly Pulse", "Regional Rank", "Max Peak"])
        with i1:
            df = fetch_data("SELECT State, SUM(Transaction_amount) as Amount FROM aggregated_transaction GROUP BY State ORDER BY Amount DESC LIMIT 5")
            st.plotly_chart(px.bar(df, x='State', y='Amount'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT State, SUM(Transaction_amount) FROM aggregated_transaction GROUP BY State ORDER BY Amount DESC LIMIT 5;", language="sql")
        with i2:
            df = fetch_data("SELECT Year, SUM(Transaction_amount) AS Total FROM aggregated_transaction GROUP BY Year")
            st.plotly_chart(px.line(df, x='Year', y='Total', markers=True), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT Year, SUM(Transaction_amount) FROM aggregated_transaction GROUP BY Year;", language="sql")
        with i3:
            df = fetch_data("SELECT Quarter, AVG(Transaction_amount) as Avg FROM aggregated_transaction GROUP BY Quarter")
            st.plotly_chart(px.pie(df, values='Avg', names='Quarter'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT Quarter, AVG(Transaction_amount) FROM aggregated_transaction GROUP BY Quarter;", language="sql")
        with i4:
            df = fetch_data(f"SELECT Quarter, SUM(Transaction_count) as Count FROM aggregated_transaction WHERE State = '{selected_state if selected_state != 'All India' else 'Maharashtra'}' GROUP BY Quarter")
            st.plotly_chart(px.bar(df, x='Quarter', y='Count'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT State, Quarter, SUM(Transaction_count) FROM aggregated_transaction GROUP BY Quarter;", language="sql")
        with i5:
            df = fetch_data("SELECT Transaction_type, MAX(Transaction_amount) as Peak FROM aggregated_transaction GROUP BY Transaction_type")
            st.plotly_chart(px.bar(df, x='Transaction_type', y='Peak'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT Transaction_type, MAX(Transaction_amount) FROM aggregated_transaction GROUP BY Transaction_type;", language="sql")

    elif case == "2. Device Dominance":
        i1, i2, i3, i4, i5 = st.tabs(["Market Leader", "Top Brand/State", "Avg Share", "Brand Diversity", "2022 Snapshot"])
        with i1:
            df = fetch_data("SELECT Brand, SUM(Count) AS Total_Users FROM aggregated_user GROUP BY Brand ORDER BY Total_Users DESC")
            st.plotly_chart(px.bar(df, x='Brand', y='Total_Users'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT Brand, SUM(Count) FROM aggregated_user GROUP BY Brand ORDER BY Total_Users DESC;", language="sql")
        with i2:
            df = fetch_data("SELECT State, Brand, MAX(Count) as Max_Count FROM aggregated_user GROUP BY State LIMIT 10")
            st.table(df)
            with st.expander("SQL Query"): st.code("SELECT State, Brand, MAX(Count) FROM aggregated_user GROUP BY State;", language="sql")
        with i3:
            df = fetch_data("SELECT Brand, AVG(Percentage) * 100 AS Avg_Share FROM aggregated_user GROUP BY Brand")
            st.plotly_chart(px.pie(df, values='Avg_Share', names='Brand'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT Brand, AVG(Percentage) * 100 FROM aggregated_user GROUP BY Brand;", language="sql")
        with i4:
            st.write("### Brand Diversity by State (Stacked Composition)")
            div_query = f"""
                SELECT State, Brand, SUM(Count) as User_Count 
                FROM aggregated_user 
                WHERE Year = {selected_year}
                AND State IN (
                    SELECT State FROM aggregated_user 
                    WHERE Year = {selected_year} 
                    GROUP BY State ORDER BY SUM(Count) DESC LIMIT 10
                )
                GROUP BY State, Brand
            """
            div_df = fetch_data(div_query)
            if not div_df.empty:
                st.plotly_chart(px.bar(div_df, x='State', y='User_Count', color='Brand', title="Top 10 States: Brand Distribution"), use_container_width=True)
            else:
                st.warning("No brand data available for this selection.")
            with st.expander("SQL Query"): st.code(div_query, language="sql")
        with i5:
            df = fetch_data("SELECT Brand, SUM(Count) as Count FROM aggregated_user WHERE Year = 2022 GROUP BY Brand")
            st.plotly_chart(px.bar(df, x='Brand', y='Count'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT Brand, SUM(Count) FROM aggregated_user WHERE Year = 2022 GROUP BY Brand;", language="sql")

    elif case == "3. Insurance Penetration":
        i1, i2, i3, i4, i5 = st.tabs(["Top Markets", "Total Policies", "Avg Premium", "Yearly Growth", "Policy Distribution"])
        with i1:
            df = fetch_data("SELECT State, SUM(Amount) as Amount FROM aggregated_insurance GROUP BY State ORDER BY Amount DESC LIMIT 5")
            st.plotly_chart(px.bar(df, x='State', y='Amount'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT State, SUM(Amount) FROM aggregated_insurance GROUP BY State ORDER BY Amount DESC LIMIT 5;", language="sql")
        with i2:
            df = fetch_data("SELECT Year, SUM(Count) as Total_Count FROM aggregated_insurance GROUP BY Year")
            st.plotly_chart(px.line(df, x='Year', y='Total_Count', markers=True), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT Year, SUM(Count) FROM aggregated_insurance GROUP BY Year;", language="sql")
        with i3:
            df = fetch_data("SELECT State, (SUM(Amount)/SUM(Count)) AS Avg_Premium FROM aggregated_insurance GROUP BY State ORDER BY Avg_Premium DESC LIMIT 10")
            st.plotly_chart(px.bar(df, x='State', y='Avg_Premium'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT State, (SUM(Amount)/SUM(Count)) AS Avg_Premium FROM aggregated_insurance GROUP BY State;", language="sql")
        with i4:
            df = fetch_data("SELECT Year, SUM(Amount) as Total_Amount FROM aggregated_insurance GROUP BY Year")
            st.plotly_chart(px.bar(df, x='Year', y='Total_Amount'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT Year, SUM(Amount) FROM aggregated_insurance GROUP BY Year;", language="sql")
        with i5:
            df = fetch_data("SELECT State, SUM(Count) as Count FROM aggregated_insurance GROUP BY State ORDER BY Count DESC LIMIT 10")
            st.plotly_chart(px.pie(df, values='Count', names='State'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT State, SUM(Count) FROM aggregated_insurance GROUP BY State;", language="sql")

    elif case == "4. Market Expansion (ATV)":
        i1, i2, i3, i4, i5 = st.tabs(["Highest ATV", "Type ATV", "Premium States", "ATV Trend", "Lowest ATV"])
        with i1:
            df = fetch_data("SELECT State, (SUM(Transaction_amount)/SUM(Transaction_count)) AS ATV FROM aggregated_transaction GROUP BY State ORDER BY ATV DESC LIMIT 10")
            st.plotly_chart(px.bar(df, x='State', y='ATV'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT State, (SUM(Transaction_amount)/SUM(Transaction_count)) AS ATV FROM aggregated_transaction GROUP BY State ORDER BY ATV DESC;", language="sql")
        with i2:
            df = fetch_data("SELECT Transaction_type, (SUM(Transaction_amount)/SUM(Transaction_count)) AS Type_ATV FROM aggregated_transaction GROUP BY Transaction_type")
            st.plotly_chart(px.bar(df, x='Transaction_type', y='Type_ATV'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT Transaction_type, (SUM(Transaction_amount)/SUM(Transaction_count)) AS Type_ATV FROM aggregated_transaction GROUP BY Transaction_type;", language="sql")
        with i3:
            df = fetch_data("SELECT State, (SUM(Transaction_amount)/SUM(Transaction_count)) AS ATV FROM aggregated_transaction GROUP BY State HAVING ATV > 1000 ORDER BY ATV DESC")
            st.dataframe(df)
            with st.expander("SQL Query"): st.code("SELECT State FROM aggregated_transaction GROUP BY State HAVING (SUM(Transaction_amount)/SUM(Transaction_count)) > 1000;", language="sql")
        with i4:
            df = fetch_data("SELECT Year, (SUM(Transaction_amount)/SUM(Transaction_count)) AS Yearly_ATV FROM aggregated_transaction GROUP BY Year")
            st.plotly_chart(px.line(df, x='Year', y='Yearly_ATV', markers=True), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT Year, (SUM(Transaction_amount)/SUM(Transaction_count)) AS Yearly_ATV FROM aggregated_transaction GROUP BY Year;", language="sql")
        with i5:
            df = fetch_data("SELECT State, (SUM(Transaction_amount)/SUM(Transaction_count)) AS Min_ATV FROM aggregated_transaction GROUP BY State ORDER BY Min_ATV ASC LIMIT 5")
            st.plotly_chart(px.bar(df, x='State', y='Min_ATV'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT State, (SUM(Transaction_amount)/SUM(Transaction_count)) AS Min_ATV FROM aggregated_transaction GROUP BY State ORDER BY Min_ATV ASC LIMIT 5;", language="sql")

    elif case == "5. Registration Hubs":
        i1, i2, i3, i4, i5 = st.tabs(["Top Hubs", "India Total", "Current Year", "Quarterly Spike", "Growth State"])
        with i1:
            df = fetch_data("SELECT State, SUM(Count) AS Total_Reg FROM aggregated_user GROUP BY State ORDER BY Total_Reg DESC LIMIT 5")
            st.plotly_chart(px.bar(df, x='State', y='Total_Reg'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT State, SUM(Count) FROM aggregated_user GROUP BY State ORDER BY Total_Reg DESC LIMIT 5;", language="sql")
        with i2:
            df = fetch_data("SELECT Year, SUM(Count) as Total FROM aggregated_user GROUP BY Year")
            st.plotly_chart(px.line(df, x='Year', y='Total', markers=True), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT SUM(Count) FROM aggregated_user;", language="sql")
        with i3:
            df = fetch_data(f"SELECT State, SUM(Count) as Count FROM aggregated_user WHERE Year = {selected_year} GROUP BY State ORDER BY Count DESC LIMIT 10")
            st.plotly_chart(px.bar(df, x='State', y='Count'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT State, SUM(Count) FROM aggregated_user WHERE Year = ? GROUP BY State;", language="sql")
        with i4:
            df = fetch_data("SELECT Quarter, SUM(Count) as Count FROM aggregated_user GROUP BY Quarter")
            st.plotly_chart(px.pie(df, values='Count', names='Quarter'), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT Quarter, SUM(Count) FROM aggregated_user GROUP BY Quarter;", language="sql")
        with i5:
            df = fetch_data(f"SELECT Year, SUM(Count) as Count FROM aggregated_user WHERE State = '{selected_state if selected_state != 'All India' else 'Karnataka'}' GROUP BY Year")
            st.plotly_chart(px.line(df, x='Year', y='Count', markers=True), use_container_width=True)
            with st.expander("SQL Query"): st.code("SELECT State, Year, SUM(Count) FROM aggregated_user WHERE State = ? GROUP BY Year;", language="sql")

