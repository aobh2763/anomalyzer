import pandas as pd

from anomaly_detection.etl.load import load_records
from anomaly_detection.parser.data_parsers import *
from anomaly_detection.api.models import LogType
from anomaly_detection.api.services.paths import LOGS_DIR, FEATURES_DIR


def determine_log_type(log_id):
    input_filename = f"{log_id}.evtx"
    evtx_path = LOGS_DIR / input_filename

    records = load_records(evtx_path)

    match records[0]["System"]["Channel"]:
        case "System":
            return LogType.SYSTEM
        case "Application":
            return LogType.APPLICATION
        case "Security":
            return LogType.SECURITY
        case _:
            return LogType.UNKNOWN


def _extract_features(log_id, parser_fn):
    input_filename = f"{log_id}.evtx"
    evtx_path = LOGS_DIR / input_filename

    records = parser_fn(evtx_path)

    flat_records = [
        {**record["timestamp"], **record["profile"], **record["data"]}
        for record in records
    ]

    features_df = pd.DataFrame(flat_records)

    output_filename = f"{log_id}.csv"
    features_df.to_csv(FEATURES_DIR / output_filename)

    return features_df.columns.values.tolist()


def extract_system_features(log_id):
    return _extract_features(log_id, parse_system)


def extract_application_features(log_id):
    return _extract_features(log_id, parse_application)


def extract_security_features(log_id):
    return _extract_features(log_id, parse_security)
