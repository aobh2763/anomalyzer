from anomaly_detection.features import (
    APPLICATION_DATA_SCHEMA,
    APPLICATION_EVENT_FIELD_MAPS,
    SECURITY_DATA_SCHEMA,
    SECURITY_EVENT_FIELD_MAPS,
    SYSTEM_DATA_SCHEMA,
    SYSTEM_EVENT_FIELD_MAPS,
)


def extract_application_data_features(application_data_record):
    application_data_attributes = dict.fromkeys(APPLICATION_DATA_SCHEMA)

    field_map = APPLICATION_EVENT_FIELD_MAPS.get(application_data_record["EventID"], {})

    for original_field, unified_field in field_map.items():
        application_data_attributes[unified_field] = application_data_record.get(
            original_field
        )

    return application_data_attributes


def extract_security_data_features(security_data_record):
    security_data_attributes = dict.fromkeys(SECURITY_DATA_SCHEMA)

    field_map = SECURITY_EVENT_FIELD_MAPS.get(security_data_record["EventID"], {})

    for original_field, unified_field in field_map.items():
        security_data_attributes[unified_field] = security_data_record.get(
            original_field
        )

    return security_data_attributes


def extract_system_data_features(system_data_record):
    system_data_attributes = dict.fromkeys(SYSTEM_DATA_SCHEMA)

    field_map = SYSTEM_EVENT_FIELD_MAPS.get(system_data_record["EventID"], {})

    for original_field, unified_field in field_map.items():
        system_data_attributes[unified_field] = system_data_record.get(original_field)

    return system_data_attributes
