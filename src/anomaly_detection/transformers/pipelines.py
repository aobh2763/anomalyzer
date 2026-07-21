import pandas as pd

from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline


def _seconds(X):
    """Convert a timedelta64 column to float seconds."""
    return pd.DataFrame(X).apply(lambda col: col.dt.total_seconds()).to_numpy()


def _has_value(X):
    """Presence-only flag (1/0), for fields where the raw value is meaningless"""
    return (~pd.DataFrame(X).isna()).astype(int).to_numpy()


onehot_pipeline = Pipeline(
    [
        ("to_string", FunctionTransformer(lambda X: X.astype(str), validate=False)),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

ordinal_pipeline = Pipeline(
    [
        ("to_string", FunctionTransformer(lambda X: X.astype(str), validate=False)),
        (
            "ordinal",
            OrdinalEncoder(
                handle_unknown="use_encoded_value",
                unknown_value=-1,
            ),
        ),
    ]
)
