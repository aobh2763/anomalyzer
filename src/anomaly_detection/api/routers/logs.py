from fastapi import Depends, APIRouter, UploadFile, File, HTTPException
from sqlmodel import Session, select
from pathlib import Path
from uuid import UUID
import shutil

from anomaly_detection.api.db import get_session
from anomaly_detection.api.services import delete_evaluation
from anomaly_detection.etl.extract import extract_timestamps
from anomaly_detection.api.models import Log, LogType, Evaluation, FeatureSet

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = PROJECT_DIR / "storage/logs"
FEATURES_DIR = PROJECT_DIR / "storage/features"

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/", response_model=list[Log])
async def get_all_logs(session: Session = Depends(get_session)):
    return session.exec(select(Log)).all()


@router.get("/{log_id}", response_model=Log)
async def get_log_by_id(log_id: UUID, session: Session = Depends(get_session)):
    log = session.get(Log, log_id)

    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    return log


@router.post("/", response_model=Log)
async def upload_log(
    log_type: LogType,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    if file.filename is None:
        raise HTTPException(status_code=400, detail="No filename provided.")

    extension = Path(file.filename).suffix.lower()

    if extension != ".evtx":
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    log = Log(log_type=log_type)

    filename = f"{log.log_id}{extension}"
    destination = LOGS_DIR / filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    log.raw_event_count = len(extract_timestamps(destination))

    session.add(log)
    session.commit()
    session.refresh(log)

    return log


@router.delete("/{log_id}")
async def delete_log(log_id: UUID, session: Session = Depends(get_session)):
    log = session.get(Log, log_id)

    if log is None:
        return

    features = session.exec(
        select(FeatureSet).where(FeatureSet.log_id == log_id)
    ).first()

    if features is not None:
        feature_filename = f"{log_id}.csv"

        (FEATURES_DIR / feature_filename).unlink(missing_ok=True)

        session.delete(features)
        session.commit()

    evaluations = session.exec(select(Evaluation).where(Evaluation.log_id == log_id))

    for evaluation in evaluations:
        delete_evaluation(evaluation.evaluation_id, session)

    log_filename = f"{log_id}.evtx"

    (LOGS_DIR / log_filename).unlink(missing_ok=True)

    session.delete(log)
    session.commit()


@router.get("/{log_id}/evaluations")
async def get_evaluations_by_log(log_id: UUID, session: Session = Depends(get_session)):
    log = session.get(Log, log_id)

    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    evaluations = session.exec(
        select(Evaluation).where(Evaluation.log_id == log_id)
    ).all()

    return evaluations
