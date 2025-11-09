import altair as alt
import folium
from folium.features import GeoJsonTooltip
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from .config import (
    CHART_HEIGHT,
    TOOLTIP_TITLE_COUNT,
    # Map
    VANCOUVER_CENTER,
    DEFAULT_ZOOM,
    DEFAULT_MAP_TILE,
    CHOROPLETH_FILL_COLOR,
    CHOROPLETH_FILL_OPACITY,
    CHOROPLETH_LINE_OPACITY,
    CHOROPLETH_LEGEND_NAME,
    TOOLTIP_ALIASES,
    TOOLTIP_FORMAT_NUMBERS,
    # Line
    X_TITLE_WEEKLY,
    Y_TITLE_REQUESTS,
    LEGEND_TITLE_STATUS,
    STATUS_COLOR_RED,
    STATUS_COLOR_GREEN,
    TOOLTIP_TITLE_WEEK,
    TOOLTIP_TITLE_STATUS,
    # Pie
    TOP_N,
    TOOLTIP_TITLE_SERVICE_TYPE,
    TOOLTIP_TITLE_PERCENTAGE
)
from .constants import (
    ServiceRequestsColumns,
    WEEK_START_COL,
    LocalAreaColumns,
    OPEN_STATUS,
    CLOSED_STATUS,
    UNKNOWN_VALUE
    )
from .api import get_local_area_geodataframe

# Constant
_AREA_NAME_LOWER_COL = 'area_name_lower'
_COUNT_COL = 'count'
_PERCENTAGE_COL = 'percentage'

def plot_311_map(df: pd.DataFrame) -> None:
    # Check if dataframe is empty or None
    if df is None or df.empty:
        st.warning('No data available for the map.')
        return

    # Get local area boundary data
    gdf_local_area = get_local_area_geodataframe()

    if gdf_local_area is None:
        st.error('Failed to obtain local area data')
        st.stop()

    # Copy dataframes
    df_for_map = df.copy()
    gdf_local_area_for_map = gdf_local_area.copy()

    # Clean strings for merge
    df_for_map[_AREA_NAME_LOWER_COL] = df_for_map[ServiceRequestsColumns.LOCAL_AREA].str.strip().str.lower()
    gdf_local_area_for_map[_AREA_NAME_LOWER_COL] = gdf_local_area_for_map[LocalAreaColumns.NAME].str.strip().str.lower() 

    # Count requests per local area
    counts = df_for_map.groupby(_AREA_NAME_LOWER_COL).size().reset_index(name=_COUNT_COL)

    # Merge counts into geodataframe
    gdf_local_area_count = gdf_local_area_for_map.merge(
        counts,
        left_on=_AREA_NAME_LOWER_COL,
        right_on=_AREA_NAME_LOWER_COL,
        how='left'
    )

    gdf_local_area_count[_COUNT_COL] = gdf_local_area_count[_COUNT_COL].fillna(0).astype(int)

    # Create a Folium map
    m = folium.Map(location=VANCOUVER_CENTER, zoom_start=DEFAULT_ZOOM, tiles=DEFAULT_MAP_TILE)

    choropleth = folium.Choropleth(
        geo_data=gdf_local_area_count,
        data=gdf_local_area_count,
        columns=[_AREA_NAME_LOWER_COL, _COUNT_COL],
        key_on=f'feature.properties.{_AREA_NAME_LOWER_COL}',
        fill_color=CHOROPLETH_FILL_COLOR,
        fill_opacity=CHOROPLETH_FILL_OPACITY,
        line_opacity=CHOROPLETH_LINE_OPACITY,
        legend_name=CHOROPLETH_LEGEND_NAME
    ).add_to(m)

    tooltip = GeoJsonTooltip(
        fields=[LocalAreaColumns.NAME, _COUNT_COL],
        aliases=TOOLTIP_ALIASES,
        localize=TOOLTIP_FORMAT_NUMBERS
    )
    choropleth.geojson.add_child(tooltip)

    st_folium(m, height=CHART_HEIGHT)

