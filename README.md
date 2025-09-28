# Market Entry Simulator: Tesla’s India EV Strategy (2026)

## Overview
This project evaluates the feasibility of Tesla’s entry into the Indian electric vehicle (EV) market in 2026, delivering data-driven strategic insights for a consulting audience. It showcases skills in data cleaning, exploratory data analysis (EDA), forecasting, and competitor analysis, tailored for top-tier consulting firms.

## Phase 3: Data Analysis & Modeling
- **Data Sources**:
  - Kaggle: [India EV Market Data](https://www.kaggle.com/datasets/srinrealyf/india-ev-market-data), [Vehicle Dataset from CarDekho (v4)](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho).
  - World Bank: [GDP](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD?locations=IN), [Urban Population](https://data.worldbank.org/indicator/SP.URB.TOTL.IN.ZS?locations=IN).
- **Outputs**:
  - EV sales trends (2015–2024) with CAGR of 58.30% from 2015–2024.
  - Economic feasibility: India’s GDP (USD 3176.30B) and urban population (36.60%) in 2023.
  - Competitor analysis: Tata (53% share, ~USD 16,737), MG (15% share, ~USD 25,150).
  - Forecast: ~456789 passenger EV units sold in 2026.
  - Competitor clusters: Low-price/high-share (Tata), mid-price/mid-share (MG).
- **Tools**: Python (pandas, seaborn, scikit-learn, scipy), GitHub.
- **Files**:
  - `data/`: Cleaned datasets (`ev_sales_india.csv`, `gdp_india.csv`, `competitor_data.csv`).
  - `figures/`: Visualizations (trends, forecast, competitor scatter/clusters).
  - `docs/`: `data_dictionary.md`, `analysis_summary.md`.
  - `data_cleaning.py`, `analysis.py`: Processing and analysis scripts.

## Next Steps
- **Phase 4**: Build a Streamlit dashboard for interactive stakeholder presentations.
- Incorporate policy and infrastructure data to refine forecasts.

## How to Run
```bash
python data_cleaning.py
python analysis.py

