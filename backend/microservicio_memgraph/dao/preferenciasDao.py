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
    query = """
    MATCH (u:Usuario {id: $uid})-[:FAVORITO|VISITA]->(l:Lugar)<-[:FAVORITO|VISITA]-(other:Usuario)
    MATCH (other)-[:FAVORITO|VISITA]->(rec:Lugar)
    """

    # Recomendaciones genericas
    params = { "uid": user_id }

    conditions = [ "NOT (u)-[:VISITA]->(rec)" ]

    # ==========================================
    # FILTRO POR LABEL (Optimizar busqueda por label)
    # ==========================================
    tipos_validos = [
        t for t in (filtros.get("tipo") or [])
        if t in ["Parque", "Lonja"]
    ]

    # Solo filtramos por label si hay uno único
    if len(tipos_validos) == 1:

        query = query.replace(
            "(rec:Lugar)",
            f"(rec:{tipos_validos[0]})"
        )

    # ==========================================
    # ESTADO
    # ==========================================
    if filtros.get("estado"):

        conditions.append(
            "rec.estado IN $estado"
        )

        params["estado"] = filtros["estado"]

    # ==========================================
    # ACCESIBILIDAD
    # ==========================================
    if filtros.get("accesible") is not None:

        conditions.append(
            "rec.acceso_silla_ruedas = $accesible"
        )

        params["accesible"] = filtros["accesible"]

    # ==========================================
    # MUNICIPIO
    # ==========================================
    if filtros.get("codigo_municipio"):

        conditions.append(
            "rec.codigo_municipio = $codigo"
        )

        params["codigo"] = filtros["codigo_municipio"]

    # ==========================================
    # TIPO DETALLE
    # ==========================================
    if filtros.get("tipo_detalle"):

        conditions.append(
            "rec.tipo IN $tipo_detalle"
        )

        params["tipo_detalle"] = filtros["tipo_detalle"]

    # ==========================================
    # AGUA
    # ==========================================
    if filtros.get("agua") is not None:

        conditions.append(
            "rec.agua = $agua"
        )

        params["agua"] = filtros["agua"]

    # ==========================================
    # ELECTRICIDAD
    # ==========================================
    if filtros.get("electricidad") is not None:

        conditions.append(
            "rec.electricidad = $electricidad"
        )

        params["electricidad"] = filtros["electricidad"]

    # ==========================================
    # COMEDOR
    # ==========================================
    if filtros.get("comedor") is not None:

        conditions.append(
            "rec.comedor = $comedor"
        )

        params["comedor"] = filtros["comedor"]

    # ==========================================
    # JUEGOS INFANTILES
    # ==========================================
    if filtros.get("juegos") is not None:

        conditions.append(
            "rec.juegos_infantiles = $juegos"
        )

        params["juegos"] = filtros["juegos"]

    # ==========================================
    # MEDIA MÍNIMA
    # ==========================================
    if filtros.get("media_min") is not None:

        conditions.append(
            "rec.media >= $media_min"
        )

        params["media_min"] = filtros["media_min"]

    # ==========================================
    # MEDIA MÁXIMA
    # ==========================================
    if filtros.get("media_max") is not None:

        conditions.append(
            "rec.media <= $media_max"
        )

        params["media_max"] = filtros["media_max"]

    # ==========================================
    # CONSTRUCCIÓN FINAL DEL WHERE
    # ==========================================
    if conditions:

        query += "\nWHERE " + "\nAND ".join(conditions)

    # ==========================================
    # QUERY FINAL
    # ==========================================
    query += """

    RETURN DISTINCT rec

    ORDER BY
        rec.media DESC,
        rec.likes DESC

    LIMIT 20
    """

    return run_query(query, params)

# ==============================
# TOP LUGARES (con filtros)
# ==============================
def getTopLugares(filtros):

    query = """
    MATCH (l:Lugar)
    """

    params = {}

    conditions = [
        "l.media IS NOT NULL"
    ]

    # ==========================================
    # LABELS
    # ==========================================
    tipos_validos = [
        t for t in (filtros.get("tipo") or [])
        if t in ["Parque", "Lonja"]
    ]

    # Solo optimizamos si hay uno único
    if len(tipos_validos) == 1:

        query = query.replace(
            "(l:Lugar)",
            f"(l:{tipos_validos[0]})"
        )

    # ==========================================
    # MUNICIPIO
    # ==========================================
    if filtros.get("codigo_municipio"):

        conditions.append(
            "l.codigo_municipio = $codigo"
        )

        params["codigo"] = filtros["codigo_municipio"]

    # ==========================================
    # TIPO DETALLE
    # ==========================================
    if filtros.get("tipo_detalle"):

        conditions.append(
            "l.tipo IN $tipo_detalle"
        )

        params["tipo_detalle"] = filtros["tipo_detalle"]

    # ==========================================
    # WHERE FINAL
    # ==========================================
    if conditions:

        query += "\nWHERE " + "\nAND ".join(conditions)

    # ==========================================
    # RETURN
    # ==========================================
    query += """

    RETURN l

    ORDER BY
        l.media DESC,
        l.likes DESC

    LIMIT 20
    """

    return run_query(query, params)
