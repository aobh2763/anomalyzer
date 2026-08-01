import dill
import pandas as pd
import numpy as np

from sqlalchemy import delete
from sqlmodel import Session

from anomaly_detection.api.models import Evaluation, EventResult
from anomaly_detection.utils.extract_shared_features import extract_specific_events
from anomaly_detection.api.services.paths import (
    LOGS_DIR,
    FEATURES_DIR,
    TRANSFORMERS_DIR,
    RESULTS_DIR,
)


def _evaluate(log_id, model, transformer_filename):
    input_filename = f"{log_id}.csv"
    features_path = FEATURES_DIR / input_filename

    features_df = pd.read_csv(features_path)
    features_df["deltatime"] = pd.to_timedelta(features_df["deltatime"])

    with open(TRANSFORMERS_DIR / transformer_filename, "rb") as f:
        transformer = dill.load(f)

    X = transformer.transform(features_df)
    X = np.nan_to_num(X)  # type: ignore

    scores = model.decision_function(X)

    return pd.DataFrame(
        {
            "event_record_id": features_df["event_record_id"],
            "anomaly_score": scores,
        }
    )


def evaluate_system(log_id, model):
    return _evaluate(log_id, model, "system_transformer.pkl")


def evaluate_application(log_id, model):
    return _evaluate(log_id, model, "application_transformer.pkl")


def evaluate_security(log_id, model):
    return _evaluate(log_id, model, "security_transformer.pkl")


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

    results = extract_specific_events(
        anomalies_records,
        LOGS_DIR / log_filename,
    )

    for result in results:
        event_record_id = result["data"]["System"]["EventRecordID"]

        event_result = EventResult(
            event_record_id=str(event_record_id),
            evaluation_id=evaluation_id,
            timestamp=result["timestamp"],
            event_id=result["data"]["System"]["EventID"],
            anomaly_score=results_df.loc[
                results_df["event_record_id"] == int(event_record_id),
                "anomaly_score",
            ].iloc[0],
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
