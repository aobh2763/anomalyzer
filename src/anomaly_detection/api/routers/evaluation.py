from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from datetime import datetime
from pathlib import Path
from uuid import UUID
import joblib
import shutil

from anomaly_detection.api.db import get_session
from anomaly_detection.api.models import FeatureSet, Log, LogType, Evaluation, ModelInfo
from anomaly_detection.api.services import (
    evaluate_system,
    evaluate_application,
    evaluate_security,
)

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = PROJECT_DIR / "models"
RESULTS_DIR = PROJECT_DIR / "storage/results"

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.post("/{log_id}/{model_id}", response_model=Evaluation)
def evaluate_log(log_id: UUID, model_id: UUID, session: Session = Depends(get_session)):
    log = session.get(Log, log_id)

    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    model = session.get(ModelInfo, model_id)

    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")

    if model.log_type != log.log_type:
        raise HTTPException(status_code=400, detail="Model and Log type incompatible.")

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
