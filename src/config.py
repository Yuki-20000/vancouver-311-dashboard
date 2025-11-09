# -- Common settings --
# Timezone
TIMEZONE = 'America/Vancouver'

# Number of past months to fetch data for
PAST_MONTHS = 3

# API cache expiry time in seconds (3600s = 1 hour)
CACHE_EXPIRY_SECONDS = 3600

# Time period for time series aggregation
TIME_PERIOD = 'W-SAT'  # week ending Saturday (week starts on Sunday)

# -- API settings --
# 3-1-1 service requests URL
VANCOUVER_311_URL = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/3-1-1-service-requests/exports/json'

# Local area boundary URL
VANCOUVER_LOCAL_AREA_URL = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/local-area-boundary/exports/geojson'

# Default parameters for APIs
DEFAULT_LIMIT = -1
DEFAULT_USE_LABELS = 'false'
DEFAULT_COMPRESSED = 'false'
DEFAULT_EPSG = 4326

# Default parameters for 3-1-1 service requests
DEFAULT_ORDER_BY_311 = 'service_request_open_timestamp'

# -- Filter settings --
# Status options for radio buttons
STATUS_OPTIONS = ['All', 'Open', 'Close']

# -- Chart settings --
# Common chart settings
CHART_HEIGHT = 400
TOOLTIP_TITLE_COUNT = 'Count'

# Map chart settings
VANCOUVER_CENTER = (49.25, -123.12)
DEFAULT_ZOOM = 11
DEFAULT_MAP_TILE = 'cartodbpositron'

CHOROPLETH_FILL_COLOR = 'YlOrRd'
CHOROPLETH_FILL_OPACITY = 0.7
CHOROPLETH_LINE_OPACITY = 0.4
CHOROPLETH_LEGEND_NAME = 'Request Count'

TOOLTIP_ALIASES = ['Local Area:', 'Requests:']
TOOLTIP_FORMAT_NUMBERS = True

# Line chart settings
X_TITLE_WEEKLY = 'Week'
Y_TITLE_REQUESTS = 'Number of Requests'
LEGEND_TITLE_STATUS = 'Status'
STATUS_COLOR_RED = '#d62728'
STATUS_COLOR_GREEN = '#2ca02c'
TOOLTIP_TITLE_WEEK = 'Week'
TOOLTIP_TITLE_STATUS = 'Status'

# Pie chart settings
TOP_N = 10
TOOLTIP_TITLE_SERVICE_TYPE = 'Service Type'
TOOLTIP_TITLE_PERCENTAGE = 'Percentage'