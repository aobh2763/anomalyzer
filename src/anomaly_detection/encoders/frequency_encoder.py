from sklearn.base import BaseEstimator, TransformerMixin

import numpy as np
import pandas as pd


def _normalize(value):
    if pd.isna(value):
        return value

    return str(value).strip().lower()


class FrequencyEncoder(BaseEstimator, TransformerMixin):
    """Encodes categorical values by their relative frequency."""

    def __init__(self, normalize=False, unknown_value=0.0):
        self.normalize = normalize
        self.unknown_value = unknown_value

    def fit(self, X, y=None):
        X = pd.Series(np.asarray(X).ravel())

        if self.normalize:
            X = X.map(_normalize)

        self.frequencies_ = X.value_counts(normalize=True).to_dict()

        return self

    def transform(self, X):
        X = pd.Series(np.asarray(X).ravel())

        return (
            X.map(self.frequencies_)
            .fillna(self.unknown_value)
            .to_numpy(dtype=np.float64)
            .reshape(-1, 1)
        )

    def get_feature_names_out(self, input_features=None):
        return np.asarray(input_features)
