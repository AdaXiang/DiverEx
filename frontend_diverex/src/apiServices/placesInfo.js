import api from "./client";

// Crear lugar
export const createPlace = (data) => 
  api.post("/lugares", data);

// Actualizar lugar
export const updatePlace = (id, data) => 
  api.put(`/lugares/${id}`, data);

// Obtener todos
export const getPlaces = () => 
  api.get("/lugares");

// Obtener uno
export const getPlace = (id) => 
  api.get(`/lugares/${id}`);

// Eliminar lugar
export const deletePlace = (id) => 
  api.delete(`/lugares/${id}`);