Data Dictionary: Market Entry Simulator
This document describes the datasets used to analyze Tesla’s potential entry into the Indian EV market in 2026.
1. ev_sales_india.csv

Source: Kaggle - India EV Market Data 2001–2024
Description: Historical EV sales in India, filtered for passenger vehicles (2015–2024).
Variables:
year: Integer (e.g., 2020)
units_sold: Integer, number of EVs sold
vehicle_category: String, vehicle type (passenger cars)


Use: Estimate market size and CAGR for 2026 projections.

2. gdp_india.csv

Source: World Bank - GDP, Urban Population
Description: Economic indicators for India (2020–2023).
Variables:
year: Integer
gdp_usd_billions: Float, GDP in USD billions
urban_population_percent: Float, urban population as % of total


Use: Assess economic feasibility and consumer base.

3. competitor_data.csv

Source: Kaggle - Vehicle Dataset from CarDekho, enriched with 2024 market share data
Description: Market share and pricing of EV players in India (2023–2024).
Variables:
company: String (e.g., Tata, MG)
year: Integer
market_share_percent: Float, % of EV market
avg_price_usd: Float, average vehicle price in USD


Use: Analyze competitive landscape for Tesla’s entry.
