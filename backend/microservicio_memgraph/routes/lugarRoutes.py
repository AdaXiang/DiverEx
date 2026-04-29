# ==============================
# Recupera las llamadas de las API
# ==============================
from fastapi import APIRouter, HTTPException, status
from microservicio_memgraph.services.lugarService import *

router = APIRouter(tags=["Lugar"])

# ==============================
# CREAR LUGAR
# ==============================
@router.post("/", status_code=status.HTTP_201_CREATED)
def createLugarRoute(data: dict):
    
    if data["tipo"] not in ["Parque", "Lonja"]:
        raise HTTPException(400, "Tipo inválido")
    
    required_fields = ["id", "tipo", "name", "codigo", "estado", "accesible", "tipo_detalle"]

    for field in required_fields:
        if field not in data:
            raise HTTPException(
                status_code=400,
                detail=f"Falta campo obligatorio: {field}"
            )

    lugar = addLugar(data)

    if not lugar:
        raise HTTPException(status_code=400, detail="Error al crear lugar")

    return lugar.toDict()

# ==============================
# EDITAR LUGAR
# ==============================
@router.put("/{lugar_id}", status_code=status.HTTP_200_OK)
def updateLugarRoute(lugar_id: str, data: dict):

    lugar = editLugar(lugar_id, data)

    if not lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")

    return lugar.toDict()

# ==============================
# ELIMINAR LUGAR
# ==============================
@router.delete("/{lugar_id}", status_code=status.HTTP_200_OK)
def deleteLugarRoute(lugar_id: str):

    deleted = removeLugar(lugar_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")

    return {"message": "Lugar eliminado"}

# ==============================
# OBTENER LUGAR
# ==============================
@router.get("/{lugar_id}", status_code=status.HTTP_200_OK)
def getLugarRoute(lugar_id: str):

    lugar = getLugar(lugar_id)

    if not lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")

    return lugar

# ==============================
# OBTENER LUGARES
# ==============================
@router.get("/", status_code=status.HTTP_200_OK)
def getAllLugaresRoute():
    return getLugares()