def plot_311_line(df: pd.DataFrame) -> None:
    # Check if dataframe is empty or None
    if df is None or df.empty:
        st.warning('No data available for the line chart.')
        return

    df_for_line = df.copy()

    df_for_line = df_for_line.dropna(subset=[ServiceRequestsColumns.OPEN_TIMESTAMP])

    # Check if dataframe is empty after dropna
    if df_for_line.empty:
        st.warning('No valid timestamp data available for the line chart.')
        return
    
    # Count requests per week and status
    weekly_counts = df_for_line.groupby([WEEK_START_COL, ServiceRequestsColumns.STATUS]).size().reset_index(name=_COUNT_COL)

    # Create all week x status combinations
    all_weeks = pd.date_range(
        weekly_counts[WEEK_START_COL].min(),
        weekly_counts[WEEK_START_COL].max(),
        freq='7D'
    )
    all_status = weekly_counts[ServiceRequestsColumns.STATUS].unique()
    weekly_counts_all = pd.DataFrame(
        [(w, s) for w in all_weeks for s in all_status],
        columns=[WEEK_START_COL, ServiceRequestsColumns.STATUS]
    )

    # Merge counts and fill missing with 0
    weekly_counts_all = weekly_counts_all.merge(
        weekly_counts,
        left_on=[WEEK_START_COL, ServiceRequestsColumns.STATUS],
        right_on=[WEEK_START_COL, ServiceRequestsColumns.STATUS],
        how='left'
    ).fillna({_COUNT_COL: 0})

    chart = alt.Chart(weekly_counts_all).mark_line(point=True).encode(
        x=alt.X(
            WEEK_START_COL,
            title=X_TITLE_WEEKLY,
            axis=alt.Axis(
                values=weekly_counts_all[WEEK_START_COL].dt.floor('D'),
                format='%m/%d'
            )
        ),
        y=alt.Y(_COUNT_COL, title=Y_TITLE_REQUESTS),
        color=alt.Color(
            ServiceRequestsColumns.STATUS,
            title=LEGEND_TITLE_STATUS,
            scale=alt.Scale(
                domain=[OPEN_STATUS, CLOSED_STATUS],
                range=[STATUS_COLOR_RED, STATUS_COLOR_GREEN]
            )
        ),
        tooltip=[
            alt.Tooltip(
                WEEK_START_COL,
                title=TOOLTIP_TITLE_WEEK,
                format='%m/%d'
            ),
            alt.Tooltip(
                ServiceRequestsColumns.STATUS,
                title=TOOLTIP_TITLE_STATUS
            ),
            alt.Tooltip(
                _COUNT_COL,
                title=TOOLTIP_TITLE_COUNT
            )
        ]
    ).properties(height=CHART_HEIGHT)

    st.altair_chart(chart, use_container_width=True)
    st.caption('Note: The line chart is based on **Open date** of requests.')

def plot_311_pie(df: pd.DataFrame) -> None:
    # Check if dataframe is empty or None
    if df is None or df.empty:
        st.warning('No data available for the pie chart.')
        return

    df_for_pie = df.copy()

    df_for_pie[ServiceRequestsColumns.SERVICE_REQUEST_TYPE] = df_for_pie[ServiceRequestsColumns.SERVICE_REQUEST_TYPE].fillna(UNKNOWN_VALUE)

    service_counts = df_for_pie[ServiceRequestsColumns.SERVICE_REQUEST_TYPE].value_counts()

    # Get top N categories
    top_counts = service_counts.nlargest(TOP_N)

    df_top_counts = pd.DataFrame({
        ServiceRequestsColumns.SERVICE_REQUEST_TYPE: top_counts.index,
        _COUNT_COL: top_counts.values
    })
    
    # Calculate percentage
    total_count = df_for_pie[ServiceRequestsColumns.SERVICE_REQUEST_TYPE].count()
    df_top_counts[_PERCENTAGE_COL] = (df_top_counts[_COUNT_COL] / total_count * 100).round(1)
    
    chart = alt.Chart(df_top_counts).mark_arc().encode(
        theta=alt.Theta(field=_COUNT_COL, type='quantitative'),
        color=alt.Color(
            field=ServiceRequestsColumns.SERVICE_REQUEST_TYPE,
            type='nominal',
            legend=None
        ),
        order=alt.Order(field=_COUNT_COL, type='quantitative', sort='descending'),
        tooltip=[
            alt.Tooltip(
                field=ServiceRequestsColumns.SERVICE_REQUEST_TYPE,
                type='nominal',
                title=TOOLTIP_TITLE_SERVICE_TYPE
            ),
            alt.Tooltip(
                field=_COUNT_COL,
                type='quantitative',
                title=TOOLTIP_TITLE_COUNT
            ),
            alt.Tooltip(
                field=_PERCENTAGE_COL,
                type='quantitative',
                title=TOOLTIP_TITLE_PERCENTAGE,
                format='.1f'
            )
        ]
    ).properties(height=CHART_HEIGHT)
    
    st.altair_chart(chart, use_container_width=True)