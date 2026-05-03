import api from "./client";

// Crear visita
export const createVisit = (data) => 
  api.post("/visitas", data);

// Obtener visitas de un usuario
export const getVisits = (userId) => 
  api.get(`/visitas/${userId}`);

// Eliminar visita
export const deleteVisit = (data) => 
  api.delete("/visitas", { data });