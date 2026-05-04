# ==============================
# Lógica de negocio ME_GUSTA
# ==============================
from microservicio_memgraph.dao.meGustaDao import (
    createMeGusta,
    getMeGustaByUsuario,
    deleteMeGusta
)
from microservicio_memgraph.dto.lugarDto import LugarDto

# ==============================
# CREAR LIKE
# ==============================
def addMeGusta(user_id, lugar_id):
    result = createMeGusta(user_id, lugar_id)

    if not result:
        return None

    lugarNode = result[0]["l"]

    return LugarDto(
        id=lugarNode["id"],
        name=lugarNode.get("name"),
        tipo=lugarNode.get("tipo"),
        estado=lugarNode.get("estado"),
        accesible=lugarNode.get("acceso_silla_ruedas"),
        media=lugarNode.get("media"),
        likes=lugarNode.get("likes")
    )

# ==============================
# LISTAR LIKES
# ==============================
def getMeGustaUsuario(user_id):
    result = getMeGustaByUsuario(user_id)

    lugares = []

    for record in result:
        l = record["l"]

        lugares.append(
            LugarDto(
                id=l["id"],
                name=l.get("name"),
                tipo=l.get("tipo"),
                estado=l.get("estado"),
                accesible=l.get("acceso_silla_ruedas"),
                media=l.get("media"),
                likes=l.get("likes")
            ).toDict()
        )

    return lugares

# ==============================
# ELIMINAR LIKE
# ==============================
def removeMeGusta(user_id, lugar_id):
    result = deleteMeGusta(user_id, lugar_id)

    if not result:
        return False

    deleted = result[0]["deleted"]

    return deleted > 0