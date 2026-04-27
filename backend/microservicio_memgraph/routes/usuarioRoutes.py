# ==============================
# Recupera las llamadas de las API, encia los datos al services
# ==============================
from fastapi import APIRouter, HTTPException, status
from microservicio_memgraph.services.usuarioService import ( 
    login, 
    signup,
    deleteUsuario
)

#Routas de api
router = APIRouter()

# ==============================
# LOGIN DE USUARIO
# ==============================
@router.post("/login", status_code=status.HTTP_200_OK)
def loginRoute(data: dict):
    email = data.get("email")
    password = data.get("password")

    # Fallo de datos
    if not email or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email y password requeridos")

    usuario = login(email, password)

    # Sin resultados
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")

    return usuario.toDict()

# ==============================
# SIGN UP
# ==============================
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signupRoute(data: dict):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Fallo de datos
    if not name or not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name, email y password requeridos"
        )

    usuario = signup(name, email, password)
    # Sin resultados (ya existe)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya existe"
        )

    return usuario.toDict()

# ==============================
# DELETE USER
# ==============================
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def deleteUsuarioRoute(user_id: str):

    deleteUsuario(user_id)

    return {
        "message": f"Usuario {user_id} eliminado correctamente"
    }