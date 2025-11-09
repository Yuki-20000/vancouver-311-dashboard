import pandas as pd
import streamlit as st

from .config import CACHE_EXPIRY_SECONDS
from .constants import (
    ServiceRequestsColumns,
    KPI_TOTAL_KEY,
    KPI_OPEN_KEY,
    KPI_CLOSED_KEY,
    KPI_TOP_AREA_KEY,
    OPEN_STATUS,
    CLOSED_STATUS,
    UNKNOWN_VALUE
)

@st.cache_data(ttl=CACHE_EXPIRY_SECONDS)
def compute_kpis(df: pd.DataFrame) -> dict:
    # Get the counts for each status
    status_counts = df[ServiceRequestsColumns.STATUS].value_counts()

    # Get the area with the most requests (excluding unknown value)
    valid_areas = df[df[ServiceRequestsColumns.LOCAL_AREA] != UNKNOWN_VALUE][ServiceRequestsColumns.LOCAL_AREA]

    if not valid_areas.empty:
        top_area = valid_areas.value_counts().idxmax()
    else:
        top_area = 'N/A'

    kpi_dict = {
        KPI_TOTAL_KEY: len(df),
        KPI_OPEN_KEY: status_counts.get(OPEN_STATUS, 0),
        KPI_CLOSED_KEY: status_counts.get(CLOSED_STATUS, 0),
        KPI_TOP_AREA_KEY: top_area
    }

    return kpi_dict