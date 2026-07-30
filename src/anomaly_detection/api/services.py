import io
import dill
import pandas as pd
import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pathlib import Path
from sqlalchemy import delete
from sqlmodel import Session, select
from anomaly_detection.api.db import get_session
from anomaly_detection.etl.load import load_records
from anomaly_detection.parser.data_parsers import *
from anomaly_detection.api.models import Evaluation, EventResult, LogType
from anomaly_detection.utils.extract_shared_features import extract_specific_events

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_DIR / "storage/logs"
FEATURES_DIR = PROJECT_DIR / "storage/features"
TRANSFORMERS_DIR = PROJECT_DIR / "storage/transformers"
RESULTS_DIR = PROJECT_DIR / "storage/results"


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


def plot_score_histogram(
    scores, decision_boundary=None, title="Decision function distribution", bins=100
):
    """Plot a histogram of Isolation Forest decision_function scores.

    Args:
        scores (array-like): decision_function scores for each event.
        decision_boundary (float | None): x-position to draw as a vertical
            reference line. If None, no boundary line is drawn.
        title (str): Plot title.
        bins (int): Number of histogram bins.

    Returns:
        matplotlib.figure.Figure: The generated figure, not yet shown/saved.
    """
    scores = np.asarray(scores)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(scores, bins=bins, color="orange", alpha=0.8, label="all points")

    if decision_boundary is not None:
        ax.axvline(
            decision_boundary,
            color="black",
            linestyle="--",
            linewidth=1,
            label=f"decision boundary ({decision_boundary:.4f})",
        )

    ax.set_title(title)
    ax.set_xlabel("decision_function score (lower = more anomalous)")
    ax.set_ylabel("count")
    ax.legend()

    fig.tight_layout()

    return fig


def score_histogram_to_png_bytes(
    scores, decision_boundary=None, title="Decision function distribution", bins=100
):
    fig = plot_score_histogram(scores, decision_boundary, title, bins)

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=100)
    plt.close(fig)
    buffer.seek(0)

    return buffer.getvalue()


def get_score_histogram(evaluation_id, session: Session):
    evaluation = session.get(Evaluation, evaluation_id)
    assert evaluation is not None

    evaluation_filename = f"{evaluation_id}.csv"
    results_df = pd.read_csv(RESULTS_DIR / evaluation_filename)

    scores = results_df["anomaly_score"].to_numpy()

    return score_histogram_to_png_bytes(
        scores,
        decision_boundary=evaluation.decision_boundary,
        title=f"Evaluation {evaluation_id} - decision function distribution",
    )
