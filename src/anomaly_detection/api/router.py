from fastapi import Depends, APIRouter, status
from sqlmodel import Session, select

from anomaly_detection.api.db import init_db, get_session
from anomaly_detection.api.models import Test

router = APIRouter(prefix="/detector", tags=["detector"])


@router.post("/{name}", response_model=Test)
async def add_test(name: str, session: Session = Depends(get_session)):
    test = Test(name=name)

    session.add(test)
    session.commit()
    session.refresh(test)

    return test


@router.get("/", response_model=list[Test])
async def get_all(session: Session = Depends(get_session)):
    return session.exec(select(Test)).all()
