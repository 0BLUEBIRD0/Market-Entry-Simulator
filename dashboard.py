import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Tesla India EV Market Entry (2026)", layout="wide")

st.title("Tesla India EV Market Entry Simulator (2026)")
st.markdown("Strategic analysis for Tesla’s 2026 entry into India’s EV market, built for consulting-grade insights.")

# Load data
data_dir = 'data'
ev_sales = pd.read_csv(os.path.join(data_dir, 'ev_sales_india.csv'))
gdp = pd.read_csv(os.path.join(data_dir, 'gdp_india.csv'))
competitors = pd.read_csv(os.path.join(data_dir, 'competitor_data.csv'))

# Sidebar filters
st.sidebar.header("Filters")
years = st.sidebar.slider("Select Years for Sales", int(ev_sales['year'].min()), int(ev_sales['year'].max()), (2015, 2024))
category = st.sidebar.multiselect("Select Vehicle Category", ev_sales['vehicle_category'].unique(), default=ev_sales['vehicle_category'].unique())

# Filter data
ev_sales_filtered = ev_sales[ev_sales['year'].between(years[0], years[1]) & ev_sales['vehicle_category'].isin(category)]

# Layout
col1, col2 = st.columns(2)

# EV Sales Trend
with col1:
    st.header("EV Sales Trends (2015–2024)")
    ev_sales_agg = ev_sales_filtered.groupby('year')['units_sold'].sum().reset_index()
    fig1 = px.line(ev_sales_agg, x='year', y='units_sold', markers=True, title='India EV Sales (Passenger Vehicles)')
    fig1.update_layout(xaxis_title='Year', yaxis_title='Units Sold')
    st.plotly_chart(fig1, use_container_width=True)

# 2026 Forecast
with col2:
    st.header("EV Sales Forecast (2025–2026)")
    ev_sales_agg_all = ev_sales.groupby('year')['units_sold'].sum().reset_index()
    fig2 = px.line(ev_sales_agg_all, x='year', y='units_sold', title='EV Sales Forecast')
    forecast = pd.DataFrame({'year': [2025, 2026], 'predicted_units_sold': [374123.456, 456789.123]})  # Update with actual
    fig2.add_scatter(x=forecast['year'], y=forecast['predicted_units_sold'], mode='lines+markers', name='Forecast', line=dict(color='red'))
    fig2.update_layout(xaxis_title='Year', yaxis_title='Units Sold')
    st.plotly_chart(fig2, use_container_width=True)

# Economic Indicators
st.header("Economic Feasibility (2020–2023)")
fig3 = px.line(gdp, x='year', y='gdp_usd_billions', title='India GDP and Urban Population')
fig3.add_scatter(x=gdp['year'], y=gdp['urban_population_percent'], yaxis='y2', name='Urban Pop (%)', line=dict(color='orange'))
fig3.update_layout(yaxis_title='GDP (USD Billions)', yaxis2=dict(title='Urban Pop (%)', overlaying='y', side='right'))
st.plotly_chart(fig3, use_container_width=True)

# Competitor Analysis
col3, col4 = st.columns(2)
with col3:
    st.header("Competitor Pricing vs. Market Share")
    comp_summary = competitors.groupby('company').agg({'market_share_percent': 'mean', 'avg_price_usd': 'mean'}).reset_index()
    fig4 = px.scatter(comp_summary, x='avg_price_usd', y='market_share_percent', color='company', size='market_share_percent',
                      title='Competitor Pricing vs. Market Share (2023–2024)', text='company')
    fig4.update_traces(textposition='top center')
    fig4.update_layout(xaxis_title='Average Price (USD)', yaxis_title='Market Share (%)')
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    st.header("Competitor Clusters")
    comp_summary['cluster'] = [0, 1]  # Update with actual clusters
    fig5 = px.scatter(comp_summary, x='avg_price_usd', y='market_share_percent', color='cluster', symbol='company',
                      title='Competitor Clusters by Price and Market Share', text='company')
    fig5.update_traces(textposition='top center')
    fig5.update_layout(xaxis_title='Average Price (USD)', yaxis_title='Market Share (%)')
    st.plotly_chart(fig5, use_container_width=True)

# Key Metrics
st.header("Key Metrics")
st.metric("2026 EV Sales Forecast", f"{456789:,} units")  # Update with actual
st.metric("Tata Market Share", "53.0%")
st.metric("MG Market Share", "15.0%")
st.markdown(f"**CAGR (2015–2024)**: 58.30%")
st.markdown(f"**2023 GDP**: USD 3176.30B")
st.markdown(f"**2023 Urban Population**: 36.60%")
