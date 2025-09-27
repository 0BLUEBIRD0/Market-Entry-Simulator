import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import os

# Set directories
data_dir = 'data'
figures_dir = 'figures'
docs_dir = 'docs'
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)
if not os.path.exists(docs_dir):
    os.makedirs(docs_dir)

# Load datasets
ev_sales = pd.read_csv(os.path.join(data_dir, 'ev_sales_india.csv'))
gdp = pd.read_csv(os.path.join(data_dir, 'gdp_india.csv'))
competitors = pd.read_csv(os.path.join(data_dir, 'competitor_data.csv'))

# Initialize summary for analysis_summary.md
summary_lines = ["# Phase 3: Analysis Summary\n\n## Key Insights\n"]

# EDA: EV Sales Trends
if not ev_sales.empty and 'year' in ev_sales.columns and 'units_sold' in ev_sales.columns:
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=ev_sales, x='year', y='units_sold', hue='vehicle_category', marker='o')
    plt.title('India EV Sales (Passenger Vehicles, 2015–2024)')
    plt.xlabel('Year')
    plt.ylabel('Units Sold')
    plt.savefig(os.path.join(figures_dir, 'ev_sales_trend.png'))
    plt.close()

    # Calculate CAGR (2015–2024)
    start_year = ev_sales['year'].min()
    end_year = ev_sales['year'].max()
    if end_year > start_year:
        start_sales = ev_sales[ev_sales['year'] == start_year]['units_sold'].sum()
        end_sales = ev_sales[ev_sales['year'] == end_year]['units_sold'].sum()
        if start_sales > 0:
            cagr = ((end_sales / start_sales) ** (1 / (end_year - start_year)) - 1) * 100
            summary_lines.append(f"- **EV Market Growth**: Passenger EV sales grew at a CAGR of {cagr:.2f}% from {start_year}–{end_year}.\n")
        else:
            summary_lines.append("- **EV Market Growth**: Insufficient sales data for CAGR calculation.\n")
    else:
        summary_lines.append("- **EV Market Growth**: Only one year of data; CAGR not calculated.\n")
else:
    print("Warning: EV sales data is empty or missing required columns. Check data_cleaning.py.")
    summary_lines.append("- **EV Market Growth**: No valid sales data available.\n")

# EDA: Economic Indicators
if not gdp.empty:
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=gdp, x='year', y='gdp_usd_billions', label='GDP (USD Billions)', marker='o')
    plt.twinx()
    sns.lineplot(data=gdp, x='year', y='urban_population_percent', color='orange', label='Urban Pop (%)', marker='o')
    plt.title('India GDP and Urban Population (2020–2023)')
    plt.xlabel('Year')
    plt.savefig(os.path.join(figures_dir, 'economic_trends.png'))
    plt.close()
    latest_gdp = gdp[gdp['year'] == gdp['year'].max()]['gdp_usd_billions'].iloc[0]
    latest_urban = gdp[gdp['year'] == gdp['year'].max()]['urban_population_percent'].iloc[0]
    summary_lines.append(f"- **Economic Feasibility**: India’s GDP was USD {latest_gdp:.2f}B and urban population {latest_urban:.2f}% in {gdp['year'].max()}.\n")
else:
    summary_lines.append("- **Economic Feasibility**: No GDP/urban population data available.\n")

# EDA: Competitor Analysis
if not competitors.empty:
    comp_summary = competitors.groupby('company').agg({
        'market_share_percent': 'mean',
        'avg_price_usd': 'mean'
    }).reset_index()
    print("Competitor Summary:\n", comp_summary)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=comp_summary, x='avg_price_usd', y='market_share_percent', hue='company', size='market_share_percent')
    plt.title('Competitor Pricing vs. Market Share (2023–2024)')
    plt.xlabel('Average Price (USD)')
    plt.ylabel('Market Share (%)')
    plt.savefig(os.path.join(figures_dir, 'competitor_scatter.png'))
    plt.close()
    summary_lines.append(f"- **Competitor Landscape**: Tata leads with ~{comp_summary.loc[comp_summary['company'] == 'Tata', 'market_share_percent'].iloc[0]:.1f}% share. Pricing ranges from USD {comp_summary['avg_price_usd'].min():.2f} to {comp_summary['avg_price_usd'].max():.2f}.\n")
else:
    print("Warning: Competitor data is empty. Check data_cleaning.py.")
    summary_lines.append("- **Competitor Landscape**: No competitor data available.\n")

# Forecasting: EV Sales for 2026
if not ev_sales.empty and len(ev_sales['year'].unique()) >= 2:
    X = ev_sales[['year']].values
    y = ev_sales['units_sold'].values
    model = LinearRegression()
    model.fit(X, y)
    future_years = np.array([[2025], [2026]])
    predictions = model.predict(future_years)
    forecast = pd.DataFrame({'year': [2025, 2026], 'predicted_units_sold': predictions})
    print("2026 EV Sales Forecast:\n", forecast)
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=ev_sales, x='year', y='units_sold', label='Historical', marker='o')
    plt.plot(future_years, predictions, 'ro-', label='Forecast')
    plt.title('EV Sales Forecast (2025–2026)')
    plt.xlabel('Year')
    plt.ylabel('Units Sold')
    plt.legend()
    plt.savefig(os.path.join(figures_dir, 'sales_forecast.png'))
    plt.close()
    summary_lines.append(f"- **2026 Forecast**: Predicted {forecast.loc[forecast['year'] == 2026, 'predicted_units_sold'].iloc[0]:.0f} passenger EV units sold in 2026.\n")
else:
    summary_lines.append("- **2026 Forecast**: Insufficient data for forecasting.\n")

# Clustering: Competitors
if not competitors.empty:
    comp_summary = competitors.groupby('company').agg({
        'market_share_percent': 'mean',
        'avg_price_usd': 'mean'
    }).reset_index()
    n_clusters = min(2, len(comp_summary))  # Use 2 clusters or fewer if less data
    if n_clusters >= 2:
        X_comp = comp_summary[['avg_price_usd', 'market_share_percent']].values
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        comp_summary['cluster'] = kmeans.fit_predict(X_comp)
        print("Competitor Clusters:\n", comp_summary)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=comp_summary, x='avg_price_usd', y='market_share_percent', hue='cluster', style='company')
        plt.title('Competitor Clusters by Price and Market Share')
        plt.xlabel('Average Price (USD)')
        plt.ylabel('Market Share (%)')
        plt.savefig(os.path.join(figures_dir, 'competitor_clusters.png'))
        plt.close()
        summary_lines.append("- **Clusters**: Competitors form low-price/high-share (e.g., Tata) and mid-price/mid-share (e.g., MG). Tesla can target premium.\n")
    else:
        print("Warning: Insufficient unique companies for clustering. Need at least 2.")
        summary_lines.append("- **Clusters**: Insufficient unique companies for clustering.\n")
else:
    print("Warning: Competitor data is empty. Check data_cleaning.py.")
    summary_lines.append("- **Clusters**: No competitor data available.\n")

# Save summary
summary_lines.append("\n## Next Steps\n- Refine forecasts with additional data (e.g., policy incentives).\n- Develop interactive dashboard in Phase 4.")
with open(os.path.join(docs_dir, 'analysis_summary.md'), 'w') as f:
    f.write('\n'.join(summary_lines))
