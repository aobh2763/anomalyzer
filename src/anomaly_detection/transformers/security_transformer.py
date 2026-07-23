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
        ("entity", EntityEncoder(), ["entity"]),
        ("context", ordinal_pipeline, ["context"]),
        ("correlation_activity_id", "drop", ["correlation_activity_id"]),
        ("execution_thread_id", "drop", ["execution_thread_id"]),
        ("actor", onehot_pipeline, ["actor"]),
        ("value", PresenceXMLTransformer(), ["value"]),
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
