import pandas as pd
import numpy as np

from pathlib import Path
from anomaly_detection.parser.data_parsers import (
    parse_system,
    parse_application,
    parse_security,
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_DIR / "storage/logs"
FEATURES_DIR = PROJECT_DIR / "storage/features"


def extract_system_features(log_id):
    input_filename = f"{log_id}.evtx"
    system_evtx_path = LOGS_DIR / input_filename

    system_records = parse_system(system_evtx_path)

    flat_system_records = [
        {**record["timestamp"], **record["profile"], **record["data"]}
        for record in system_records
    ]

    system_features_df = pd.DataFrame(flat_system_records)

    output_filename = f"{log_id}.csv"

    system_features_df.to_csv(FEATURES_DIR / output_filename)

    return system_features_df.columns.values.tolist()


def extract_application_features(log_id):
    input_filename = f"{log_id}.evtx"
    application_evtx_path = LOGS_DIR / input_filename

    application_records = parse_application(application_evtx_path)

    flat_application_records = [
        {**record["timestamp"], **record["profile"], **record["data"]}
        for record in application_records
    ]

    application_features_df = pd.DataFrame(flat_application_records)

    output_filename = f"{log_id}.csv"
    application_features_df.to_csv(FEATURES_DIR / output_filename)

    return application_features_df.columns.values.tolist()


def extract_security_features(log_id):
    input_filename = f"{log_id}.evtx"
    security_evtx_path = LOGS_DIR / input_filename

    security_records = parse_security(security_evtx_path)

    flat_security_records = [
        {**record["timestamp"], **record["profile"], **record["data"]}
        for record in security_records
    ]

    security_features_df = pd.DataFrame(flat_security_records)

    output_filename = f"{log_id}.csv"
    security_features_df.to_csv(FEATURES_DIR / output_filename)

    return security_features_df.columns.values.tolist()
