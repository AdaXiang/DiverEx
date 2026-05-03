import api from "./client";

// Añadir favorito
export const addFavorite = (data) => 
  api.post("/favoritos", data);

// Obtener favoritos
export const getFavorites = (userId) => 
  api.get(`/favoritos/${userId}`);

// Eliminar favorito
export const removeFavorite = (data) => 
  api.delete("/favoritos", { data });