import pandas as pd

complex_system_fields = ["Provider", "TimeCreated", "Correlation", "Execution"]


def flatten_record(record, complex_fields, origin=None):
    """Gets rid of the unnecessary "#attributes" keys in a Windows Event Log dictionary

    Args:
        record (dict): The unflattened Windows Event Log record.
        complex_fields (_type_): The fields containing the "#attributes" key.
        origin (str, optional): The concerned field in the Windows Event Log, can be "System" or "EventData". Can be None for root. Defaults to None.

    Raises:
        TypeError: If origin is not "System" or "EventData".

    Returns:
        dict: The flattened Windows Event Log record.
    """
    if origin not in ["System", "EventData", None]:
        raise TypeError("origin must be 'System' or 'EventData'.")

    if origin is not None:
        system = record[origin]
    else:
        system = record

    for key in complex_fields:
        value = system.get(key)
        if value:
            system[key] = value["#attributes"]

    return record


def flatten_dataframe(df, complex_columns):
    """Flatten complex dict columns in a given DataFrame into multiple columns, deleting the original complex ones.

    Args:
        df (DataFrame): The DataFrame containing complex dict columns.
        complex_columns (_type_): The columns to flatten.

    Returns:
        DataFrame: The DataFrame with flattened columns.
    """
    for column in complex_columns:
        # Extract complex objects
        complex_df = df[column].apply(pd.Series)

        # Reinsert them into the dataframe
        df = df.join(complex_df.add_prefix(column))

    # Drop the complex columns
    df.drop(columns=complex_columns, inplace=True)

    return df


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


def transform_system(records):
    """Transform event records into a pandas DataFrame.

    Args:
        records (list[dict]): List of extracted data.

    Returns:
        DataFrame: The created system records DataFrame.
    """
    records_clean = [
        flatten_record(record, complex_system_fields, origin="System")
        for record in records
    ]

    system_records = [record["System"] for record in records_clean]

    system_df = pd.DataFrame(system_records)

    system_df = flatten_dataframe(system_df, complex_system_fields)

    return system_df
