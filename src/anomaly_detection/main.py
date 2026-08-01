from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from anomaly_detection.api.db import init_db
from anomaly_detection.api.routers import *

init_db()
app = FastAPI(
    title="Anomaly Detection API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(logs_router)
app.include_router(models_router)
app.include_router(features_router)
app.include_router(evaluation_router)
app.include_router(anomalies_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Anomaly Detection API!"}
