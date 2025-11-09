# Column names for 3-1-1 service requests data
class ServiceRequestsColumns:
    DEPARTMENT = 'department'
    SERVICE_REQUEST_TYPE = 'service_request_type'
    STATUS = 'status'
    CLOSURE_REASON = 'closure_reason'
    OPEN_TIMESTAMP = 'service_request_open_timestamp'
    CLOSE_DATE = 'service_request_close_date'
    LAST_MODIFIED_TIMESTAMP = 'last_modified_timestamp'
    ADDRESS = 'address'
    LOCAL_AREA = 'local_area'
    CHANNEL = 'channel'
    LATITUDE = 'latitude'
    LONGITUDE = 'longitude'
    GEOM = 'geom'

# Derived column names
WEEK_START_COL = 'week_start'

# Column names for local area boundary data
class LocalAreaColumns:
    NAME = 'name'
    GEOM_2D_POINT = 'geo_point_2d'
    GEOMETRY = 'geometry'

# KPI keys
KPI_TOTAL_KEY = 'total_requests'
KPI_OPEN_KEY = 'open_requests'
KPI_CLOSED_KEY = 'closed_requests'
KPI_TOP_AREA_KEY = 'top_area'

# Status values in 3-1-1 service requests
OPEN_STATUS = 'Open'
CLOSED_STATUS = 'Close'

# Missing data placeholder
UNKNOWN_VALUE = 'Unknown'