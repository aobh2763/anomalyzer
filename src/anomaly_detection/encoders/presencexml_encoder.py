from sklearn.base import BaseEstimator, TransformerMixin

import numpy as np
import pandas as pd


class PresenceXMLEncoder(BaseEstimator, TransformerMixin):
    """Infers two attributes: has_value (not None) and is_xml (string contains XML)."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        values = pd.Series(X.squeeze())

        has_value = values.notna().astype(np.float64)

        is_xml = values.fillna("").str.lstrip().str.startswith("<").astype(np.float64)

        return np.column_stack([has_value, is_xml])

    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            return

        feature = input_features[0]
        return np.array(
            [
                f"{feature}_has_value",
                f"{feature}_is_xml",
            ]
        )
