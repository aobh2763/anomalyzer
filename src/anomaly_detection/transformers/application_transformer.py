import pandas as pd

from anomaly_detection.encoders import *
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, LabelEncoder


def _seconds(X):
    """Convert a timedelta64 column to float seconds."""
    return pd.DataFrame(X).apply(lambda col: col.dt.total_seconds()).to_numpy()


def _has_value(X):
    """Presence-only flag (1/0), for fields where the raw value is meaningless"""
    return (~pd.DataFrame(X).isna()).astype(int).to_numpy()


application_transformer = ColumnTransformer(
    [
        (FunctionTransformer(_seconds), "deltatime"),
        (FunctionTransformer(_has_value), "correlation_activity_id"),
        (OneHotEncoder(handle_unknown="ignore"), "entity"),
        (
            EmbeddingEncoder(
                model_path=str(
                    Path.cwd() / "src/anomaly_detection/models/all-MiniLM-L6-v2"
                ),
                n_components=32,
            ),
            "context",
        ),
    ],
    remainder="passthrough",
    verbose_feature_names_out=False,
)
