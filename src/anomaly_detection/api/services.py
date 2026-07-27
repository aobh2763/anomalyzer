import pandas as pd
import numpy as np
import dill

from pathlib import Path
from anomaly_detection.parser.data_parsers import *

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_DIR / "storage/logs"
FEATURES_DIR = PROJECT_DIR / "storage/features"
TRANSFORMERS_DIR = PROJECT_DIR / "storage/transformers"


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


def evaluate_system(log_id, model):
    input_filename = f"{log_id}.csv"
    features_path = FEATURES_DIR / input_filename

    features_df = pd.read_csv(features_path)
    features_df["deltatime"] = pd.to_timedelta(features_df["deltatime"])

    with open(TRANSFORMERS_DIR / "system_transformer.pkl", "rb") as f:
        system_transformer = dill.load(f)

    X = system_transformer.transform(features_df)

    X = np.nan_to_num(X)  # type: ignore

    scores = model.decision_function(X)

    return pd.DataFrame(
        {
            "event_record_id": features_df["event_record_id"],
            "anomaly_score": scores,
        }
    )


def evaluate_application(log_id, model):
    input_filename = f"{log_id}.csv"
    features_path = FEATURES_DIR / input_filename

    features_df = pd.read_csv(features_path)
    features_df["deltatime"] = pd.to_timedelta(features_df["deltatime"])

    with open(TRANSFORMERS_DIR / "application_transformer.pkl", "rb") as f:
        application_transformer = dill.load(f)

    X = application_transformer.transform(features_df)

    X = np.nan_to_num(X)  # type: ignore

    scores = model.decision_function(X)

    return pd.DataFrame(
        {
            "event_record_id": features_df["event_record_id"],
            "anomaly_score": scores,
        }
    )


def evaluate_security(log_id, model):
    input_filename = f"{log_id}.csv"
    features_path = FEATURES_DIR / input_filename

    features_df = pd.read_csv(features_path)
    features_df["deltatime"] = pd.to_timedelta(features_df["deltatime"])

    with open(TRANSFORMERS_DIR / "security_transformer.pkl", "rb") as f:
        security_transformer = dill.load(f)

    X = security_transformer.transform(features_df)

    X = np.nan_to_num(X)  # type: ignore

    scores = model.decision_function(X)

    return pd.DataFrame(
        {
            "event_record_id": features_df["event_record_id"],
            "anomaly_score": scores,
        }
    )
