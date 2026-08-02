import pandas as pd
from .transform_system import normalize_event_id

payload_fields = ["EventData", "UserData"]


def extract_payload(record):
    """Return whichever of EventData/UserData is present on a record, and which field it came from.

    Args:
        record (dict): A raw "Event" record (System + payload intact).

    Returns:
        tuple[dict | list | None, str | None]: (payload, source_field_name).
            source_field_name is "EventData", "UserData", or None if neither is present.
    """
    for field in payload_fields:
        value = record.get(field)
        if value:
            return value, field
    return None, None


def normalize_payload(payload):
    """Collapse unnamed <Data> elements (seen in legacy/non-manifest providers like PHP, IIS, Service Control Manager) into a flat "Data_text" string, so they don't break DataFrame profiling (.nunique(), .value_counts() fail on list-valued cells).

    Named-parameter payloads (e.g. Security log fields) have no "Data" key and pass through unchanged.

    Args:
        payload: Raw EventData/UserData payload.

    Returns:
        dict: Payload with any "Data" key replaced by "Data_text".
    """
    if not isinstance(payload, dict) or "Data" not in payload:
        return payload

    payload = dict(payload)
    raw_data = payload.pop("Data")

    if isinstance(raw_data, dict):
        raw_data = raw_data.get("#text", raw_data)

    if isinstance(raw_data, list):
        payload["Data_text"] = " | ".join(str(item) for item in raw_data)
    elif raw_data is not None:
        payload["Data_text"] = str(raw_data)

    return payload


def transform_eventdata(records):
    """Group event records by EventID and flatten each group's payload (EventData or UserData) into its own DataFrame.

    Handles real-world edge cases seen across Application/Security/System logs:
    - Provider uses UserData instead of EventData (common outside Security log)
    - Some EventIDs have no payload at all
    - Unnamed <Data> elements (legacy providers e.g. PHP, SCM), collapsed to "Data_text"
      via normalize_payload instead of breaking json_normalize

    Args:
        records (list[dict]): List of extracted "Event" records (System + payload intact).

    Returns:
        dict[int, DataFrame]: Mapping of EventID -> flattened payload DataFrame for that
            EventID. Each DataFrame also carries EventRecordID, TimeCreated and
            PayloadSource ("EventData"/"UserData"/None) for reference and later joining.
    """
    rows = []
    for record in records:
        system = record.get("System", {})
        event_id, _ = normalize_event_id(system)
        payload, source = extract_payload(record)
        payload = normalize_payload(payload)

        rows.append(
            {
                "EventID": event_id,
                "EventRecordID": system.get("EventRecordID"),
                "TimeCreated": system.get("TimeCreated")
                .get("#attributes")
                .get("SystemTime"),
                "PayloadSource": source,
                "Payload": payload,
            }
        )

    df = pd.DataFrame(rows)
    if "EventID" in df.columns:
        df["EventID"] = pd.to_numeric(df["EventID"], errors="coerce").astype("Int64")

    grouped = {}
    for eid, group in df.groupby("EventID"):
        payload_col = group["Payload"]

        if payload_col.dropna().empty:
            grouped[eid] = group.drop(columns=["Payload"])
            continue

        expanded = pd.json_normalize(payload_col)  # type: ignore
        expanded.index = group.index
        grouped[eid] = pd.concat([group.drop(columns=["Payload"]), expanded], axis=1)

    return grouped


def transform_eventdata_df(records):
    """Group event records by EventID, flatten each group's payload, then concatenate everything back into a single DataFrame.

    Args:
        records (list[dict]): List of extracted "Event" records (System + payload intact).

    Returns:
        DataFrame: One row per event, EventID + EventRecordID + TimeCreated + PayloadSource
            plus the union of all payload fields across every EventID present.
    """
    grouped = transform_eventdata(records)

    if not grouped:
        return pd.DataFrame()

    return pd.concat(grouped.values(), axis=0, ignore_index=True, sort=False)
