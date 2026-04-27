# ==============================
# Consultas sobre Comentarios
# ==============================
from microservicio_memgraph.db.connection import run_query

# ==============================
# Crear o actualizar comentario
# ==============================
def upsertComentario(user_id, lugar_id, mensaje, ranking):
    query = """
    MATCH (u:Usuario {id: $uid})
    MATCH (l:Lugar {id: $lid})

    MERGE (c:Comentario {id: $cid})
    ON CREATE SET 
        c.mensaje = $mensaje,
        c.ranking = $ranking,
        c.fecha = datetime()
    ON MATCH SET 
        c.mensaje = $mensaje,
        c.ranking = $ranking,
        c.fecha = datetime()

    MERGE (u)-[:ESCRIBE]->(c)
    MERGE (c)-[:SOBRE]->(l)

    WITH l
    MATCH (l)<-[:SOBRE]-(c2:Comentario)
    WITH l, AVG(c2.ranking) AS media
    SET l.media = media

    RETURN c,l
    """

    return run_query(query, {
        "uid": user_id,
        "lid": lugar_id,
        "cid": f"{user_id}_{lugar_id}",
        "mensaje": mensaje,
        "ranking": ranking
    })

# ==============================
# Comentarios de un usuario
# ==============================
def getComentariosByUsuario(user_id):
    query = """
    MATCH (u:Usuario {id: $uid})-[:ESCRIBE]->(c:Comentario)-[:SOBRE]->(l:Lugar)
    RETURN c, l
    ORDER BY c.fecha DESC
    """
    return run_query(query, {"uid": user_id})


# ==============================
# Comentarios de un lugar
# ==============================
def getComentariosByLugar(lugar_id, ranking_min=None, ranking_max=None):
    query = """
    MATCH (l:Lugar {id: $lid})<-[:SOBRE]-(c:Comentario)<-[:ESCRIBE]-(u:Usuario)
    WHERE 1=1
    """

    params = {"lid": lugar_id}

    if ranking_min is not None:
        query += " AND c.ranking >= $ranking_min"
        params["ranking_min"] = ranking_min

    if ranking_max is not None:
        query += " AND c.ranking <= $ranking_max"
        params["ranking_max"] = ranking_max

    query += """
    RETURN c, u
    ORDER BY c.fecha DESC
    """

    return run_query(query, params)


# ==============================
# Eliminar comentario
# ==============================
def deleteComentario(user_id, lugar_id):
    query = """
    MATCH (l:Lugar {id: $lid})
    OPTIONAL MATCH (c:Comentario {id: $cid})
    WITH l, c

    DETACH DELETE c

    WITH l, c
    OPTIONAL MATCH (l)<-[:SOBRE]-(c2:Comentario)
    WITH l, c, AVG(c2.ranking) AS media
    SET l.media = media

    RETURN c IS NOT NULL AS deleted
    """

    return run_query(query, {
        "cid": f"{user_id}_{lugar_id}",
        "lid": lugar_id
    })