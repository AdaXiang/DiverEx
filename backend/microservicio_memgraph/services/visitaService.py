# ==============================
# Prepara o transforma los datos para DAO o SALIDA
# ==============================
from microservicio_memgraph.dao.visitaDao import (
    createVisita, 
    getVisitasByUsuario,
    deleteVisita
)
from microservicio_memgraph.dto.lugarDto import LugarDto

# ==============================
# CREAR VISITA
# ==============================
def addVisita(user_id, lugar_id):
    result = createVisita(user_id, lugar_id)

    #Si falla la visita
    if not result:
        return None

    #Mostramos el lugar que ha visitado, no se duplicara al ser mediante MERGE
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
# LISTAR VISITAS
# ==============================
def getVisitasUsuario(user_id):
    result = getVisitasByUsuario(user_id)
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
# Eliminar visita
# ==============================
def removeVisita(user_id, lugar_id):
    # resultado por el numero de relacion afectadas
    result = deleteVisita(user_id, lugar_id)

    if not result:
        return False

    deleted = result[0]["deleted"]

    return deleted > 0