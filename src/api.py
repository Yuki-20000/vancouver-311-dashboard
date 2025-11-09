import logging
from datetime import date

import geopandas as gpd
import pandas as pd
import requests
from shapely.geometry import shape
import streamlit as st

from .config import (
    TIMEZONE,
    CACHE_EXPIRY_SECONDS,
    TIME_PERIOD,
    VANCOUVER_311_URL,
    VANCOUVER_LOCAL_AREA_URL,
    DEFAULT_LIMIT,
    DEFAULT_USE_LABELS,
    DEFAULT_COMPRESSED,
    DEFAULT_EPSG,
    DEFAULT_ORDER_BY_311
)
from .constants import ServiceRequestsColumns, WEEK_START_COL, UNKNOWN_VALUE

def fetch_311_service_requests(start_date: date, end_date: date) -> dict | None:
    params = {
        'select': '*',
        'where': f"{ServiceRequestsColumns.OPEN_TIMESTAMP} >= '{start_date}' AND {ServiceRequestsColumns.OPEN_TIMESTAMP} <= '{end_date}'",
        'order_by': DEFAULT_ORDER_BY_311,
        'limit': DEFAULT_LIMIT,
        'timezone': TIMEZONE,
        'use_labels': DEFAULT_USE_LABELS,
        'compressed': DEFAULT_COMPRESSED,
        'epsg': DEFAULT_EPSG
    }

    try:
        response = requests.get(VANCOUVER_311_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f'HTTP error: {e} (status code: {e.response.status_code})')
    except requests.exceptions.ConnectionError as e:
        logging.error(f'Connection error: {e}')
    except requests.exceptions.Timeout as e:
        logging.warning(f'Timeout: {e}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Unexpected error: {e}')
        
    return None

@st.cache_data(ttl=CACHE_EXPIRY_SECONDS)
def get_311_dataframe(start_date: date, end_date: date) -> pd.DataFrame | None:
    # Fetch data from the API
    json_data = fetch_311_service_requests(start_date, end_date)

    if json_data is None:
        st.cache_data.clear()
        return None
        
    df = pd.DataFrame(json_data)

    # Drop geom column (contains unhashable dict objects)
    if ServiceRequestsColumns.GEOM in df.columns:
        df = df.drop(columns=[ServiceRequestsColumns.GEOM])
    
    # Convert date column to datetime
    if ServiceRequestsColumns.OPEN_TIMESTAMP in df.columns:
        df[ServiceRequestsColumns.OPEN_TIMESTAMP] = pd.to_datetime(
            df[ServiceRequestsColumns.OPEN_TIMESTAMP],
            utc=True,
            errors='coerce'
        )
        df[ServiceRequestsColumns.OPEN_TIMESTAMP] = df[ServiceRequestsColumns.OPEN_TIMESTAMP].dt.tz_convert(TIMEZONE)

        # Create a new column with time periods
        df[WEEK_START_COL] = (
            df[ServiceRequestsColumns.OPEN_TIMESTAMP]
            .dt.tz_localize(None)
            .dt.to_period(TIME_PERIOD)
            .dt.start_time
        )

    # Clean local_area column
    if ServiceRequestsColumns.LOCAL_AREA in df.columns:
        df[ServiceRequestsColumns.LOCAL_AREA] = df[ServiceRequestsColumns.LOCAL_AREA].fillna(UNKNOWN_VALUE)

    return df

def fetch_local_area_boundaries() -> dict | None:
    params = {
        'select': '*',
        'limit': DEFAULT_LIMIT,
        'timezone': TIMEZONE,
        'use_labels': DEFAULT_USE_LABELS,
        'compressed': DEFAULT_COMPRESSED,
        'epsg': DEFAULT_EPSG
    }

    try:
        response = requests.get(VANCOUVER_LOCAL_AREA_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f'HTTP error: {e} (status code: {e.response.status_code})')
    except requests.exceptions.ConnectionError as e:
        logging.error(f'Connection error: {e}')
    except requests.exceptions.Timeout as e:
        logging.warning(f'Timeout: {e}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Unexpected error: {e}')
        
    return None

@st.cache_data(ttl=CACHE_EXPIRY_SECONDS)
def get_local_area_geodataframe() -> gpd.GeoDataFrame | None:
    # Fetch data from the API
    geojson_data = fetch_local_area_boundaries()

    if geojson_data is None:
        st.cache_data.clear()
        return None

    features = geojson_data.get('features', [])

    # Check for empty features
    if not features:
        logging.warning('No features found in local area boundary data')
        return None

    gdf = gpd.GeoDataFrame(
        [f['properties'] for f in features],
        geometry=[shape(f['geometry']) for f in features],
        crs='EPSG:4326'
    )

    return gdf