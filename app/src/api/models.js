import client from "./client";

export const modelsApi = {
  getModels: () => client.get("/models/").then((r) => r.data),
  getModel: (modelId) => client.get(`/models/${modelId}`).then((r) => r.data),
  addModel: ({ logType, filename, nEstimators, maxSamples, maxFeatures }) => {
    const params = new URLSearchParams();
    params.append("log_type", logType);
    params.append("filename", filename);
    if (nEstimators != null) params.append("n_estimators", nEstimators);
    if (maxSamples != null) params.append("max_samples", maxSamples);
    if (maxFeatures != null) params.append("max_features", maxFeatures);

    return client.post("/models/", params).then((r) => r.data);
  },
  deleteModel: (modelId) =>
    client.delete(`/models/${modelId}`).then((r) => r.data),
};
