import pandas as pd


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
    timestamps_df["deltatime"] = timestamps_df["deltatime"].fillna(
        timestamps_df["deltatime"].mean()
    )

    return timestamps_df
