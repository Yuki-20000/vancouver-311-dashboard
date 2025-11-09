import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import streamlit as st
from dateutil.relativedelta import relativedelta

from src.config import TIMEZONE, PAST_MONTHS, TOP_N
from src.constants import (
    KPI_TOTAL_KEY,
    KPI_OPEN_KEY,
    KPI_CLOSED_KEY,
    KPI_TOP_AREA_KEY
)
from src.api import get_311_dataframe
from src.filters import sidebar_filters
from src.kpis import compute_kpis
from src.charts import plot_311_map, plot_311_line, plot_311_pie

# -- Configure logging --
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -- Get dates --
today = datetime.now(ZoneInfo(TIMEZONE)).date()
yesterday = today - timedelta(days=1)
start_date = yesterday - relativedelta(months=PAST_MONTHS)

# -- Setting --
st.set_page_config(
    page_title='Vancouver 311 Service Requests Dashboard',
    page_icon='📍',
    layout='wide',
    initial_sidebar_state='expanded'   
)

# -- Title --
st.title('Vancouver 311 Service Requests Dashboard')
st.markdown(f'''
    Data covers the past {PAST_MONTHS} months ({start_date} to {yesterday})<br>
    Source: [Open Data Vancouver](https://opendata.vancouver.ca/explore/dataset/3-1-1-service-requests/)<br>
    License: [ODbL](https://opendata.vancouver.ca/pages/licence/)
''', unsafe_allow_html=True)

# -- Get data --
df_311 = get_311_dataframe(
    start_date=start_date,
    end_date=yesterday
)

if df_311 is None:
    st.error('Failed to obtain data')
    st.stop()

# -- Filter data --
df_311 = sidebar_filters(df_311, start_date, yesterday)

if df_311.empty:
    st.warning('No data matches the selected filters. Please adjust your filter criteria.')
    st.stop()

# -- KPI --
kpis = compute_kpis(df_311)

kpi_cols = st.columns(4)
kpi_cols[0].metric('Total Requests', kpis.get(KPI_TOTAL_KEY, 0))
kpi_cols[1].metric('Open Requests', kpis.get(KPI_OPEN_KEY, 0))
kpi_cols[2].metric('Closed Requests', kpis.get(KPI_CLOSED_KEY, 0))
kpi_cols[3].metric('Top Area (valid locations only)', kpis.get(KPI_TOP_AREA_KEY, 'N/A'))

# -- Charts --
col1, col2, col3 = st.columns(3)

with col1:
    st.text('Requests by Local Area')
    plot_311_map(df_311)
with col2:
    st.text('Weekly Requests')
    plot_311_line(df_311)
with col3:
    st.text(f'Service Request Types (Up to {TOP_N})')
    plot_311_pie(df_311)
