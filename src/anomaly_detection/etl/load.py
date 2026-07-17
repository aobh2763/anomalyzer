from anomaly_detection.etl.extract import extract_timestamps, extract_data
from anomaly_detection.etl.transform import (
    complex_system_fields,
    flatten_record,
    transform_timestamps,
    transform_system_df,
    transform_eventdata,
    transform_eventdata_df,
)


def load_timestamps(path):
    """Load timestamps from a given Windows Event Log (.evtx) file into a list.

    Args:
        path (Path): The path to the Windows Event Log (.evtx) file.

    Returns:
        list[str]: The timestamps of the events.
    """
    timestamps = extract_timestamps(path)

    cleaned = [timestamp.replace(" UTC", "") for timestamp in timestamps]

    return cleaned


def load_timestamps_df(path):
    """Load timestamps from a given Windows Event Log (.evtx) file into a DataFrame.

    Args:
        path (Path): The path to the Windows Event Log (.evtx) file.

    Returns:
        DataFrame: The timestamps of the events.
    """
    records = extract_timestamps(path)

    return transform_timestamps(records)


def load_records(path):
    """Load raw event records from a given Windows Event Log (.evtx) file, with the System block flattened. Payload (EventData/UserData) is left untouched.

    Works for Application, Security or System log files alike.

    Args:
        path (Path): The path to the Windows Event Log (.evtx) file.

    Returns:
        list[dict]: The event records, System complex fields flattened.
    """
    records = extract_data(path)

    return [
        flatten_record(record, complex_system_fields, origin="System")
        for record in records
    ]


def load_system_df(path):
    """Load the System block of every event in a .evtx file into a flat DataFrame.

    Works for Application, Security or System log files alike.

    Args:
        path (Path): The path to the Windows Event Log (.evtx) file.

    Returns:
        DataFrame: The system records of the events.
    """
    records = extract_data(path)

    return transform_system_df(records)


def load_eventdata(path):
    """Load the payload (EventData or UserData) of every event in a .evtx file,
    grouped by EventID.

    Works for Application, Security or System log files alike, and transparently
    handles events that use UserData instead of EventData.

    Args:
        path (Path): The path to the Windows Event Log (.evtx) file.

    Returns:
        dict[int, DataFrame]: Mapping of EventID -> DataFrame of that EventID's payload fields.
    """
    records = extract_data(path)

    return transform_eventdata(records)


def load_eventdata_df(path):
    """Load the payload (EventData or UserData) of every event in a .evtx file into a single, wide DataFrame spanning all EventIDs present.

    Args:
        path (Path): The path to the Windows Event Log (.evtx) file.

    Returns:
        DataFrame: All events with their payload fields flattened, EventID as a column.
    """
    records = extract_data(path)

    return transform_eventdata_df(records)
