from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = PROJECT_DIR / "storage"

DATABASE_URL = f"sqlite:///{STORAGE_DIR / 'app.db'}"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,
)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
