from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select
from pathlib import Path
from uuid import UUID

from anomaly_detection.api.db import get_session
from anomaly_detection.api.models import (
    Evaluation,
    EventResult,
)

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = PROJECT_DIR / "models"
RESULTS_DIR = PROJECT_DIR / "storage/results"

router = APIRouter(prefix="/evaluations", tags=["anomalies"])


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
