# Indian E-Commerce Big Data Analytics Platform (Ecommerce-BDA)

An end-to-end Big Data Analytics suite for Indian E-Commerce datasets featuring synthetic data generation in Indian Rupees (INR / ₹), data ingestion, PySpark batch analytics, relational/columnar storage integration (SQLite & DuckDB), and an interactive Streamlit multi-page dashboard.

## Project Structure

```text
ecommerce-bda/
├── app.py                 # Streamlit main entry point
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore patterns
├── config/                # Configuration management
├── database/              # SQLite/DuckDB schema & storage
├── data/                  # Raw & processed data storage (INR datasets)
├── ingestion/             # Data generation & ETL pipelines
├── spark/                 # PySpark jobs & analytics scripts
├── analytics/             # Business intelligence & metrics logic
├── pages/                 # Streamlit multi-page dashboard views
├── utils/                 # Currency formatters, logging, db connectors
│   └── currency.py        # Centralized INR (₹) formatting utility
├── tests/                 # Unit & integration tests
└── assets/                # Visual assets, stylesheets, icons
```

## Features
- **INR Currency System**: Centralized formatting utility (`utils/currency.py`) supporting standard Indian numbering (₹1,00,000) and compact formats (₹62.32L, ₹1.25Cr).
- **Indian Marketplace Data**: Realistic product categories, price ranges in INR (₹50 to ₹1,50,000), Indian state/city geographic metadata, and UPI/COD payment methods.
- **Spark & DuckDB Analytics**: Scalable PySpark and DuckDB analytics for customer RFM segmentation, conversion funnels, and revenue aggregations.
- **Interactive Dashboard**: Streamlit multi-page dashboard with real-time KPI metrics, Plotly visualizations, and SQL analytical workbench.

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy environment file:
   ```bash
   cp .env.example .env
   ```
3. Run Data Ingestion & ETL:
   ```bash
   python -m ingestion.etl_pipeline
   ```
4. Launch Streamlit Dashboard:
   ```bash
   streamlit run app.py
   ```
