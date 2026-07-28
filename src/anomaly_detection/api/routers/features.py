from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from pathlib import Path
from uuid import UUID
import shutil

from anomaly_detection.api.db import get_session
from anomaly_detection.api.models import FeatureSet, Log, LogType
from anomaly_detection.api.services import (
    extract_system_features,
    extract_application_features,
    extract_security_features,
)

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = PROJECT_DIR / "storage/logs"
FEATURES_DIR = PROJECT_DIR / "storage/features"

router = APIRouter(prefix="/features", tags=["features"])


@router.post("/{log_id}", response_model=FeatureSet)
async def extract_features(log_id: UUID, session: Session = Depends(get_session)):
    log = session.get(Log, log_id)

    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    match log.log_type:
        case LogType.SYSTEM:
            column_list = extract_system_features(log_id)
        case LogType.APPLICATION:
            column_list = extract_application_features(log_id)
        case LogType.SECURITY:
            column_list = extract_security_features(log_id)

    features = FeatureSet(log_id=log_id, feature_count=len(column_list))
    features.columns = column_list

    session.add(features)
    session.commit()
    session.refresh(features)

    return features


@router.get("/{log_id}", response_model=FeatureSet)
async def get_feature_set(log_id: UUID, session: Session = Depends(get_session)):
    features = session.get(FeatureSet, log_id)

    if features is None:
        raise HTTPException(status_code=404, detail="Feature set not found")

    return features


@router.delete("/{log_id}")
async def delete_feature_set(log_id: UUID, session: Session = Depends(get_session)):
    features = session.get(FeatureSet, log_id)

    if features is None:
        return

    filename = f"{log_id}.csv"
    filepath = FEATURES_DIR / filename
    filepath.unlink()

    session.delete(features)
    session.commit()


@router.get("/{log_id}/download")
async def download_features(log_id: UUID, session: Session = Depends(get_session)):
    features = session.get(FeatureSet, log_id)

    if features is None:
        raise HTTPException(status_code=404, detail="Feature set not found")

    filename = f"{log_id}.csv"
    filepath = FEATURES_DIR / filename

    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Feature file not found on disk")

    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="text/csv",
    )
