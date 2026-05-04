# ==============================
# Lógica de negocio para consulta entre arcos
# ==============================
from microservicio_memgraph.dao.preferenciasDao import *
from microservicio_memgraph.dto.lugarDto import LugarDto
from microservicio_memgraph.dto.usuarioDto import UsuarioDto


def mapLugar(l):
    return LugarDto(
        id=l["id"],
        name=l.get("name"),
        tipo=l.get("tipo"),
        estado=l.get("estado"),
        accesible=l.get("acceso_silla_ruedas"),
        media=l.get("media"),
        likes=l.get("likes")
    ).toDict()


# ==============================
# RECOMENDACIONES
# ==============================
def recomendaciones(user_id):
    result = getRecomendaciones(user_id)
    return [mapLugar(r["rec"]) for r in result]


def recomendacionesFiltradas(user_id, filtros):
    result = getRecomendacionesFiltradas(user_id, filtros)
    return [mapLugar(r["rec"]) for r in result]


# ==============================
# TOP
# ==============================
def topLugares(filtros):
    result = getTopLugares(filtros)
    return [mapLugar(r["l"]) for r in result]