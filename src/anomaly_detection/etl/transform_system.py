import pandas as pd

complex_system_fields = [
    "Provider",
    "TimeCreated",
    "Correlation",
    "Execution",
    "Security",
]


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
