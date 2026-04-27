#==============================
# Consultas sobre memgraph referente a Favorito
#==============================
from microservicio_memgraph.db.connection import run_query

# ==============================
# Favorito un lugar
# ==============================
def createFavorito(user_id, lugar_id):
    #No guardaremos de cuando es el favorito
    query = """
    MATCH (u:Usuario {id: $uid})
    MATCH (l:Lugar {id: $lid})
    MERGE (u)-[r:FAVORITO]->(l)
    RETURN l
    """

    result = run_query(query, {
        "uid": user_id,
        "lid": lugar_id
    })

    return result

# ==============================
# Lugares favoritos
# ==============================
def getFavoritosByUsuario(user_id):
    #Ordenamos por nombres
    query = """
    MATCH (u:Usuario {id: $uid})-[r:FAVORITO]->(l:Lugar)
    RETURN l
    ORDER BY l.name ASC
    """

    result = run_query(query, {"uid": user_id})
    return result

# ==============================
# Eliminar favorito
# ==============================
def deleteFavorito(user_id, lugar_id):
    query = """
    MATCH (u:Usuario {id: $uid})-[r:FAVORITO]->(l:Lugar {id: $lid})
    DELETE r
    RETURN count(r) AS deleted
    """

    result = run_query(query, {
        "uid": user_id,
        "lid": lugar_id
    })

    return result