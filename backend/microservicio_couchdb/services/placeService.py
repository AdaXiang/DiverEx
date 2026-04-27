from dao.placeDAO import PlaceDAO
from dto.placeDTO import PlaceDTO
from typing import Optional, List

class PlaceService:
    def __init__(self):
        self.dao = PlaceDAO()

    def get_site_details(self, site_id: str) -> PlaceDTO:
        data = self.dao.get_by_id(site_id)
        if not data:
            return None
        
        # Mapeo manual del modelo/dict al DTO
        return PlaceDTO(
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
            dto = PlaceDTO(
                id=item.get("_id"),
                nombre=props.get("nombre", "Sin nombre"),
                municipio=props.get("municipio_nombre", "Provincia de Badajoz"),
                dataset=item.get("dataset", "general"), 
                acceso_silla_ruedas=props.get("acceso_silla_ruedas", "NO")
            )
            results.append(dto)
        return results