import api from "./client";

// Crear comentario
export const createComment = (data) => 
  api.post("/comentarios", data);

// Eliminar comentario
export const deleteComment = (data) => 
  api.delete("/comentarios", { data });

// Comentarios de un lugar
export const getCommentsByPlace = (placeId) => 
  api.get(`/comentarios/lugar/${placeId}`);

// Comentarios de un usuario
export const getCommentsByUser = (userId) => 
  api.get(`/comentarios/usuario/${userId}`);