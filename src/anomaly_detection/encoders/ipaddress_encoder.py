from sklearn.base import BaseEstimator, TransformerMixin

import numpy as np
import pandas as pd
import ipaddress


def parse_ip(value):
    """Pases string representation of an IP address and returns a list of the first four octets."""
    if value in (None, "", "-") or pd.isna(value):
        return None

    try:
        ip = ipaddress.ip_address(value)
    except ValueError:
        return None

    if ip.version != 4:
        return None

    return list(map(int, str(ip).split(".")))


class IPAddressEncoder(BaseEstimator, TransformerMixin):
    """Transforms an IPv4 address into its four octets."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = np.asarray(X).ravel()

        transformed = []

        for value in X:
            octets = parse_ip(value)

            if octets is None:
                transformed.append([0, 0, 0, 0, 0])
            else:
                transformed.append([1, *octets])

        return np.asarray(transformed, dtype=np.float64)

    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            return

        feature = input_features[0]
        return np.array(
            [
                f"{feature}_has_value",
                f"{feature}_octet1",
                f"{feature}_octet2",
                f"{feature}_octet3",
                f"{feature}_octet4",
            ]
        )
