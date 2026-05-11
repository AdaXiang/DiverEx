from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from services.LugarService import LugarService
from dto.LugarDTO import LugarDTO

router = APIRouter()
service = LugarService()

# Función para convertir una lista de DTOs a GeoJSON
def to_geojson(items):
    features = []
    
    for item in items:
        if hasattr(item, "model_dump"):
            data = item.model_dump(exclude_none=True)
        else:
            data = {k: v for k, v in item.items() if v is not None}
        
        geometry = data.pop("geometry", None)
        geo_point = data.pop("geo_point", None)
        
        feature = {
            "type": "Feature",
            "geo_point": geo_point,  
            "geometry": geometry,
            "properties": data
        }
        features.append(feature)
        
    return {
        "type": "FeatureCollection",
        "features": features
    }

@router.get("/lugares/filtrar")
async def filter_lugares(
    lat: Optional[float] = Query(None, description="Latitud del usuario"),
    lon: Optional[float] = Query(None, description="Longitud del usuario"),
    distancia_max: Optional[float] = Query(None, description="Distancia máxima en km"),
    acceso_silla_ruedas: Optional[bool] = Query(None),
    zona_infantil: Optional[bool] = Query(None),
    comedor: Optional[bool] = Query(None),
    tipo_lugar: Optional[List[str]] = Query(None),
    estado: Optional[List[str]] = Query(None),
    nombre: Optional[str] = Query(None),
    municipio: Optional[str] = Query(None),
):
    # Pasamos TODOS los parámetros a la función maestra
    items =  service.search_places(
        lat=lat, lon=lon, distancia_max=distancia_max,
        acceso_silla_ruedas=acceso_silla_ruedas, zona_infantil=zona_infantil,
        comedor=comedor, tipos=tipo_lugar, estados=estado,
        nombre=nombre, municipio=municipio
    )
    return to_geojson(items)

#------------------------------
# Endpoint para filtro geoespacial
#------------------------------
@router.get("/lugares/geoespacial", response_model=List[LugarDTO])
async def geospatial_filter(
    lat: float = Query(..., description="Latitud del punto central"),
    lon: float = Query(..., description="Longitud del punto central"),
    radius: float = Query(1000, description="Radio en metros para el filtro geoespacial")
):
    """
    Endpoint para filtrar sitios dentro de un radio específico desde un punto geográfico.
    """
    return service.search_by_location(lat, lon, radius)


#-----------------------------
# CREATE, UPDATE, DELETE
#-----------------------------
@router.post("/lugares/", response_model=List[LugarDTO])
async def create_lugar(lugar: LugarDTO):
    """
    Endpoint para crear un nuevo sitio de interés.
    """
    return service.create_place(lugar)

@router.put("/lugares/{site_id}", response_model=LugarDTO)
async def update_lugar(site_id: str, lugar: LugarDTO):
    """
    Endpoint para actualizar un sitio de interés existente.
    """
    updated_place = service.update_place(site_id, lugar)
    if not updated_place:
        raise HTTPException(status_code=404, detail="Sitio no encontrado para actualizar")
    return updated_place.model_dump(exclude_none=True)

@router.delete("/lugares/{site_id}")
async def delete_lugar(site_id: str):
    """
    Endpoint para eliminar un sitio de interés por su ID.
    """
    success = service.delete_place(site_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sitio no encontrado para eliminar")
    return {"detail": "Sitio eliminado exitosamente"}

#-----------------------------
# READ
#-----------------------------
@router.get("/lugares")
async def get_lugares(
    dataset: Optional[str] = Query(None, description="Filtrar por 'parques' o 'lonjas'")
    ):
    """
    Retorna la lista entera de sitios de interés en la provincia de Badajoz.
    """
    items = service.get_all_places(dataset)
    return to_geojson(items)



@router.get("/sitio/{site_id}", response_model=LugarDTO)
async def read_site(site_id: str):
    site = service.get_site_details(site_id)
    print(type(site))
    if not site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    return site.model_dump(exclude_none=True)