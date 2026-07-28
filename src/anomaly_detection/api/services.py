import pandas as pd
import numpy as np
import dill

from pathlib import Path
from sqlalchemy import delete
from sqlmodel import Session, select
from anomaly_detection.api.db import get_session
from anomaly_detection.parser.data_parsers import *
from anomaly_detection.api.models import Evaluation, EventResult
from anomaly_detection.utils.extract_shared_features import extract_specific_events

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_DIR / "storage/logs"
FEATURES_DIR = PROJECT_DIR / "storage/features"
TRANSFORMERS_DIR = PROJECT_DIR / "storage/transformers"
RESULTS_DIR = PROJECT_DIR / "storage/results"


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


def update_decision_boundary(evaluation_id, decision_boundary, session: Session):
    session.exec(delete(EventResult).where(EventResult.evaluation_id == evaluation_id))
    session.commit()

    evaluation_filename = f"{evaluation_id}.csv"

    evaluation = session.get(Evaluation, evaluation_id)
    assert evaluation is not None

    log_filename = f"{evaluation.log_id}.evtx"

    results_df = pd.read_csv(RESULTS_DIR / evaluation_filename)

    anomalies = results_df[results_df["anomaly_score"] <= decision_boundary]

    anomalies_records = anomalies["event_record_id"].tolist()

    results = extract_specific_events(anomalies_records, LOGS_DIR / log_filename)

    for result in results:
        event_record_id = result["data"]["System"]["EventRecordID"]

        event_result = EventResult(
            event_record_id=event_record_id,
            evaluation_id=evaluation_id,
            timestamp=result["timestamp"],
            event_id=result["data"]["System"]["EventID"],
            anomaly_score=results_df[
                results_df["event_record_id"] == int(event_record_id)
            ]["anomaly_score"].iloc[0],
        )

        event_result.raw_fields = result["data"]

        session.add(event_result)

    session.commit()

    return len(anomalies_records)


def delete_evaluation(evaluation_id, session: Session):
    evaluation = session.get(Evaluation, evaluation_id)
    assert evaluation is not None

    evaluation_filename = f"{evaluation_id}.csv"
    (RESULTS_DIR / evaluation_filename).unlink(missing_ok=True)

    session.exec(delete(EventResult).where(EventResult.evaluation_id == evaluation_id))
    session.delete(evaluation)
    session.commit()
