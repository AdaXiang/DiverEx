import api from "./client";

export const getRecommendations = (userId) =>
  api.get(`/preferencias/recomendaciones/${userId}`);

export const getFilteredRecommendations = (userId, params) =>
  api.get(`/preferencias/recomendaciones-filtradas/${userId}`, { params });

export const getTop = (params) =>
  api.get("/preferencias/top", { params });