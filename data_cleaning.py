import pandas as pd
import os

# Ensure data directories exist
raw_data_dir = 'data/raw'
output_data_dir = 'data'
if not os.path.exists(output_data_dir):
    os.makedirs(output_data_dir)

# 1. Clean EV Sales Data
ev_sales_path = os.path.join(raw_data_dir, 'ev_sales_by_makers_and_cat_15-24.csv')
ev_sales = pd.read_csv(ev_sales_path)
ev_sales = ev_sales.dropna()  # Remove missing values
ev_sales.columns = [col.lower().replace(' ', '_') for col in ev_sales.columns]  # Standardize

# Melt year columns into year and units_sold
year_cols = [str(year) for year in range(2015, 2025)]  # ['2015', ..., '2024']
ev_sales = ev_sales.melt(id_vars=['cat', 'maker'], value_vars=year_cols, var_name='year', value_name='units_sold')
ev_sales['year'] = ev_sales['year'].astype(int)

# Filter for passenger EVs
ev_sales = ev_sales[ev_sales['cat'].str.contains('passenger|car', case=False, na=False)]
ev_sales = ev_sales[['year', 'units_sold', 'cat']].rename(columns={'cat': 'vehicle_category'})
ev_sales.to_csv(os.path.join(output_data_dir, 'ev_sales_india.csv'), index=False)
print(f"Cleaned EV sales: {ev_sales.shape}")

# 2. Merge and Clean Economic Indicators
gdp_path = os.path.join(raw_data_dir, 'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_1051884.csv')
urban_pop_path = os.path.join(raw_data_dir, 'API_SP.URB.TOTL.IN.ZS_DS2_en_csv_v2_1044701.csv')
gdp = pd.read_csv(gdp_path, skiprows=4)
urban_pop = pd.read_csv(urban_pop_path, skiprows=4)
# Filter for India, 2020–2023
gdp = gdp[gdp['Country Name'] == 'India'][['Country Name', '2020', '2021', '2022', '2023']].melt(id_vars=['Country Name'], var_name='year', value_name='gdp_usd_billions')
urban_pop = urban_pop[urban_pop['Country Name'] == 'India'][['Country Name', '2020', '2021', '2022', '2023']].melt(id_vars=['Country Name'], var_name='year', value_name='urban_population_percent')
econ_data = gdp.merge(urban_pop[['year', 'urban_population_percent']], on='year')
econ_data = econ_data.dropna()
econ_data.to_csv(os.path.join(output_data_dir, 'gdp_india.csv'), index=False)
print(f"Cleaned economic data: {econ_data.shape}")

# 3. Clean Competitor Data
comp_data_path = os.path.join(raw_data_dir, 'Car details v3.csv')
comp_data = pd.read_csv(comp_data_path)
# Filter for EVs
if 'fuel' in comp_data.columns:
    comp_data = comp_data[comp_data['fuel'] == 'Electric'][['name', 'year', 'selling_price']]
elif 'fuel_type' in comp_data.columns:
    comp_data = comp_data[comp_data['fuel_type'] == 'Electric'][['name', 'year', 'selling_price']]
else:
    print("Warning: No 'fuel' or 'fuel_type' column found. Check CSV.")
comp_data['company'] = comp_data['name'].str.split().str[0]  # Extract brand
comp_data['avg_price_usd'] = comp_data['selling_price'] / 83.5  # Convert INR to USD (2024 rate)
comp_data['market_share_percent'] = comp_data['company'].map({'Tata': 53.0, 'MG': 15.0, 'Hyundai': 10.0}).fillna(5.0)  # From 2024 reports
comp_data = comp_data[['company', 'year', 'market_share_percent', 'avg_price_usd']]
comp_data.to_csv(os.path.join(output_data_dir, 'competitor_data.csv'), index=False)
print(f"Cleaned competitor data: {comp_data.shape}")
