from pydantic import BaseModel, Field
from typing import List, Optional, Any

class GeometryModel(BaseModel):
    type: str
    coordinates: List[Any]  # MultiPolygon usa listas anidadas complejas

class FeatureModel(BaseModel):
    id: str = Field(alias="_id")
    rev: Optional[str] = Field(None, alias="_rev")
    type: str
    dataset: str  # "lonjas" o "parques"
    geometry: GeometryModel
    properties: dict  # Guardamos el diccionario crudo para máxima flexibilidad