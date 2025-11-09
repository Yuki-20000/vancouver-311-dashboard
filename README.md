# 🏙️ Vancouver 311 Dashboard

Interactive dashboard for visualizing Vancouver's 311 service requests.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vancouver-311-dashboard.streamlit.app/)

## 📊 Overview
This Streamlit dashboard provides an interactive visualization of Vancouver's 311 service requests from the past 3 months. The data is fetched from the City of Vancouver's Open Data Portal.

**Features:**
- **KPI Metrics**: Total requests, open/closed counts, and top area
- **Interactive Map**: Choropleth map showing requests by local area
- **Time Series Chart**: Weekly request trends over time
- **Service Type Distribution**: Top service categories
- **Advanced Filters**: Filter by date range, status and local area

## 🛠️ Tech Stack
- **Streamlit** - Web framework
- **Pandas & GeoPandas** - Data processing
- **Altair & Folium** - Visualization
- **Vancouver Open Data API** - Data source

## 📊 Data Source
This dashboard uses data from the City of Vancouver's Open Data Portal:
- [311 Service Requests API](https://opendata.vancouver.ca/explore/dataset/3-1-1-service-requests/information/)
- [Local Area Boundaries API](https://opendata.vancouver.ca/explore/dataset/local-area-boundary/information/)

## 📁 Project Structure
```
vancouver-311-dashboard/
├── app.py              # Main application
├── requirements.txt    # Dependencies
└── src/
    ├── api.py         # Data fetching
    ├── charts.py      # Visualizations
    ├── filters.py     # Filter components
    ├── kpi.py         # KPI calculations
    ├── config.py      # Configuration
    └── constants.py   # Constants
```
