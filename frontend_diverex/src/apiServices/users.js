import api from "./client";

export const signup = (data) => api.post("/usuarios/signup", data);

export const login = (data) => api.post("/usuarios/login", data);

export const deleteUser = (id) => api.delete(`/usuarios/${id}`);