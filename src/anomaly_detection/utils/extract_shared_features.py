import pandas as pd
import numpy as np

from anomaly_detection.features.shared_field_maps import (
    TIME_ATTRIBUTES_SCHEMA,
    PROFILE_ATTRIBUTES_FIELD_MAPS,
    PROFILE_ATTRIBUTES_SCHEMA,
)


def encode_cyclic(value, periodicity):
    """Encode value using cyclic encoding for a specific period.

    Args:
        value (int): Value to encode.
        periodicity (int): Periodicity of encoding.

    Returns:
        tuple[float, float]: The encoded pair of values.
    """
    return (
        np.sin(2 * np.pi * value / periodicity),
        np.cos(2 * np.pi * value / periodicity),
    )


def extract_time_features(timestamp_record):
    """Extract time features from a given timestamp string.

    Args:
        timestamp_record (str): Timestamp string.

    Returns:
        TIME_ATTRIBUTES_SCHEMA: Extracted time features except deltatime.
    """
    timestamp = pd.Timestamp(timestamp_record)

    time_attributes = dict.fromkeys(TIME_ATTRIBUTES_SCHEMA)

    time_attributes["second_sin"], time_attributes["second_cos"] = encode_cyclic(
        timestamp.second, 60
    )

    time_attributes["minute_sin"], time_attributes["minute_cos"] = encode_cyclic(
        timestamp.minute, 60
    )

    time_attributes["hour_sin"], time_attributes["hour_cos"] = encode_cyclic(
        timestamp.hour, 24
    )

    time_attributes["day_sin"], time_attributes["day_cos"] = encode_cyclic(
        timestamp.day, 7
    )

    time_attributes["month_sin"], time_attributes["month_cos"] = encode_cyclic(
        timestamp.month, 12
    )

    time_attributes["year"] = timestamp.year

    return time_attributes


def extract_profile_features(system_record):
    system_attributes = dict.fromkeys(PROFILE_ATTRIBUTES_SCHEMA)

    for original_field, unified_field in PROFILE_ATTRIBUTES_FIELD_MAPS.items():
        system_attributes[unified_field] = system_record.get(original_field)

    return system_attributes
