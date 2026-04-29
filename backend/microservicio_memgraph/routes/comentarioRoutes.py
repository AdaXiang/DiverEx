# ==============================
# Recupera las llamadas de las API
# ==============================
from fastapi import APIRouter, HTTPException, status
from microservicio_memgraph.services.comentarioService import (
    saveComentario,
    getComentariosUsuario,
    getComentariosLugar,
    removeComentario
)

router = APIRouter(tags=["Comentario"])

# ==============================
# CREAR / EDITAR COMENTARIO
# ==============================
@router.post("/", status_code=status.HTTP_201_CREATED)
def createComentario(data: dict):

    user_id = data.get("user_id")
    lugar_id = data.get("lugar_id")
    mensaje = data.get("mensaje")
    ranking = data.get("ranking")

    if not all([user_id, lugar_id, mensaje, ranking]):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Datos incompletos")

    comentario = saveComentario(user_id, lugar_id, mensaje, ranking)

    if not comentario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario o lugar no encontrado")

    return comentario.toDict()


# ==============================
# COMENTARIOS DE USUARIO
# ==============================
@router.get("/usuario/{user_id}", status_code=status.HTTP_200_OK)
def comentariosUsuario(user_id: str):
    return getComentariosUsuario(user_id)


# ==============================
# COMENTARIOS DE LUGAR
# ==============================
@router.get("/lugar/{lugar_id}", status_code=status.HTTP_200_OK)
def comentariosLugar(
    lugar_id: str,
    ranking_min: int | None = None,
    ranking_max: int | None = None
):
    return getComentariosLugar(lugar_id, ranking_min, ranking_max)


# ==============================
# ELIMINAR COMENTARIO
# ==============================
@router.delete("/", status_code=status.HTTP_200_OK)
def deleteComentario(data: dict):

    user_id = data.get("user_id")
    lugar_id = data.get("lugar_id")

    if not user_id or not lugar_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Datos incompletos")

    deleted = removeComentario(user_id, lugar_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Comentario no encontrado")

    return {"message": "Comentario eliminado"}