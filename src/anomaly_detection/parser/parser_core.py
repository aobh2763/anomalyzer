import pandas as pd

from anomaly_detection.parser.compute_features import (
    compute_deltatime,
    compute_sequence_features,
)
from anomaly_detection.etl.extract import extract_data
from anomaly_detection.etl.transform import (
    complex_system_fields,
    flatten_record,
    normalize_event_id,
    extract_payload,
    normalize_payload,
)
from anomaly_detection.utils.extract_shared_features import (
    extract_time_features,
    extract_profile_features,
)
from anomaly_detection.features.shared_field_maps import (
    TIME_ATTRIBUTES_SCHEMA,
    PROFILE_ATTRIBUTES_SCHEMA,
)

SENTINEL_TIMESTAMP = "1601-01-01T00:00:00Z"


def _nest_row(flat_row, data_schema):
    """Split a flat row dict into the {"timestamp", "profile", "data"} shape
    matching FULL_*_SCHEMA, based on which schema each key belongs to.

    Args:
        flat_row (dict): One row as built by _parse_log (all keys at the top level).
        data_schema (set[str]): The log-specific *_DATA_SCHEMA (e.g. APPLICATION_DATA_SCHEMA).

    Returns:
        dict: {"timestamp": {...}, "profile": {...}, "data": {...}}.
    """
    return {
        "timestamp": {k: flat_row[k] for k in TIME_ATTRIBUTES_SCHEMA},
        "profile": {k: flat_row[k] for k in PROFILE_ATTRIBUTES_SCHEMA},
        "data": {k: flat_row[k] for k in data_schema},
    }


def _flatten_system(system):
    """Flatten a raw System block into the flat field names extract_profile_features
    expects (EventID, Version, Correlation_ActivityID, Execution_ThreadID, EventRecordID),
    mirroring what transform_system_df()/flatten_dataframe() do for a full DataFrame,
    but for a single record.

    Args:
        system (dict): The already flatten_record()-processed "System" block --
            Provider/TimeCreated/Correlation/Execution are unwrapped dicts at this point.

    Returns:
        dict: Flat dict with EventID as a plain value and prefixed Correlation_/Execution_ keys.
    """
    event_id, qualifiers = normalize_event_id(system)

    correlation = system.get("Correlation") or {}
    execution = system.get("Execution") or {}

    flat = dict(system)
    flat["EventID"] = event_id
    flat["Qualifiers"] = qualifiers
    for key, value in correlation.items():
        flat[f"Correlation_{key}"] = value
    for key, value in execution.items():
        flat[f"Execution_{key}"] = value

    return flat


def _parse_log(path, extract_data_features, data_schema):
    """Shared core: single parser pass, time + envelope + payload features merged
    per record, sorted chronologically, then nested into {"timestamp", "profile", "data"}.
    Not called directly -- use parse_security()/parse_system()/parse_application() instead.

    Args:
        path (Path): Path to the .evtx file.
        extract_data_features (callable): One of extract_security_data_features,
            extract_system_data_features, extract_application_data_features.
        data_schema (set[str]): The log-specific *_DATA_SCHEMA, used to nest the output.

    Returns:
        list[dict]: One row per event, shaped like FULL_*_SCHEMA, deltatime included.
    """
    records = extract_data(path)

    rows = (
        []
    )  
    
    for record in records:
        record = flatten_record(record, complex_system_fields, origin="System")
        system = record.get("System", {})

        time_created = (system.get("TimeCreated") or {}).get("SystemTime")
        if time_created is None or time_created == SENTINEL_TIMESTAMP:
            continue  # same rule as load_timestamps(), applied on the same record

        parsed_ts = pd.Timestamp(time_created)
        flat_system = _flatten_system(system)

        row = {}
        row.update(extract_time_features(time_created))
        row.update(extract_profile_features(flat_system))

        raw_payload, _source = extract_payload(record)
        payload = normalize_payload(raw_payload) or {}
        payload = dict(payload)
        payload["EventID"] = flat_system["EventID"]
        row.update(extract_data_features(payload))

        rows.append((parsed_ts, row))

    rows.sort(key=lambda pair: pair[0])

    timestamps = [ts for ts, _ in rows]
    deltas = compute_deltatime(timestamps)

    flat_rows = [row for _, row in rows]
    for row, delta in zip(flat_rows, deltas):
        row["deltatime"] = delta

    compute_sequence_features(flat_rows)

    return [_nest_row(row, data_schema) for row in flat_rows]
