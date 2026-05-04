#==============================
# Consultas sobre memgraph referente a Lugar (solo interaccion o preferencais)
#==============================
from microservicio_memgraph.db.connection import run_query

# ==============================
# Crear lugar
# ==============================
def createLugar(data):
    tipo = data["tipo"]

    query = f"""
    MERGE (l:Lugar:{tipo} {{
        id: $id
    }})
    SET l.name = $name,
        l.codigo_municipio = $codigo,
        l.estado = $estado,
        l.acceso_silla_ruedas = $accesible,
        l.tipo = $tipo_detalle,
        l.likes = 0,
        l.media = 0
    """

    if tipo == "Parque":
        query += """
        SET l.agua = $agua,
            l.electricidad = $electricidad,
            l.comedor = $comedor,
            l.juegos_infantiles = $juegos
        """

    query += " RETURN l"

    return run_query(query, data)

# ==============================
# Obtener un lugar
# ==============================
def getLugarById(lugar_id):
    query = """
    MATCH (l:Lugar {id: $id})
    RETURN l
    LIMIT 1
    """

    return run_query(query, {"id": lugar_id})

# ==============================
# Obtener un lugares
# ==============================
def getAllLugares():
    query = """
    MATCH (l:Lugar)
    RETURN l
    """

    return run_query(query)

# ==============================
# Actualiza lugar (necesario para las preferencias)
# ==============================
def updateLugar(lugar_id, data):
    tipo = data.get("tipo")  # opcional

    query = """
    MATCH (l:Lugar {id: $id})
    SET l.name = $name,
        l.codigo_municipio = $codigo,
        l.estado = $estado,
        l.acceso_silla_ruedas = $accesible,
        l.tipo = $tipo_detalle
    """

    if tipo == "Parque":
        query += """
        SET l.agua = $agua,
            l.electricidad = $electricidad,
            l.comedor = $comedor,
            l.juegos_infantiles = $juegos
        """

    query += " RETURN l"

    data["id"] = lugar_id

    return run_query(query, data)

# ==============================
# Elimina lugar (junto a todas sus relaciones)
# ==============================
def deleteLugar(lugar_id):
    query = """
    MATCH (l:Lugar {id: $id})
    DETACH DELETE l
    RETURN count(l) AS deleted
    """

    return run_query(query, {"id": lugar_id})


