# ==============================
# Consultas sobre memgraph referente a ME_GUSTA
# ==============================
from microservicio_memgraph.db.connection import run_query

# ==============================
# Dar like a un lugar
# ==============================
def createMeGusta(user_id, lugar_id):
    query = """
    MATCH (u:Usuario {id: $uid})
    MATCH (l:Lugar {id: $lid})
    MERGE (u)-[r:ME_GUSTA]->(l)
    
    WITH l
    MATCH (l)<-[r2:ME_GUSTA]-()
    WITH l, count(r2) AS total
    SET l.likes = total
    
    RETURN l
    """

    result = run_query(query, {
        "uid": user_id,
        "lid": lugar_id
    })

    return result

# ==============================
# Lugares con like
# ==============================
def getMeGustaByUsuario(user_id):
    query = """
    MATCH (u:Usuario {id: $uid})-[r:ME_GUSTA]->(l:Lugar)
    RETURN l
    ORDER BY l.name ASC
    """

    result = run_query(query, {"uid": user_id})
    return result

# ==============================
# Eliminar like
# ==============================
def deleteMeGusta(user_id, lugar_id):
    query = """
    MATCH (u:Usuario {id: $uid})-[r:ME_GUSTA]->(l:Lugar {id: $lid})
    DELETE r

    WITH l, count(*) AS deleted

    OPTIONAL MATCH (l)<-[r2:ME_GUSTA]-()
    WITH l, deleted, count(r2) AS total
    SET l.likes = total

    RETURN deleted
    """

    return run_query(query, {
        "uid": user_id,
        "lid": lugar_id
    })
