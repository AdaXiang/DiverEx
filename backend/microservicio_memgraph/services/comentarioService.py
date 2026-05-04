# ==============================
# Prepara o transforma los datos para DAO o SALIDA
# ==============================
from microservicio_memgraph.dao.comentarioDao import (
    upsertComentario,
    getComentariosByUsuario,
    getComentariosByLugar,
    deleteComentario
)
from microservicio_memgraph.dto.comentarioDto import ComentarioDto
from microservicio_memgraph.dto.lugarDto import LugarDto
from microservicio_memgraph.dto.usuarioDto import UsuarioDto


# ==============================
# Crear o actualizar comentario
# ==============================
def saveComentario(user_id, lugar_id, mensaje, ranking):
    result = upsertComentario(user_id, lugar_id, mensaje, ranking)

    if not result:
        return None

    record = result[0]
    c = record["c"]
    l = record["l"]
    
    lugarDto = LugarDto(
        id=l["id"],
        name=l.get("name"),
        tipo=l.get("tipo"),
        estado=l.get("estado"),
        accesible=l.get("acceso_silla_ruedas"),
        media=l.get("media"),
        likes=l.get("likes")
    )

    return ComentarioDto(
        id=c["id"],
        mensaje=c["mensaje"],
        ranking=c["ranking"],
        fecha=str(c["fecha"]),
        lugar=lugarDto.toDict()
    )


# ==============================
# Comentarios de usuario
# ==============================
def getComentariosUsuario(user_id):
    result = getComentariosByUsuario(user_id)

    comentarios = []

    for r in result:
        c = r["c"]
        l = r["l"]
        
        lugarDto = LugarDto(
            id=l["id"],
            name=l.get("name"),
            tipo=l.get("tipo"),
            estado=l.get("estado"),
            accesible=l.get("acceso_silla_ruedas"),
            media=l.get("media"),
            likes=l.get("likes")
        )

        comentarios.append(
            ComentarioDto(
                id=c["id"],
                mensaje=c["mensaje"],
                ranking=c["ranking"],
                fecha=str(c["fecha"]),
                lugar=lugarDto.toDict()
            ).toDict()
        )

    return comentarios


# ==============================
# Comentarios de lugar
# ==============================
def getComentariosLugar(lugar_id, ranking_min=None, ranking_max=None):
    result = getComentariosByLugar(lugar_id,ranking_min,ranking_max)

    comentarios = []

    for r in result:
        c = r["c"]
        u = r["u"]

        usuarioDto = UsuarioDto(
            id=u["id"],
            name=u.get("name"),
            email=u.get("email")
        )

        comentarios.append(
            ComentarioDto(
                id=c["id"],
                mensaje=c["mensaje"],
                ranking=c["ranking"],
                fecha=str(c["fecha"]),
                usuario=usuarioDto.toDict()
            ).toDict()
        )

    return comentarios


# ==============================
# Eliminar comentario
# ==============================
def removeComentario(user_id, lugar_id):
    result = deleteComentario(user_id, lugar_id)

    if not result:
        return False

    return result[0]["deleted"] > 0