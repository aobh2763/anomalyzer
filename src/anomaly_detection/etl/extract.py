import json
from evtx import PyEvtxParser


def extract_timestamps(path):
    """Uses PyEvtxParser to parse and extract the timestamps of all events from a given Windows Event Log (.evtx) file.

    Args:
        path (Path): The path to the Windows Event Log (.evtx) file.

    Returns:
        list[str]: List of timestamps in the given Windows Event Log (.evtx) file.
    """
    parser = PyEvtxParser(path)

    timestamps = [
        record["timestamp"] for record in parser.records() if record is not None
    ]

    return timestamps


def extract_data(path):
    """Uses PyEvtxParser to parse and extract the data of all events from a given Windows Event Log (.evtx) file.

    Args:
        path (Path): The path to the Windows Event Log (.evtx) file.

    Returns:
        list[dict]: List of event data in the given Windows Event Log (.evtx) file.
    """
    parser = PyEvtxParser(path)

    records = [
        json.loads(record["data"])["Event"]
        for record in parser.records_json()
        if record is not None
    ]

    return records
