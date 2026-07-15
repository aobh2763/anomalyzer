import pytest
import numpy as np

from anomaly_detection.utils.extract_shared_features import (
    encode_cyclic,
    extract_time_features,
    extract_profile_features,
)


def test_extract_time_features():
    assert extract_time_features("2026-06-12 10:56:03.411997900+00:00") == {
        "deltatime": None,
        "second_sin": encode_cyclic(3, 60)[0],
        "second_cos": encode_cyclic(3, 60)[1],
        "minute_sin": encode_cyclic(56, 60)[0],
        "minute_cos": encode_cyclic(56, 60)[1],
        "hour_sin": encode_cyclic(10, 24)[0],
        "hour_cos": encode_cyclic(10, 24)[1],
        "day_sin": encode_cyclic(12, 7)[0],
        "day_cos": encode_cyclic(12, 7)[1],
        "month_sin": encode_cyclic(6, 12)[0],
        "month_cos": encode_cyclic(6, 12)[1],
        "year": 2026,
    }

    assert extract_time_features("2026-06-14 23:24:00.758247168+00:00") == {
        "deltatime": None,
        "second_sin": encode_cyclic(0, 60)[0],
        "second_cos": encode_cyclic(0, 60)[1],
        "minute_sin": encode_cyclic(24, 60)[0],
        "minute_cos": encode_cyclic(24, 60)[1],
        "hour_sin": encode_cyclic(23, 24)[0],
        "hour_cos": encode_cyclic(23, 24)[1],
        "day_sin": encode_cyclic(14, 7)[0],
        "day_cos": encode_cyclic(14, 7)[1],
        "month_sin": encode_cyclic(6, 12)[0],
        "month_cos": encode_cyclic(6, 12)[1],
        "year": 2026,
    }


def test_extract_system_features():
    assert extract_profile_features(
        {
            "EventID": 4624,
            "Version": 2,
            "Level": 0,
            "Task": 12544,
            "Opcode": 0,
            "Keywords": "0x8020000000000000",
            "EventRecordID": 34978816,
            "Channel": "Security",
            "Computer": "ESANTE.carte.com.tn",
            "Provider_Name": "Microsoft-Windows-Security-Auditing",
            "Provider_Guid": "54849625-5478-4994-A5BA-3E3B0328C30D",
            "TimeCreated_SystemTime": "2026-06-17T00:15:07.799161Z",
            "Correlation_ActivityID": "F1DAB952-E970-0004-5DB9-DAF170E9DC01",
            "Execution_ProcessID": 940,
            "Execution_ThreadID": 5960,
        }
    ) == {
        "event_id": 4624,
        "previous_event_id": None,
        "event_id_frequency": None,
        "version": 2,
        "correlation_activity_id": "F1DAB952-E970-0004-5DB9-DAF170E9DC01",
        "execution_thread_id": 5960,
        "event_record_id": 34978816,
    }
