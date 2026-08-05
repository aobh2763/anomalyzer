import client from "./client";

export const logsApi = {
  getLogs: () => client.get("/logs/").then((r) => r.data),
  getLog: (logId) => client.get(`/logs/${logId}`).then((r) => r.data),
  uploadLog: (file) => {
    const formData = new FormData();
    formData.append("file", file);
    return client.post(`/logs/`, formData).then((r) => r.data);
  },
  deleteLog: (logId) => client.delete(`/logs/${logId}`),
  getEvaluations: (logId) =>
    client.get(`/logs/${logId}/evaluations`).then((r) => r.data),
};
