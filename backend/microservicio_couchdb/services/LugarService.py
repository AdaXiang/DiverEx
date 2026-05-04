from dotenv import load_dotenv

from dao.LugarDAO import LugarDAO
from dto.LugarDTO import LugarDTO
from typing import Optional, List
import os

class LugarService:

    def __init__(self):
        load_dotenv()
        print(os.getenv("COUCHBASE_HOST"))
        print(os.getenv("COUCHBASE_USER"))
        self.dao = LugarDAO(
            host=os.getenv("COUCHBASE_HOST"),
            user=os.getenv("COUCHBASE_USER"),
            password=os.getenv("COUCHBASE_PASSWORD"),
            bucket=os.getenv("COUCHBASE_BUCKET")
        )

    def get_site_details(self, site_id: str) -> LugarDTO:
        data = self.dao.get_by_id(site_id)
        if not data:
            return None
        
        # Mapeo manual del modelo/dict al DTO
        return LugarDTO(
            id=data["_id"],
            nombre=data["properties"].get("nombre", "Sin nombre"),
            dataset=data["dataset"],
            municipio=data["properties"].get("municipio_nombre", "Desconocido"),
            acceso_silla_ruedas=data["properties"].get("acceso_silla_ruedas")
        )
    
    def get_all_places(self, category: Optional[str] = None):
        raw_data = self.dao.list_all(category)
        results = []
        
        for item in raw_data:
            props = item.get("properties", {})
            
            # Creamos el DTO asegurándonos de que CADA nombre coincida con el DTO
            dto = LugarDTO(
                id=item.get("_id"),
                nombre=props.get("nombre", "Sin nombre"),
                municipio=props.get("municipio_nombre", "Provincia de Badajoz"),
                dataset=item.get("dataset", "general"), 
                acceso_silla_ruedas=props.get("acceso_silla_ruedas", "NO")
            )
            results.append(dto)
        return results