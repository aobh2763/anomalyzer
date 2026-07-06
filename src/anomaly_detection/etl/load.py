from anomaly_detection.etl.extract import *
from anomaly_detection.etl.transform import *


def load_timestamps(path):
    """Load timestamps from a given Windows Event Log (.evtx) file into a list of records.

    Args:
        path (Path): The path to the Windows Event Log (.evtx) file.

    Returns:
        list[dict]: The timestamps of the events.
    """
    records = extract_timestamps(path)

    return records


def load_timestamps_df(path):
    """Load timestamps from a given Windows Event Log (.evtx) file into a DataFrame.

    Args:
        path (Path): The path to the Windows Event Log (.evtx) file.

    Returns:
        DataFrame: The timestamps of the events.
    """
    records = extract_timestamps(path)

    timestamps_df = transform_timestamps(records)

    return timestamps_df


def load_data_records(path):
    """Load data records from a given Windows Event Log (.evtx) file into a list of records.

    Args:
        path (Path): The path to the Windows Event Log (.evtx) file.
        dataframe (bool, optional): Return a DataFrame or a list of dicts. Defaults to True.

    Returns:
        list[dict]: The data records of the events.
    """
    records = extract_data(path)

    records_clean = [
        flatten_record(record, complex_system_fields, origin="System")
        for record in records
    ]

    return records_clean


def load_system_records_df(path, dataframe=True):
    """Load system records from a given Windows Event Log (.evtx) file into a DataFrame.

    Args:
        path (Path): The path to the Windows Event Log (.evtx) file.

    Returns:
        DataFrame: The system records of the events.
    """
    records = extract_data(path)

    system_df = transform_system(records)

    return system_df
