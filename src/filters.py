from datetime import date

import pandas as pd
import streamlit as st

from .config import STATUS_OPTIONS
from .constants import ServiceRequestsColumns, UNKNOWN_VALUE

def sidebar_filters(df: pd.DataFrame, min_date: date, max_date: date) -> pd.DataFrame:
    # -- Header --
    st.sidebar.header('🔍 Filters')

    # -- Date range filter --
    dates = st.sidebar.date_input(
        'Date range',
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    try:
        selected_start, selected_end = dates
    except ValueError:
        # If only one date is selected, use it for both start and end
        if len(dates) == 1:
            selected_start = selected_end = dates[0]
        # If no date is selected, fall back to the full available range
        else:
            selected_start, selected_end = min_date, max_date

    # -- Status filter --
    status_choice = st.sidebar.radio('Request status', STATUS_OPTIONS)

    # -- Local area filter --
    areas = sorted(df[ServiceRequestsColumns.LOCAL_AREA].dropna().unique())

    # Add unknown value at the end
    if UNKNOWN_VALUE in areas:
        areas.remove(UNKNOWN_VALUE)
        areas.append(UNKNOWN_VALUE)
    
    selected_areas = st.sidebar.multiselect(
        'Local areas',
        options=areas,
        default=areas
    )

    # -- Apply filters --
    df_filtered = df.copy()

    df_filtered = df_filtered[
        (df_filtered[ServiceRequestsColumns.OPEN_TIMESTAMP].dt.date >= selected_start) &
        (df_filtered[ServiceRequestsColumns.OPEN_TIMESTAMP].dt.date <= selected_end)
    ]

    if status_choice != 'All':
        df_filtered = df_filtered[df_filtered[ServiceRequestsColumns.STATUS] == status_choice]
    
    if selected_areas:
        df_filtered = df_filtered[df_filtered[ServiceRequestsColumns.LOCAL_AREA].isin(selected_areas)]

    return df_filtered