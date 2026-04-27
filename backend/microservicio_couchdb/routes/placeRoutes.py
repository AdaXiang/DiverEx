from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from services.placeService import PlaceService
from dto.placeDTO import PlaceDTO

router = APIRouter()
service = PlaceService()

@router.get("/sitio/{site_id}", response_model=PlaceDTO)
async def read_site(site_id: str):
    site = service.get_site_details(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    return site

@router.get("/lugares", response_model=List[PlaceDTO])
async def get_lugares(dataset: Optional[str] = Query(None, description="Filtrar por 'parques' o 'lonjas'")):
    """
    Retorna la lista entera de sitios de interés en la provincia de Badajoz.
    """
    return service.get_all_places(dataset)