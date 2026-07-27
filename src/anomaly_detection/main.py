from fastapi import FastAPI

from anomaly_detection.api.db import init_db
from anomaly_detection.api.routers.evaluation import router

init_db()
app = FastAPI(
    title="Anomaly Detection API",
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Welcome to the main application API Engine!"}
