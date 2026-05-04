# ==============================
# Prepara o transforma los datos para DAO o SALIDA
# ==============================
from microservicio_memgraph.dao.favoritoDao import (
    createFavorito, 
    getFavoritosByUsuario,
    deleteFavorito
)
from microservicio_memgraph.dto.lugarDto import LugarDto

# ==============================
# CREAR Favorito
# ==============================
def addFavorito(user_id, lugar_id):
    result = createFavorito(user_id, lugar_id)

    #Si falla la consulta
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
# LISTAR FAVORITOS
# ==============================
def getFavoritosUsuario(user_id):
    result = getFavoritosByUsuario(user_id)
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
# Eliminar favorito
# ==============================
def removeFavorito(user_id, lugar_id):
    # resultado por el numero de relaciones afectadas
    result = deleteFavorito(user_id, lugar_id)

    if not result:
        return False

    deleted = result[0]["deleted"]

    return deleted > 0