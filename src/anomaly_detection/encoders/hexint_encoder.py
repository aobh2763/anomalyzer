from sklearn.base import BaseEstimator, TransformerMixin

import numpy as np
import pandas as pd


def _convert(value):
    if pd.isna(value):
        return 0
    if isinstance(value, str):
        value = value.strip()
        try:
            if value.startswith(("0x", "0X")):
                return int(value, 16)
            return int(value)
        except ValueError:
            return 0
        return int(value)


class HexIntEncoder(BaseEstimator, TransformerMixin):
    """Converts hexadecimal strings and integers to integers."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        values = pd.Series(X.squeeze())

        encoded = values.apply(_convert).astype(np.float64)

        return encoded.to_numpy().reshape(-1, 1)

    def get_feature_names_out(self, input_features=None):
        return np.asarray(input_features)
