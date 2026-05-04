# ==============================
# Prepara o transforma los datos para DAO o SALIDA
# ==============================
from microservicio_memgraph.dto.usuarioDto import UsuarioDto
from microservicio_memgraph.dao.usuarioDao import (
    getUsuarioByEmailAndPassword,
    createUsuario,
    getUsuarioByEmail,
    deleteUsuarioById
)
import uuid

# ==============================
# Inicio de sesion
# ==============================
def login(email, password):
    result = getUsuarioByEmailAndPassword(email, password)

    if not result:
        return None

    record = result[0] #Iterador del resultado
    userNode = record["u"] #Mucho cuidado, resultado RAW, recuperamos los datos que queremos

    usuario = UsuarioDto(
        id=userNode["id"],
        name=userNode["name"],
        email=userNode["email"]
    )

    return usuario

# ==============================
# SIGN UP
# ==============================
def signup(name, email, password):

    # Duplicidad de email
    existing = getUsuarioByEmail(email)

    if existing:
        return None  # usuario ya existe

    # Generar id
    user_id = str(uuid.uuid4())

    # Crear usuario
    result = createUsuario(user_id, name, email, password)

    record = result[0]
    userNode = record["u"]

    usuario = UsuarioDto(
        id=userNode["id"],
        name=userNode["name"],
        email=userNode["email"]
    )

    return usuario

# ==============================
# DELETE USER
# ==============================
def deleteUsuario(user_id):
    deleteUsuarioById(user_id)
    return True