from pydantic import BaseModel
from typing import Any, Dict, Optional

class LugarDTO(BaseModel):
    id: str
    nombre: str
    dataset: str
    municipio: str
    codigo_provincia: str
    codigo_municipio: str
    estado: str
    acceso_silla_ruedas: bool
    titularidad: str
    gestion: str
    titularidad: str
    gestion: str
    superficie_cubierta: float
    tipo_lugar: str
    geo_point: Dict[str, Any]  # {"type": "Point", "coordinates": [lon, lat]}
    geometry: Dict[str, Any]
    superficie_aire: Optional[float] = None
    superficie_solar: Optional[float] = None
    agua: Optional[bool] = None
    saneamiento: Optional[bool] = None
    electricidad: Optional[bool] = None
    comedor: Optional[bool] = None
    juegos_infantiles: Optional[bool] = None
    otras_prestaciones: Optional[bool] = None
    distancia_km: Optional[float] = None
    