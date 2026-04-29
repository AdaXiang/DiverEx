# ==============================
# Prepara o transforma los datos para DAO o SALIDA
# ==============================
from microservicio_memgraph.dao.lugarDao import *
from microservicio_memgraph.dto.lugarDto import LugarDto
import uuid

def mapLugar(l):
    return LugarDto(
        id=l["id"],
        name=l.get("name"),
        tipo=l.get("tipo"),
        estado=l.get("estado"),
        accesible=l.get("acceso_silla_ruedas"),
        media=l.get("media"),
        likes=l.get("likes"),
        agua=l.get("agua"),
        electricidad=l.get("electricidad"),
        comedor=l.get("comedor"),
        juegos=l.get("juegos_infantiles")
    )
    
# ==============================
# Crear lugar
# ==============================
def addLugar(data):
    result = createLugar(data)

    if not result:
        return None

    return mapLugar(result[0]["l"])
    
# ==============================
# Editar lugar
# ==============================
def editLugar(lugar_id, data):
    result = updateLugar(lugar_id, data)

    if not result:
        return None

    return mapLugar(result[0]["l"])
    
# ==============================
# Eliminar lugar
# ==============================
def removeLugar(lugar_id):
    result = deleteLugar(lugar_id)

    if not result:
        return False

    return result[0]["deleted"] > 0
    
# ==============================
# Obtener lugar
# ==============================
def getLugar(lugar_id):
    result = getLugarById(lugar_id)

    if not result:
        return None

    return mapLugar(result[0]["l"]).toDict()
    
# ==============================
# Obtener lugares
# ==============================
def getLugares():
    result = getAllLugares()

    return [mapLugar(r["l"]).toDict() for r in result]