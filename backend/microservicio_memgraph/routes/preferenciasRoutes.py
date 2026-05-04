# ==============================
# API RELACION ARCOS
# ==============================
from fastapi import APIRouter, HTTPException, status
from microservicio_memgraph.services.preferenciasService import *

router = APIRouter(tags=["Preferencias"])

# ==============================
# RECOMENDACIONES
# ==============================
@router.get("/recomendaciones/{user_id}", status_code=status.HTTP_200_OK)
def getRecomendacionesRoute(user_id: str):
    # Fallo de datos
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id requerido")
    
    return recomendaciones(user_id)

# ==============================
# RECOMENDACIONES FILTRADAS
# ==============================
@router.get("/recomendaciones-filtradas/{user_id}", status_code=status.HTTP_200_OK)
def getRecomendacionesFiltradasRoute(
    user_id: str,
    tipo: str = None,
    estado: str = None,
    accesible: bool = None,
    codigo_municipio: str = None,
    tipo_detalle: str = None,
    agua: bool = None,
    electricidad: bool = None,
    comedor: bool = None,
    juegos: bool = None,
    media_min: int = None,
    media_max: int = None
):
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id requerido")

    filtros = {
        "tipo": tipo,
        "estado": estado,
        "accesible": accesible,
        "codigo_municipio": codigo_municipio,
        "tipo_detalle": tipo_detalle,
        "agua": agua,
        "electricidad": electricidad,
        "comedor": comedor,
        "juegos": juegos,
        "media_min": media_min,
        "media_max": media_max
    }

    return recomendacionesFiltradas(user_id, filtros)


# ==============================
# TOP LUGARES
# ==============================
@router.get("/top", status_code=status.HTTP_200_OK)
def getTopRoute(
    tipo: str = None,
    codigo_municipio: str = None,
    tipo_detalle: str = None
):
    filtros = {
        "tipo": tipo,
        "codigo_municipio": codigo_municipio,
        "tipo_detalle": tipo_detalle
    }

    return topLugares(filtros)