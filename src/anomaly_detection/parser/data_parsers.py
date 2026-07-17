from anomaly_detection.parser.parser_core import _parse_log
from anomaly_detection.utils.extract_event_features import (
    extract_security_data_features,
    extract_system_data_features,
    extract_application_data_features,
)
from anomaly_detection.features.application_field_maps import APPLICATION_DATA_SCHEMA
from anomaly_detection.features.security_field_maps import SECURITY_DATA_SCHEMA
from anomaly_detection.features.system_field_maps import SYSTEM_DATA_SCHEMA


def parse_security(path):
    """Parse a Security .evtx file into merged, time-sorted feature rows.

    Args:
        path (Path): Path to the Security .evtx file.

    Returns:
        list[dict]: One row per event, shaped like FULL_SECURITY_SCHEMA.
    """
    return _parse_log(path, extract_security_data_features, SECURITY_DATA_SCHEMA)


def parse_system(path):
    """Parse a System .evtx file into merged, time-sorted feature rows.

    Args:
        path (Path): Path to the System .evtx file.

    Returns:
        list[dict]: One row per event, shaped like FULL_SYSTEM_SCHEMA.
    """
    return _parse_log(path, extract_system_data_features, SYSTEM_DATA_SCHEMA)


def parse_application(path):
    """Parse an Application .evtx file into merged, time-sorted feature rows.

    Args:
        path (Path): Path to the Application .evtx file.

    Returns:
        list[dict]: One row per event, shaped like FULL_APPLICATION_SCHEMA.
    """
    return _parse_log(path, extract_application_data_features, APPLICATION_DATA_SCHEMA)
