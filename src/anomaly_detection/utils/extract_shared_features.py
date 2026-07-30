import pandas as pd
import numpy as np
import xmltodict
import re

from datetime import datetime
from evtx import PyEvtxParser
from anomaly_detection.features import (
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
        timestamp.dayofweek, 7
    )

    time_attributes["month_sin"], time_attributes["month_cos"] = encode_cyclic(
        timestamp.month, 12
    )

    return time_attributes


def extract_profile_features(system_record):
    system_attributes = dict.fromkeys(PROFILE_ATTRIBUTES_SCHEMA)

    for original_field, unified_field in PROFILE_ATTRIBUTES_FIELD_MAPS.items():
        system_attributes[unified_field] = system_record.get(original_field)

    return system_attributes


def transform_eventdata(event):
    event_data = event.get("Event", {}).get("EventData")

    if not event_data:
        return event

    data = event_data.get("Data")

    if data is None:
        return event

    # Normalize to a list
    if isinstance(data, dict):
        data = [data]
    elif isinstance(data, str):
        data = [{"#text": data}]
    elif not isinstance(data, list):
        return event

    transformed = {}

    for item in data:
        if not isinstance(item, dict):
            continue

        name = item.get("@Name")
        if not name:
            continue

        transformed[name] = item.get("#text")

    event["Event"]["EventData"] = transformed

    return event


event_record_re = re.compile(r"<EventRecordID>(\d+)</EventRecordID>")


def extract_specific_events(record_ids, path):
    wanted = {int(x) for x in record_ids}
    results = []

    parser = PyEvtxParser(path)

    for record in parser.records():
        if record is None:
            continue

        match = event_record_re.search(record["data"])

        if not match:
            continue

        event_record_id = int(match.group(1))

        if event_record_id not in wanted:
            continue

        event = transform_eventdata(xmltodict.parse(record["data"]))["Event"]

        # Normalize EventID
        event_id = event["System"]["EventID"]

        if isinstance(event_id, dict):
            event["System"]["EventID"] = int(event_id["#text"])
        else:
            event["System"]["EventID"] = int(event_id)

        results.append(
            {
                "timestamp": datetime.fromisoformat(
                    record["timestamp"].replace("Z UTC", "+00:00")
                ),
                "data": event,
            }
        )

        if len(results) == len(wanted):
            break

    return results
