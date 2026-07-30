import client from "./client";

export const featuresApi = {
    extractFeatures: (logId) => client.post(`/features/${logId}`).then(r => r.data),
    getFeatures: (logId) => client.get(`/features/${logId}`).then(r => r.data),
    downloadFeatures: (logId) =>
        client.get(`/features/${logId}/download`, {
            responseType: 'blob',
        }).then(r => r.data),
    deleteFeatures: (logId) => client.delete(`/features/${logId}`)
}