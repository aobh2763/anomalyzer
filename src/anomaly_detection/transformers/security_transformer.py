from anomaly_detection.encoders import *

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer

from anomaly_detection.transformers.pipelines import (
    _seconds,
    _has_value,
    ordinal_pipeline,
    onehot_pipeline,
)

security_transformer = ColumnTransformer(
    [
        ("deltatime", FunctionTransformer(_seconds), ["deltatime"]),
        (
            "correlation_activity_id",
            FunctionTransformer(_has_value),
            ["correlation_activity_id"],
        ),
        ("entity", EntityEncoder(), ["entity"]),
        ("context", ordinal_pipeline, ["context"]),
        ("actor", onehot_pipeline, ["actor"]),
        ("value", PresenceXMLEncoder(), ["value"]),
        ("ip", IPAddressEncoder(), ["ip"]),
        ("status", onehot_pipeline, ["status"]),
        ("logon_id", HexIntEncoder(), ["logon_id"]),
        ("process_id", HexIntEncoder(), ["process_id"]),
        ("process_name", onehot_pipeline, ["process_name"]),
        ("permisson", ordinal_pipeline, ["permission"]),
    ],
    remainder="passthrough",
    verbose_feature_names_out=False,
)
