from anomaly_detection.encoders import *

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer

from anomaly_detection.transformers.pipelines import (
    _seconds,
    ordinal_pipeline,
    onehot_pipeline,
)

system_transformer = ColumnTransformer(
    [
        ("deltatime", FunctionTransformer(_seconds), ["deltatime"]),
        ("correlation_activity_id", ordinal_pipeline, ["correlation_activity_id"]),
        ("new_value", MixedValueEncoder(), ["new_value"]),
        ("process_name", onehot_pipeline, ["process_name"]),
        ("entity", EntityEncoder(), ["entity"]),
        ("context", FrequencyEncoder(normalize=True), ["context"]),
        ("actor", onehot_pipeline, ["actor"]),
        ("old_value", MixedValueEncoder(), ["old_value"]),
        ("status", onehot_pipeline, ["status"]),
    ],
    remainder="passthrough",
    verbose_feature_names_out=False,
)
