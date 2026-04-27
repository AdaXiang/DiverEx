# ==============================
# API ME_GUSTA
# ==============================
from fastapi import APIRouter, HTTPException, status
from microservicio_memgraph.services.meGustaService import (
    addMeGusta,
    getMeGustaUsuario,
    removeMeGusta
)

router = APIRouter()

# ==============================
# DAR LIKE
# ==============================
@router.post("/", status_code=status.HTTP_201_CREATED)
def createMeGusta(data: dict):

    user_id = data.get("user_id")
    lugar_id = data.get("lugar_id")

    if not user_id or not lugar_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "user_id y lugar_id requeridos")

    like = addMeGusta(user_id, lugar_id)

    if not like:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario o lugar no encontrado")

    return like.toDict()

# ==============================
# LISTAR LIKES
# ==============================
@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def getMeGusta(user_id: str):
    return getMeGustaUsuario(user_id)

# ==============================
# ELIMINAR LIKE
# ==============================
@router.delete("/", status_code=status.HTTP_200_OK)
def deleteMeGusta(data: dict):

    user_id = data.get("user_id")
    lugar_id = data.get("lugar_id")

    if not user_id or not lugar_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "user_id y lugar_id requeridos")

    deleted = removeMeGusta(user_id, lugar_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "El like no existía")

    return {"message": "Like eliminado correctamente"}