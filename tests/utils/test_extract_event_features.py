import pytest

from anomaly_detection.utils.extract_event_features import (
    extract_application_data_features,
    extract_security_data_features,
    extract_system_data_features,
)


def test_extract_application_data_features():
    assert extract_application_data_features(
        {
            "EventID": 4,
            "EventRecordID": 2899035,
            "PayloadSource": "EventData",
            "Binary": None,
            "Data_text": "php[8696] | PHP Warning: PHP Startup: Unable t...",
            "Context": None,
            "ObjId": None,
        }
    ) == {
        "context": "php[8696] | PHP Warning: PHP Startup: Unable t...",
        "entity": None,
    }
