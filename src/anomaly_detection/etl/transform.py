import pandas as pd

complex_system_fields = [
    "Provider",
    "TimeCreated",
    "Correlation",
    "Execution",
    "Security",
]

payload_fields = ["EventData", "UserData"]


def flatten_record(record, complex_fields, origin=None):
    """Gets rid of the unnecessary "#attributes" keys in a Windows Event Log dictionary

    Args:
        record (dict): The unflattened Windows Event Log record.
        complex_fields (list[str]): The fields containing the "#attributes" key.
        origin (str, optional): The concerned field in the Windows Event Log, can be "System" or "EventData". Can be None for root. Defaults to None.

    Raises:
        TypeError: If origin is not "System" or "EventData".

    Returns:
        dict: The flattened Windows Event Log record.
    """
    if origin not in ["System", "EventData", None]:
        raise TypeError("origin must be 'System' or 'EventData'.")

    if origin is not None:
        system = record.get(origin)
        if system is None:
            return record
    else:
        system = record

    for key in complex_fields:
        value = system.get(key)
        if value:
            system[key] = value.get("#attributes", value)

    return record


def flatten_dataframe(df, complex_columns):
    """Flatten complex dict columns in a given DataFrame into multiple columns, deleting the original complex ones.

    Silently skips any column not present in df, since not every log type/EventID populates every complex field.

    Args:
        df (DataFrame): The DataFrame containing complex dict columns.
        complex_columns (list[str]): The columns to flatten.

    Returns:
        DataFrame: The DataFrame with flattened columns.
    """
    present_columns = [col for col in complex_columns if col in df.columns]

    for column in present_columns:
        complex_df = (
            df[column]
            .apply(lambda v: v if isinstance(v, dict) else {})
            .apply(pd.Series)
        )
        df = df.join(complex_df.add_prefix(f"{column}_"))

    df.drop(columns=present_columns, inplace=True)

    return df


def normalize_event_id(system_dict):
    """Return a plain EventID value, handling the {"#attributes": {"Qualifiers": ...}, "#text": ...} shape some providers (mostly System/Application log) use instead of a plain int.

    Args:
        system_dict (dict): The "System" block of an event record.

    Returns:
        tuple[int | None, int | None]: (EventID, Qualifiers). Qualifiers is None when
            EventID was a plain value.
    """
    event_id = system_dict.get("EventID")
    if isinstance(event_id, dict):
        qualifiers = event_id.get("#attributes", {}).get("Qualifiers")
        return event_id.get("#text"), qualifiers
    return event_id, None


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


def transform_timestamps(timestamps, minute=True, hour=True):
    """Transform timestamp records into a pandas DataFrame.

    Args:
        timestamps (list[dict]): List of extracted timestamps.
        minute (bool, optional): Add information about minutes to DataFrame. Defaults to True.
        hour (bool, optional): Add information about hours to DataFrame. Defaults to True.

    Returns:
        DataFrame: The created timestamps DataFrame.
    """
    # Remove null timestamps and clean for transforming to a DataFrame
    cleaned = [
        timestamp.replace(" UTC", "")
        for timestamp in timestamps
        if timestamp != "1601-01-01T00:00:00Z UTC"
    ]

    timestamps_index = pd.to_datetime(cleaned, format="ISO8601", utc=True)

    timestamps_df = pd.DataFrame({"timestamp": timestamps_index})
    timestamps_df = timestamps_df.sort_values("timestamp").reset_index(drop=True)

    if minute:
        timestamps_df["minute"] = timestamps_df["timestamp"].dt.floor("min")
        timestamps_df["minute_of_hour"] = timestamps_df["timestamp"].dt.minute

    if hour:
        timestamps_df["hour"] = timestamps_df["timestamp"].dt.floor("h")
        timestamps_df["hour_of_day"] = timestamps_df["timestamp"].dt.hour

    # Add a deltatime column
    timestamps_df["deltatime"] = timestamps_df["timestamp"].diff()

    return timestamps_df


def transform_system_df(records):
    """Transform the System block of event records into a flat DataFrame.

    Works for Application, Security or System log records alike.

    Args:
        records (list[dict]): List of extracted "Event" records (System + payload intact).

    Returns:
        DataFrame: One row per event, System fields only, flattened. EventID is
            normalized to a plain nullable integer column; a "Qualifiers" column
            is added when any record carried a Qualifiers-wrapped EventID.
    """
    records_clean = [
        flatten_record(record, complex_system_fields, origin="System")
        for record in records
    ]

    system_records = [record["System"] for record in records_clean]

    system_df = pd.DataFrame(system_records)

    if "EventID" in system_df.columns:
        normalized = system_df["EventID"].apply(
            lambda v: normalize_event_id({"EventID": v})
        )
        system_df["EventID"] = normalized.apply(lambda t: t[0])
        qualifiers = normalized.apply(lambda t: t[1])
        if qualifiers.notna().any():
            system_df["Qualifiers"] = qualifiers
        system_df["EventID"] = pd.to_numeric(
            system_df["EventID"], errors="coerce"
        ).astype("Int64")

    system_df = flatten_dataframe(system_df, complex_system_fields)

    return system_df


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
                "TimeCreated": system.get("TimeCreated"),
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
