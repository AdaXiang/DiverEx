# ==============================
# Recupera las llamadas de las API
# ==============================
from fastapi import APIRouter, HTTPException, status
from microservicio_memgraph.services.favoritoService import (
    addFavorito, 
    getFavoritosUsuario,
    removeFavorito
)

router = APIRouter(tags=["Favorito"])

# ==============================
# FAVORITO LUGAR
# ==============================
@router.post("/", status_code=status.HTTP_201_CREATED)
def createFavorito(data: dict):

    user_id = data.get("user_id")
    lugar_id = data.get("lugar_id")

    if not user_id or not lugar_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "user_id y lugar_id requeridos")

    favorito = addFavorito(user_id, lugar_id)
    if not favorito:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario o lugar no encontrado")

    return favorito.toDict()

# ==============================
# LUGARES FAVORITOS
# ==============================
@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def getFavoritos(user_id: str):
    favoritos = getFavoritosUsuario(user_id)

    return favoritos

# ==============================
# ELIMINAR FAVORITO
# ==============================
@router.delete("/", status_code=status.HTTP_200_OK)
def deleteFavorito(data: dict):
    user_id = data.get("user_id")
    lugar_id = data.get("lugar_id")

    if not user_id or not lugar_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "user_id y lugar_id requeridos")

    deleted = removeFavorito(user_id, lugar_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "El favorito no existía")

    return {"message": "Favorito eliminada correctamente"}