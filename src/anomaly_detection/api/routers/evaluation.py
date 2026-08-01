from fastapi import Depends, APIRouter, HTTPException, Response
from sqlmodel import Session, select
from datetime import datetime
from pathlib import Path
from uuid import UUID
import joblib
import shutil

from anomaly_detection.api.db import get_session
from anomaly_detection.api.models import (
    Log,
    LogType,
    Evaluation,
    ModelInfo,
)
from anomaly_detection.api.services import (
    evaluate_system,
    evaluate_application,
    evaluate_security,
    update_decision_boundary,
    delete_evaluation,
    get_score_histogram,
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
        case LogType.UNKNOWN:
            raise HTTPException(status_code=400, detail="Invalid log type")

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


@router.get("/{evaluation_id}/image")
def get_evaluation_image(evaluation_id: UUID, session: Session = Depends(get_session)):
    png_bytes = get_score_histogram(evaluation_id, session)

    return Response(content=png_bytes, media_type="image/png")


@router.get("/{log_id}/{model_id}", response_model=Evaluation)
async def get_eval_by_log_and_model(
    log_id: UUID, model_id: UUID, session: Session = Depends(get_session)
):
    evaluation = session.exec(
        select(Evaluation).where(
            Evaluation.log_id == log_id, Evaluation.model_id == model_id
        )
    ).first()

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


@router.delete("/{evaluation_id}")
async def delete_evaluation_by_id(
    evaluation_id: UUID, session: Session = Depends(get_session)
):
    evaluation = session.get(Evaluation, evaluation_id)

    if evaluation is None:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    delete_evaluation(evaluation_id, session)
