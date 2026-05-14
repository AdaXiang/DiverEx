import api from "./client";
import qs from "qs";

export const getRecommendations = (userId) =>
  api.get(`/preferencias/recomendaciones/${userId}`);


export const getFilteredRecommendations = (userId, params) => {

  // eliminar null, undefined y strings vacíos
  const cleanParams = Object.fromEntries(
    Object.entries(params).filter(
      ([_, value]) =>
        value !== null &&
        value !== undefined &&
        value !== ""
    )
  );

  return api.get(
    `/preferencias/recomendaciones-filtradas/${userId}`,
    {
      params: cleanParams,

      paramsSerializer: (params) =>
        qs.stringify(params, {
          arrayFormat: "repeat"
        })
    }
  );
};


export const getTop = (params) =>
  api.get("/preferencias/top", { params });