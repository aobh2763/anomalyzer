import client from "./client";

const logsApi = {
    getLogs: () => client.get('/logs/').then(r => r.data),
    getLog: (logId) => client.get(`/logs/${logId}`).then(r => r.data),
    uploadLog: (file, logType) => {
        const formData = new FormData();
        formData.append('file', file);
        return client.post(`/logs/`, formData, {
            params: { log_type: logType }
        }).then(r => r.data);
    },
    deleteLog: (logId) => client.delete(`/logs/${logId}`),
    getEvaluations: (logId) => client.get(`/logs/${logId}/evaluations`).then(r => r.data)
}

export default logsApi;