from anomaly_detection.features.application_field_maps import APPLICATION_DATA_SCHEMA
from anomaly_detection.features.security_field_maps import SECURITY_DATA_SCHEMA
from anomaly_detection.features.system_field_maps import SYSTEM_DATA_SCHEMA

SYSTEM_ATTRIBUTES_SCHEMA = {
    "event_id",
    "previous_event_id",
    "event_id_frequency",
    "version",
    "correlation_activity_id",
    "execution_thread_id",
    "event_record_id",
}

TIME_ATTRIBUTES_SCHEMA = {
    "deltatime",
    "minute",
    "hour",
    "hour_of_day",
    "minute_of_hour",
}

FULL_APPLICATION_SCHEMA = {
    "timestamp": TIME_ATTRIBUTES_SCHEMA,
    "system": SYSTEM_ATTRIBUTES_SCHEMA,
    "data": APPLICATION_DATA_SCHEMA,
}

FULL_SECURITY_SCHEMA = {
    "timestamp": TIME_ATTRIBUTES_SCHEMA,
    "system": SYSTEM_ATTRIBUTES_SCHEMA,
    "data": SECURITY_DATA_SCHEMA,
}

FULL_SYSTEM_SCHEMA = {
    "timestamp": TIME_ATTRIBUTES_SCHEMA,
    "system": SYSTEM_ATTRIBUTES_SCHEMA,
    "data": SYSTEM_DATA_SCHEMA,
}


SYSTEM_ATTRIBUTES_FIELD_MAPS = {
    "EventID": "event_id",
    "Version": "version",
    "Correlation_ActivityID": "correlation_activity_id",
    "Execution_ThreadID": "execution_thread_id",
    "EventRecordID": "event_record_id",
}
