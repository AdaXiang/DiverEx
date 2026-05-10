import api from "./client";

// Crear comentario
export const createComment = (data) => 
  api.post("/comentarios", data);

// Eliminar comentario
export const deleteComment = (data) => 
  api.delete("/comentarios", { data });

// Comentarios de un lugar
export const getCommentsByPlace = (
  placeId,
  rankingMin = null,
  rankingMax = null
) => {

  let query = [];

  if (rankingMin !== null) {
    query.push(`ranking_min=${rankingMin}`);
  }

  if (rankingMax !== null) {
    query.push(`ranking_max=${rankingMax}`);
  }

  const queryString =
    query.length > 0
      ? `?${query.join("&")}`
      : "";

  return api.get(
    `/comentarios/lugar/${placeId}${queryString}`
  );
};

// Comentarios de un usuario
export const getCommentsByUser = (userId) => 
  api.get(`/comentarios/usuario/${userId}`);