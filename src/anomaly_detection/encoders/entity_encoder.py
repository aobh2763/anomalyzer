import re

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

USER_SUFFIX_PATTERN = re.compile(r"_[0-9a-fA-F]{8}$")
GUID_PATTERN = re.compile(
    r"\{[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}\}"
)
SID_PATTERN = re.compile(r"^S-\d(-\d+)+$")
MACHINE_ACCOUNT_PATTERN = re.compile(r".+\$$")


def _normalize(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value in ("", "-"):
        return None

    # normalize Windows service suffixes
    value = USER_SUFFIX_PATTERN.sub("", value)

    # replace GUIDs with a placeholder
    value = GUID_PATTERN.sub("{GUID}", value)

    lower = value.lower()

    # normalize WMI namespaces
    if lower.startswith("root\\"):
        value = lower

    # normalize WindowsLive identifiers
    if lower.startswith("windowslive:"):
        if "(token)" in lower:
            return "windowslive:(token)"
        if "(cert)" in lower:
            return "windowslive:(cert)"
        return "windowslive"

    # normalize MicrosoftAccount identifiers
    if lower.startswith("microsoftaccount:"):
        return "microsoftaccount"

    return value


class EntityEncoder(BaseEstimator, TransformerMixin):
    """Encodes Windows entities into structural features + frequency."""

    def fit(self, X, y=None):
        X = pd.Series(np.asarray(X).ravel()).map(_normalize)

        self.frequencies_ = X.value_counts(normalize=True, dropna=True).to_dict()

        return self

    def transform(self, X):
        X = np.asarray(X).ravel()

        rows = []

        for value in X:
            normalized = _normalize(value)

            text = "" if normalized is None else str(normalized)
            lower = text.lower()

            is_sid = bool(SID_PATTERN.fullmatch(text))

            is_path = text.startswith("\\")

            is_systemroot_path = lower.startswith(r"\systemroot")

            is_wmi_namespace = lower.startswith("root\\")

            has_guid = isinstance(value, str) and GUID_PATTERN.search(value) is not None

            has_user_suffix = (
                isinstance(value, str)
                and USER_SUFFIX_PATTERN.search(value.strip()) is not None
            )

            is_machine_account = bool(MACHINE_ACCOUNT_PATTERN.fullmatch(text))

            is_account_identifier = lower.startswith(
                "windowslive:"
            ) or lower.startswith("microsoftaccount:")

            rows.append(
                [
                    is_sid,
                    is_path,
                    is_systemroot_path,
                    is_wmi_namespace,
                    has_guid,
                    has_user_suffix,
                    is_machine_account,
                    is_account_identifier,
                ]
            )

        return np.asarray(rows, dtype=np.float64)

    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            return None

        feature = input_features[0]

        return np.array(
            [
                f"{feature}_is_sid",
                f"{feature}_is_path",
                f"{feature}_is_systemroot_path",
                f"{feature}_is_wmi_namespace",
                f"{feature}_has_guid",
                f"{feature}_has_user_suffix",
                f"{feature}_is_machine_account",
                f"{feature}_is_account_identifier",
            ]
        )
