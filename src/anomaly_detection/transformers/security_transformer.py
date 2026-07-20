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


security_transformer = ColumnTransformer(
    [
        (FunctionTransformer(_seconds), "deltatime"),
        (FunctionTransformer(_has_value), "correlation_activity_id"),
        (EntityEncoder(), "entity"),
        (LabelEncoder(), "context"),
        (OneHotEncoder(handle_unknown="ignore"), "actor"),
        (PresenceXMLTransformer(), "value"),
        (IPAddressEncoder(), "ip"),
        (OneHotEncoder(handle_unknown="ignore"), "status"),
        (HexIntEncoder(), "logon_id"),
        (HexIntEncoder(), "process_id"),
        (LabelEncoder(), "permission"),
    ],
    remainder="passthrough",
    verbose_feature_names_out=False,
)
