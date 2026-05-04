#==============================
# Consultas sobre memgraph referente a Usuarios
#==============================
from microservicio_memgraph.db.connection import run_query

# ==============================
# Inicio de sesion
# ==============================
def getUsuarioByEmailAndPassword(email, password):
    query = """
    MATCH (u:Usuario {email: $email, password: $password})
    RETURN u
    LIMIT 1
    """

    # Empleamos funcion auxiliar y modulada para memgraph
    result = run_query(query, {
        "email": email,
        "password": password
    })

    return result

# ==============================
# Crear usuario
# ==============================
def createUsuario(id, name, email, password):
    query = """
    CREATE (u:Usuario {
        id: $id,
        name: $name,
        email: $email,
        password: $password
    })
    RETURN u
    """

    result = run_query(query, {
        "id": id,
        "name": name,
        "email": email,
        "password": password
    })

    return result


# ==============================
# Buscar por email (para validar duplicados, no deberia ser posible ya que se controla con reglas en base la base de datos)
# ==============================
def getUsuarioByEmail(email):
    query = """
    MATCH (u:Usuario {email: $email})
    RETURN u
    LIMIT 1
    """

    result = run_query(query, {
        "email": email
    })

    return result

# ==============================
# Eliminar usuario
# ==============================
def deleteUsuarioById(user_id):
    # Con match de usuario solo eliminaria el usuario y sus relaciones, el nodo de sus comentarios NO
    # Con optional match, borramos los comentarios del usuario
    query = """
    MATCH (u:Usuario {id: $id})
    OPTIONAL MATCH (u)-[:ESCRIBE]->(c:Comentario)
    DETACH DELETE u, c
    """

    run_query(query, {"id": user_id})