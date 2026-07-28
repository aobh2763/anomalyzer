from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from datetime import datetime
from pathlib import Path
from uuid import UUID
import joblib
import shutil

from anomaly_detection.api.db import get_session
from anomaly_detection.api.models import (
    FeatureSet,
    Log,
    LogType,
    Evaluation,
    ModelInfo,
    EventResult,
)
from anomaly_detection.api.services import (
    evaluate_system,
    evaluate_application,
    evaluate_security,
    update_decision_boundary,
    delete_evaluation,
)

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = PROJECT_DIR / "models"
RESULTS_DIR = PROJECT_DIR / "storage/results"

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.post("/{log_id}/{model_id}", response_model=Evaluation)
async def evaluate_log(
    log_id: UUID, model_id: UUID, session: Session = Depends(get_session)
):
    log = session.get(Log, log_id)

    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    model = session.get(ModelInfo, model_id)

    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")

    if model.deprecated:
        raise HTTPException(status_code=400, detail="Model is deprecated")

    if model.log_type != log.log_type:
        raise HTTPException(status_code=400, detail="Model and Log type incompatible")

    evaluation = Evaluation(log_id=log_id, model_id=model_id)

    sk_model = joblib.load(MODELS_DIR / model.filename)

    match log.log_type:
        case LogType.SYSTEM:
            results = evaluate_system(log_id, sk_model)
        case LogType.APPLICATION:
            results = evaluate_application(log_id, sk_model)
        case LogType.SECURITY:
            results = evaluate_security(log_id, sk_model)

    filename = f"{evaluation.evaluation_id}.csv"
    results.to_csv(RESULTS_DIR / filename)

    evaluation.completed_at = datetime.now()

    session.add(evaluation)
    session.commit()
    session.refresh(evaluation)

    return evaluation


@router.get("/{evaluation_id}", response_model=Evaluation)
async def get_evaluation(evaluation_id: UUID, session: Session = Depends(get_session)):
    evaluation = session.get(Evaluation, evaluation_id)

    if evaluation is None:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    return evaluation


@router.patch("/{evaluation_id}", response_model=Evaluation)
async def set_decision_boundary(
    evaluation_id: UUID,
    decision_boundary: float,
    session: Session = Depends(get_session),
):
    if decision_boundary > 1 or decision_boundary < -1:
        raise HTTPException(status_code=400, detail="Invalid decision boundary")

    evaluation = session.get(Evaluation, evaluation_id)

    if evaluation is None:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    evaluation.anomaly_count = update_decision_boundary(
        evaluation_id, decision_boundary, session
    )
    evaluation.decision_boundary = decision_boundary

    session.add(evaluation)
    session.commit()

    return evaluation


@router.get("/{evaluation_id}/anomalies", response_model=list[EventResult])
async def get_anomalies(evaluation_id: UUID, session: Session = Depends(get_session)):
    evaluation = session.get(Evaluation, evaluation_id)

    if evaluation is None:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    anomalies = session.exec(
        select(EventResult).where(EventResult.evaluation_id == evaluation_id)
    )

    return anomalies


@router.get("/{evaluation_id}/anomalies/{event_record_id}", response_model=EventResult)
async def get_anomaly_by_id(
    evaluation_id: UUID, event_record_id: str, session: Session = Depends(get_session)
):
    evaluation = session.get(Evaluation, evaluation_id)

    if evaluation is None:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    anomaly = session.exec(
        select(EventResult).where(
            EventResult.evaluation_id == evaluation_id
            and EventResult.event_record_id == event_record_id
        )
    ).first()

    if anomaly is None:
        raise HTTPException(status_code=404, detail="Anomaly not found")

    return anomaly


@router.delete("/{evaluation_id}")
async def delete_evaluation_by_id(
    evaluation_id: UUID, session: Session = Depends(get_session)
):
    evaluation = session.get(Evaluation, evaluation_id)

    if evaluation is None:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    delete_evaluation(evaluation_id, session)
