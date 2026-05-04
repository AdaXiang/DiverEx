import api from "./client";

export const like = (data) => api.post("/likes", data);

export const getLikes = (userId) => api.get(`/likes/${userId}`);

export const unlike = (data) => api.delete("/likes", { data });