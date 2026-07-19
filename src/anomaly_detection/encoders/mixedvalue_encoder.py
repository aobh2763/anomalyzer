from sklearn.base import BaseEstimator, TransformerMixin
from datetime import datetime

import numpy as np
import pandas as pd


def _is_timestamp(value):
    if not isinstance(value, str):
        return False

    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


class MixedValueEncoder(BaseEstimator, TransformerMixin):
    """Infers the type of a mixed-value column."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = np.asarray(X).ravel()

        transformed = []

        for value in X:
            has_value = value is not None and value != ""

            is_integer = isinstance(value, (int, np.integer))

            is_timestamp = _is_timestamp(value)

            is_text = (
                isinstance(value, str) and not is_timestamp and value.strip() != ""
            )

            transformed.append(
                [
                    has_value,
                    is_integer,
                    is_timestamp,
                    is_text,
                ]
            )

        return np.asarray(transformed, dtype=np.uint8)

    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            return

        feature = input_features[0]

        return np.array(
            [
                f"{feature}_has_value",
                f"{feature}_is_integer",
                f"{feature}_is_timestamp",
                f"{feature}_is_text",
            ]
        )
