import client from "./client";

export const evaluationsApi = {
    evaluateLog: (logId, modelId) => client.post(`/evaluations/${logId}/${modelId}`).then(r => r.data),
    getEvaluation: (evaluationId) => client.get(`/evaluations/${evaluationId}`).then(r => r.data),
    getEvaluationByLogAndModel: (logId, modelId) => client.get(`/evaluations/${logId}/${modelId}`).then(r => r.data),
    getEvaluationImage: (evaluationId) =>
        client.get(`/evaluations/${evaluationId}/image`, {
            responseType: "blob",
        }).then((r) => r.data),
    setDecisionBoundary: (evaluationId, decisionBoundary) =>
        client.patch(`/evaluations/${evaluationId}`, null, {
            params: { decision_boundary: decisionBoundary },
        }).then(r => r.data),
    deleteEvaluation: (evaluationId) => client.delete(`/evaluations/${evaluationId}`),
    getAnomalies: (evaluationId) => client.get(`/evaluations/${evaluationId}/anomalies`).then(r => r.data),
    getAnomalyById: (evaluationId, eventRecordId) => client.get(`/evaluations/${evaluationId}/anomalies/${eventRecordId}`).then(r => r.data)
}