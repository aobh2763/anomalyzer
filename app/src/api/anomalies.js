import client from "./client";

export const anomaliesApi = {
    getAnomalies: (evaluationId) => client.get(`/anomalies/${evaluationId}`).then(r => r.data),
    getAnomalyById: (evaluationId, eventRecordId) => client.get(`/anomalies/${evaluationId}/${eventRecordId}`).then(r => r.data),
    explainAnomalyById: (evaluationId, eventRecordId) => client.get(`/anomalies/${evaluationId}/${eventRecordId}/explain`).then(r => r.data)
}