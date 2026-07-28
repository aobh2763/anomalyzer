from fastapi import Depends, APIRouter, HTTPException, Form
from sqlmodel import Session, select
from typing import Optional
from pathlib import Path
from uuid import UUID

from anomaly_detection.api.db import get_session
from anomaly_detection.api.models import ModelInfo, LogType

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = PROJECT_DIR / "models"

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/", response_model=list[ModelInfo])
async def get_all_models(session: Session = Depends(get_session)):
    return session.exec(select(ModelInfo)).all()


@router.get("/{model_id}", response_model=ModelInfo)
async def get_model_by_id(model_id: UUID, session: Session = Depends(get_session)):
    model = session.get(ModelInfo, model_id)

    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")

    return model


@router.post("/", response_model=ModelInfo)
async def add_model(
    log_type: LogType = Form(...),
    filename: str = Form(...),
    n_estimators: Optional[int] = Form(None),
    max_samples: Optional[float] = Form(None),
    max_features: Optional[int] = Form(None),
    session: Session = Depends(get_session),
):
    model_path = MODELS_DIR / filename

    if not Path.exists(model_path):
        raise HTTPException(
            status_code=400,
            detail="The model does not exist on the server. (Did you forget the file extension?)",
        )

    model_info = ModelInfo(
        filename=filename,
        log_type=log_type,
        n_estimators=n_estimators,
        max_samples=max_samples,
        max_features=max_features,
    )

    session.add(model_info)
    session.commit()
    session.refresh(model_info)

    return model_info


@router.delete("/{model_id}")
async def delete_model(model_id: UUID, session: Session = Depends(get_session)):
    model = session.get(ModelInfo, model_id)

    if model is None:
        return

    model.deprecated = True

    session.add(model)
    session.commit()
    session.refresh(model)
