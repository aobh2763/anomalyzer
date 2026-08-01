from anomaly_detection.api.routers.logs import router as logs_router
from anomaly_detection.api.routers.models import router as models_router
from anomaly_detection.api.routers.features import router as features_router
from anomaly_detection.api.routers.evaluation import router as evaluation_router
from anomaly_detection.api.routers.anomalies import router as anomalies_router

__all__ = [
    "logs_router",
    "models_router",
    "features_router",
    "evaluation_router",
    "anomalies_router",
]
