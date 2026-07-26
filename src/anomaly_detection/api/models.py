from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
import json

from sqlmodel import SQLModel, Field


class Test(SQLModel, table=True):
    test_id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str


class LogType(str, Enum):
    SECURITY = "security"
    SYSTEM = "system"
    APPLICATION = "application"


class Log(SQLModel, table=True):
    log_id: UUID = Field(default_factory=uuid4, primary_key=True)
    log_type: LogType
    uploaded_at: datetime = Field(default_factory=datetime.now)
    raw_event_count: Optional[int] = None


class FeatureSet(SQLModel, table=True):
    log_id: UUID = Field(primary_key=True, foreign_key="log.log_id")
    feature_count: Optional[int] = None
    columns_json: str = "[]"
    generated_at: datetime = Field(default_factory=datetime.now)

    @property
    def columns(self) -> list[str]:
        return json.loads(self.columns_json)

    @columns.setter
    def columns(self, value: list[str]) -> None:
        self.columns_json = json.dumps(value)


class ModelInfo(SQLModel, table=True):
    model_id: UUID = Field(default_factory=uuid4, primary_key=True)
    filename: str
    log_type: LogType
    trained_at: datetime = Field(default_factory=datetime.now)
    n_estimators: Optional[int] = None
    max_samples: Optional[float] = None
    max_features: Optional[int] = None


class Evaluation(SQLModel, table=True):
    evaluation_id: UUID = Field(default_factory=uuid4, primary_key=True)
    log_id: UUID = Field(foreign_key="log.log_id")
    model_id: UUID = Field(foreign_key="modelinfo.model_id")
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    decision_boundary: Optional[float] = None
    anomaly_count: Optional[int] = None


class EventResult(SQLModel, table=True):
    event_record_id: str = Field(primary_key=True)
    evaluation_id: UUID = Field(foreign_key="evaluation.evaluation_id")
    timestamp: datetime
    event_id: int
    anomaly_score: float
    raw_fields_json: str = "{}"

    @property
    def raw_fields(self) -> dict:
        return json.loads(self.raw_fields_json)

    @raw_fields.setter
    def raw_fields(self, value: dict) -> None:
        self.raw_fields_json = json.dumps(value)
