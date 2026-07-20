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


system_transformer = ColumnTransformer(
    [
        (FunctionTransformer(_seconds), "deltatime"),
        (LabelEncoder(), "correlation_activity_id"),
        (MixedValueEncoder(), "new_value"),
        (OneHotEncoder(handle_unknown="ignore"), "process_name"),
        (EntityEncoder(), "entity"),
        (FrequencyEncoder(normalize=True), "context"),
        (OneHotEncoder(handle_unknown="ignore"), "actor"),
        (MixedValueEncoder(), "old_value"),
        (OneHotEncoder(handle_unknown="ignore"), "status"),
    ],
    remainder="passthrough",
    verbose_feature_names_out=False,
)
