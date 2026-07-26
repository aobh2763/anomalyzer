from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # folder containing db.py
STORAGE_DIR = BASE_DIR / "../storage"
STORAGE_DIR.mkdir(exist_ok=True)  # ensure it exists before engine tries to open it

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
