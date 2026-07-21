from anomaly_detection.encoders import *
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer

from anomaly_detection.transformers.pipelines import (
    _seconds,
    _has_value,
    onehot_pipeline,
)

application_transformer = ColumnTransformer(
    [
        ("deltatime", FunctionTransformer(_seconds), ["deltatime"]),
        (
            "correlation_activity_id",
            FunctionTransformer(_has_value),
            ["correlation_activity_id"],
        ),
        ("entity", onehot_pipeline, ["entity"]),
        (
            "context",
            EmbeddingEncoder(
                model_path=str(
                    Path.cwd().parent / "src/anomaly_detection/models/all-MiniLM-L6-v2"
                ),
                n_components=32,
            ),
            ["context"],
        ),
    ],
    remainder="passthrough",
    verbose_feature_names_out=False,
)
