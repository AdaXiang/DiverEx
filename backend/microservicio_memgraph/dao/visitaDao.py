#==============================
# Consultas sobre memgraph referente a Visita
#==============================
from microservicio_memgraph.db.connection import run_query

# ==============================
# Visitar un lugar
# ==============================
def createVisita(user_id, lugar_id):
    # Se busca que se visita o no, no queremos que puede visitarse varias veces
    query = """
    MATCH (u:Usuario {id: $uid})
    MATCH (l:Lugar {id: $lid})
    MERGE (u)-[:VISITA]->(l)
    ON CREATE SET r.fecha = datetime()
    RETURN l
    """

    result = run_query(query, {
        "uid": user_id,
        "lid": lugar_id
    })

    return result

# ==============================
# Lugares visitados
# ==============================
def getVisitasByUsuario(user_id):
    query = """
    MATCH (u:Usuario {id: $uid})-[r:VISITA]->(l:Lugar)
    RETURN l
    ORDER BY r.fecha DESC
    """

    result = run_query(query, {"uid": user_id})
    return result

# ==============================
# Eliminar visita
# ==============================
def deleteVisita(user_id, lugar_id):
    query = """
    MATCH (u:Usuario {id: $uid})-[r:VISITA]->(l:Lugar {id: $lid})
    DELETE r
    RETURN count(r) AS deleted
    """

    result = run_query(query, {
        "uid": user_id,
        "lid": lugar_id
    })

    return result