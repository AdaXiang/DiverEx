# ==============================
# Recupera las llamadas de las API, encia los datos al services
# ==============================
from fastapi import APIRouter, HTTPException, status
from microservicio_memgraph.services.visitaService import (
    addVisita, 
    getVisitasUsuario,
    removeVisita
)

router = APIRouter()

# ==============================
# VISITAR LUGAR
# ==============================
@router.post("/", status_code=status.HTTP_201_CREATED)
def createVisita(data: dict):

    user_id = data.get("user_id")
    lugar_id = data.get("lugar_id")

    if not user_id or not lugar_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "user_id y lugar_id requeridos")

    visita = addVisita(user_id, lugar_id)

    if not visita:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario o lugar no encontrado")

    return visita.toDict()

# ==============================
# LUGARES VISITADOS
# ==============================
@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def getVisitas(user_id: str):
    visitas = getVisitasUsuario(user_id)

    return visitas

# ==============================
# ELIMINAR VISITA
# ==============================
@router.delete("/", status_code=status.HTTP_200_OK)
def deleteVisita(data: dict):
    user_id = data.get("user_id")
    lugar_id = data.get("lugar_id")

    if not user_id or not lugar_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "user_id y lugar_id requeridos")

    deleted = removeVisita(user_id, lugar_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "La visita no existía")

    return {"message": "Visita eliminada correctamente"}