from pydantic import BaseModel
from typing import Optional

class PlaceDTO(BaseModel):
    id: str
    nombre: str
    dataset: str
    municipio: str
    acceso_silla_ruedas: Optional[str] = "No especificado"
    # Aquí puedes añadir más campos que quieras exponer siempre