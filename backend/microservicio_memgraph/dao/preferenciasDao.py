# ==============================
# Consultas sobre preferencias
# ==============================
from microservicio_memgraph.db.connection import run_query

# ==============================
# RECOMENDACIONES
# ==============================
def getRecomendaciones(user_id):
    #Devolver lugares de usuarios con gustos similares a user_id, los cuales no haya visitado
    query = """
    MATCH (u:Usuario {id: $uid})-[:FAVORITO|VISITA]->(l:Lugar)<-[:FAVORITO|VISITA]-(other:Usuario)
    MATCH (other)-[:FAVORITO|VISITA]->(rec:Lugar)
    WHERE NOT (u)-[:VISITA]->(rec)
    RETURN DISTINCT rec
    ORDER BY rec.media DESC, rec.likes DESC
    LIMIT 20
    """
    return run_query(query, {"uid": user_id})

# ==============================
# RECOMENDACIONES FILTRADAS
# ==============================
def getRecomendacionesFiltradas(user_id, filtros):
    query = f"""
    MATCH (u:Usuario {{id: $uid}})-[:FAVORITO|VISITA]->(l:Lugar)<-[:FAVORITO|VISITA]-(other:Usuario)
    MATCH (other)-[:FAVORITO|VISITA]->(rec:Lugar)
    WHERE NOT (u)-[:VISITA]->(rec)
    """

    params = {"uid": user_id}

    # reemplazamos MATCH de rec por si filtra por el tipo de lugar
    query = query.replace("MATCH (other)-[:FAVORITO|VISITA]->(rec:Lugar)", f"MATCH (other)-[:FAVORITO|VISITA]->(rec{':' + filtros['tipo'] if filtros.get('tipo') in ['Parque','Lonja'] else ':Lugar'})")

    if filtros.get("estado"):
        query += " AND rec.estado = $estado"
        params["estado"] = filtros["estado"]

    if filtros.get("accesible") is not None:
        query += " AND rec.acceso_silla_ruedas = $accesible"
        params["accesible"] = filtros["accesible"]

    if filtros.get("codigo_municipio"):
        query += " AND rec.codigo_municipio = $codigo"
        params["codigo"] = filtros["codigo_municipio"]

    if filtros.get("tipo_detalle"):
        query += " AND rec.tipo = $tipo_detalle"
        params["tipo_detalle"] = filtros["tipo_detalle"]

    if filtros.get("agua") is not None:
        query += " AND rec.agua = $agua"
        params["agua"] = filtros["agua"]

    if filtros.get("electricidad") is not None:
        query += " AND rec.electricidad = $electricidad"
        params["electricidad"] = filtros["electricidad"]

    if filtros.get("comedor") is not None:
        query += " AND rec.comedor = $comedor"
        params["comedor"] = filtros["comedor"]

    if filtros.get("juegos") is not None:
        query += " AND rec.juegos_infantiles = $juegos"
        params["juegos"] = filtros["juegos"]
        
    if filtros.get("media_min") is not None:
        query += " AND rec.media >= $media_min"
        params["media_min"] = filtros["media_min"]

    if filtros.get("media_max") is not None:
        query += " AND rec.media <= $media_max"
        params["media_max"] = filtros["media_max"]

    query += """
    RETURN DISTINCT rec
    ORDER BY rec.media DESC, rec.likes DESC
    LIMIT 20
    """

    return run_query(query, params)

# ==============================
# TOP LUGARES (con filtros)
# ==============================
def getTopLugares(filtros):

    label = "Lugar"

    if filtros.get("tipo") in ["Parque", "Lonja"]:
        label = f"Lugar:{filtros['tipo']}"

    query = f"""
    MATCH (l:{label})
    WHERE l.media IS NOT NULL
    """

    params = {}

    if filtros.get("codigo_municipio"):
        query += " AND l.codigo_municipio = $codigo"
        params["codigo"] = filtros["codigo_municipio"]

    if filtros.get("tipo_detalle"):
        query += " AND l.tipo = $tipo_detalle"
        params["tipo_detalle"] = filtros["tipo_detalle"]

    query += """
    RETURN l
    ORDER BY rec.media DESC, rec.likes DESC
    LIMIT 20
    """

    return run_query(query, params)
