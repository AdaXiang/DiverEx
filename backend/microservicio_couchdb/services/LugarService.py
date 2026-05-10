from dotenv import load_dotenv

from dao.LugarDAO import LugarDAO
from dto.LugarDTO import LugarDTO
from typing import Optional, List
import os

class LugarService:

    def __init__(self):
        load_dotenv()
        self.dao = LugarDAO(
            host=os.getenv("COUCHBASE_HOST"),
            user=os.getenv("COUCHBASE_USER"),
            password=os.getenv("COUCHBASE_PASSWORD"),
            bucket=os.getenv("COUCHBASE_BUCKET")
        )

    # Devuelve un lugar específico por su ID, mapeado a un DTO
    def get_site_details(self, site_id: str) -> LugarDTO:
        data = self.dao.get_by_id(site_id)
        if not data:
            return None
        
        props = data.get("properties", {})
        geo_point = data.get("geo_point", {})  # Extraemos el punto central
        
        payload = {
            "id": data["_id"],
            "nombre": props.get("nombre", "Sin nombre"),
            "dataset": data.get("dataset", "Desconocido"),
            "municipio": props.get("municipio_nombre", "Desconocido"),
            
            # Mapeo de Geografía
            "lat": geo_point.get("lat"),
            "lon": geo_point.get("lon"),
            "geometry": data.get("geometry"), # Pasamos el objeto MultiPolygon completo
            
            # Campos base
            "codigo_provincia": props.get("codigo_provincia"),
            "codigo_municipio": props.get("codigo_municipio"),
            "estado": props.get("estado"),
            "titularidad": props.get("titularidad"),
            "gestion": props.get("gestion"),
            "superficie_cubierta": props.get("superficie_cubierta")
        }

        # Campos opcionales (Booleanos y superficies)
        campos_opcionales = [
            "acceso_silla_ruedas", "tipo_lonja", "superficie_aire", 
            "superficie_solar", "tipo_parque", "agua", "saneamiento", 
            "electricidad", "comedor", "juegos_infantiles", "otras_prestaciones"
        ]

        for campo in campos_opcionales:
            if campo in props:
                payload[campo] = props[campo]

        return LugarDTO(**payload)
    
    # Devuelve una lista de lugares, opcionalmente filtrada por categoría (dataset)
    def get_all_places(self, category: Optional[str] = None):
        raw_data = self.dao.list_all(category)
        results = []
        
        for item in raw_data:
            props = item.get("properties", {})
            geo_point = item.get("geo_point", {})  # Extraemos el punto central
            
            # Creamos el DTO asegurándonos de que CADA nombre coincida con el DTO
            dto = LugarDTO(
                id=item.get("_id"),
                nombre=props.get("nombre", "Sin nombre"),
                municipio=props.get("municipio_nombre", "Provincia de Badajoz"),
                dataset=item.get("dataset", "general"), 
                acceso_silla_ruedas=props.get("acceso_silla_ruedas", 0),
                codigo_provincia=props.get("codigo_provincia"),
                codigo_municipio=props.get("codigo_municipio"),
                tipo_lonja=props.get("tipo_lonja"),
                titularidad=props.get("titularidad"),
                gestion=props.get("gestion"),
                superficie_cubierta=props.get("superficie_cubierta"),
                superficie_aire=props.get("superficie_aire"),
                superficie_solar=props.get("superficie_solar"),
                estado=props.get("estado"),
                tipo_parque=props.get("tipo_parque"),
                agua=props.get("agua"),
                saneamiento=props.get("saneamiento"),
                electricidad=props.get("electricidad"),
                comedor=props.get("comedor"),
                juegos_infantiles=props.get("juegos_infantiles"),
                otras_prestaciones=props.get("otras_prestaciones"),
                lat=geo_point.get("lat"),  # Extraemos lat del geo_point
                lon=geo_point.get("lon"),  # Extraemos lon del geo_point
                geometry=item.get("geometry") 
            )
            results.append(dto)
        return results
    
    def get_all_places_as_geojson(self, category: Optional[str] = None):
        places = self.get_all_places(category)  # reutilizas lo que ya tienes
        
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": place.geometry,
                    "properties": {
                        "id": place.id,
                        "nombre": place.nombre,
                        "municipio": place.municipio,
                        "dataset": place.dataset,
                        "estado": place.estado,
                        "acceso_silla_ruedas": place.acceso_silla_ruedas,
                        "superficie_solar": place.superficie_solar,
                        "superficie_aire": place.superficie_aire,
                        "tipo_lonja": place.tipo_lonja,
                        "tipo_parque": place.tipo_parque,
                        "agua": place.agua,
                        "electricidad": place.electricidad,
                        "juegos_infantiles": place.juegos_infantiles,
                    }
                }
                for place in places
            ]
        }
        
    # Método de búsqueda avanzada con filtros dinámicos
    def search_places(self, filters: dict):
        raw_data = self.dao.search(filters)
        results = []
        
        for item in raw_data:
            props = item.get("properties", {})
            
            dto = LugarDTO(
                id=item.get("_id"),
                nombre=props.get("nombre", "Sin nombre"),
                municipio=props.get("municipio_nombre", "Provincia de Badajoz"),
                dataset=item.get("dataset", "general"), 
                acceso_silla_ruedas=props.get("acceso_silla_ruedas", 0),
                codigo_provincia=props.get("codigo_provincia"),
                codigo_municipio=props.get("codigo_municipio"),
                tipo_lonja=props.get("tipo_lonja"),
                titularidad=props.get("titularidad"),
                gestion=props.get("gestion"),
                superficie_cubierta=props.get("superficie_cubierta"),
                superficie_aire=props.get("superficie_aire"),
                superficie_solar=props.get("superficie_solar"),
                estado=props.get("estado"),
                tipo_parque=props.get("tipo_parque"),
                agua=props.get("agua"),
                saneamiento=props.get("saneamiento"),
                electricidad=props.get("electricidad"),
                comedor=props.get("comedor"),
                juegos_infantiles=props.get("juegos_infantiles"),
                otras_prestaciones=props.get("otras_prestaciones")
            )
            results.append(dto)
        return results
    
    # Método de búsqueda geoespacial (ejemplo básico)
    def search_by_location(self, lat: float, lon: float, radius_km: float):
        # Este método es un ejemplo y no implementa la lógica real de búsqueda geoespacial
        # En una implementación real, se usaría una consulta geoespacial en la base de datos
        return self.dao.search_by_location(lat, lon, radius_km)
    
    # Create, Update y Delete
    def create_place(self, lugar_data: dict):
        return self.dao.create(lugar_data)
    
    def update_place(self, doc_id: str, update_data: dict):
        return self.dao.update(doc_id, update_data)
    
    def delete_place(self, doc_id: str):
        return self.dao.delete(doc_id)