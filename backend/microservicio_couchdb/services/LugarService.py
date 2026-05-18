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
        item = self.dao.get_by_id(site_id)
        props = item.get("properties", {}) if item else {}
        if not item:
            return None
        
        dto = LugarDTO(
                id=item.get("_id"),
                tipo_lugar=item.get("tipo_lugar", "desconocido"),
                nombre=props.get("nombre", "Sin nombre"),
                municipio=props.get("municipio_nombre", "Provincia de Badajoz"),
                dataset=item.get("dataset", "general"), 
                acceso_silla_ruedas=props.get("acceso_silla_ruedas", 0),
                codigo_provincia=props.get("codigo_provincia"),
                codigo_municipio=props.get("codigo_municipio"),
                titularidad=props.get("titularidad"),
                gestion=props.get("gestion"),
                superficie_cubierta=props.get("superficie_cubierta"),
                superficie_aire=props.get("superficie_aire"),
                superficie_solar=props.get("superficie_solar"),
                estado=props.get("estado"),
                agua=props.get("agua"),
                saneamiento=props.get("saneamiento"),
                electricidad=props.get("electricidad"),
                comedor=props.get("comedor"),
                juegos_infantiles=props.get("juegos_infantiles"),
                otras_prestaciones=props.get("otras_prestaciones"),
                geo_point=item.get("geo_point"),  
                geometry=item.get("geometry") 
            )

        return dto
    
    # Devuelve una lista de lugares, opcionalmente filtrada por categoría (dataset)
    def get_all_places(self, category: Optional[str] = None):
        raw_data = self.dao.list_all(category)
        results = []
        
        for item in raw_data:
            props = item.get("properties", {})
            
            # Creamos el DTO asegurándonos de que CADA nombre coincida con el DTO
            dto = LugarDTO(
                id=item.get("_id"),
                tipo_lugar=item.get("tipo_lugar", "desconocido"),
                nombre=props.get("nombre", "Sin nombre"),
                municipio=props.get("municipio_nombre", "Provincia de Badajoz"),
                dataset=item.get("dataset", "general"), 
                acceso_silla_ruedas=props.get("acceso_silla_ruedas", 0),
                codigo_provincia=props.get("codigo_provincia"),
                codigo_municipio=props.get("codigo_municipio"),
                titularidad=props.get("titularidad"),
                gestion=props.get("gestion"),
                superficie_cubierta=props.get("superficie_cubierta"),
                superficie_aire=props.get("superficie_aire"),
                superficie_solar=props.get("superficie_solar"),
                estado=props.get("estado"),
                agua=props.get("agua"),
                saneamiento=props.get("saneamiento"),
                electricidad=props.get("electricidad"),
                comedor=props.get("comedor"),
                juegos_infantiles=props.get("juegos_infantiles"),
                otras_prestaciones=props.get("otras_prestaciones"),
                geo_point=item.get("geo_point"),  
                geometry=item.get("geometry") 
            )
            results.append(dto)
        return results
        
    # Método de búsqueda avanzada con filtros dinámicos
    def search_places(self, lat=None, lon=None, distancia_max=None, 
                  acceso_silla_ruedas=None, zona_infantil=None, 
                  comedor=None, tipos=None, estados=None, 
                  nombre=None, municipio=None, ids_recomendaciones=None):

        results = []
        raw_data = self.dao.filter_places(
            lat=lat, 
            lon=lon, 
            distancia_max=distancia_max,
            acceso_silla_ruedas=acceso_silla_ruedas,
            zona_infantil=zona_infantil,
            comedor=comedor,
            tipos=tipos,
            estados=estados,
            nombre=nombre,
            municipio=municipio,
            ids_recomendaciones=ids_recomendaciones
        )

        if not raw_data:
            return []

        results = []

        for item in raw_data:
            props = item.get("properties", {})
            
            distancia_calculada = item.get("distancia_km", 0)
            
            dto = LugarDTO(
                id=item.get("_id"),
                tipo_lugar=item.get("tipo_lugar", "desconocido"),
                nombre=props.get("nombre", "Sin nombre"),
                municipio=props.get("municipio_nombre", "Provincia de Badajoz"),
                dataset=item.get("dataset", "general"), 
                acceso_silla_ruedas=props.get("acceso_silla_ruedas", 0),
                codigo_provincia=props.get("codigo_provincia"),
                codigo_municipio=props.get("codigo_municipio"),
                titularidad=props.get("titularidad"),
                gestion=props.get("gestion"),
                superficie_cubierta=props.get("superficie_cubierta"),
                superficie_aire=props.get("superficie_aire"),
                superficie_solar=props.get("superficie_solar"),
                estado=props.get("estado"),
                agua=props.get("agua"),
                saneamiento=props.get("saneamiento"),
                electricidad=props.get("electricidad"),
                comedor=props.get("comedor"),
                juegos_infantiles=props.get("juegos_infantiles"),
                otras_prestaciones=props.get("otras_prestaciones"),
                geo_point=item.get("geo_point"),  
                geometry=item.get("geometry"),
                distancia_km=distancia_calculada
            )
            results.append(dto)
        return results
    
    # Método de búsqueda geoespacial 
    def search_by_location(self, lat: float, lon: float, radius_km: float):
        raw_data = self.dao.search_by_location(lat, lon, radius_km)
        results = []
        
        for item in raw_data:
            props = item.get("properties", {})
            
            dto = LugarDTO(
                id=item.get("_id"),
                tipo_lugar=item.get("tipo_lugar", "desconocido"),
                nombre=props.get("nombre", "Sin nombre"),
                municipio=props.get("municipio_nombre", "Provincia de Badajoz"),
                dataset=item.get("dataset", "general"), 
                acceso_silla_ruedas=props.get("acceso_silla_ruedas", 0),
                codigo_provincia=props.get("codigo_provincia"),
                codigo_municipio=props.get("codigo_municipio"),
                titularidad=props.get("titularidad"),
                gestion=props.get("gestion"),
                superficie_cubierta=props.get("superficie_cubierta"),
                superficie_aire=props.get("superficie_aire"),
                superficie_solar=props.get("superficie_solar"),
                estado=props.get("estado"),
                agua=props.get("agua"),
                saneamiento=props.get("saneamiento"),
                electricidad=props.get("electricidad"),
                comedor=props.get("comedor"),
                juegos_infantiles=props.get("juegos_infantiles"),
                otras_prestaciones=props.get("otras_prestaciones"),
                geo_point=item.get("geo_point"),  
                geometry=item.get("geometry") 
            )
            results.append(dto)
        return results
    
    def getLugaresSimilares(self, lugar_id: str):
        results = []
        raw_data = self.dao.getLugaresSimilares(lugar_id)

        if not raw_data:
            return []

        results = []

        for item in raw_data:
            props = item.get("properties", {})
            
            dto = LugarDTO(
                id=item.get("_id"),
                tipo_lugar=item.get("tipo_lugar", "desconocido"),
                nombre=props.get("nombre", "Sin nombre"),
                municipio=props.get("municipio_nombre", "Provincia de Badajoz"),
                dataset=item.get("dataset", "general"), 
                acceso_silla_ruedas=props.get("acceso_silla_ruedas", 0),
                codigo_provincia=props.get("codigo_provincia"),
                codigo_municipio=props.get("codigo_municipio"),
                titularidad=props.get("titularidad"),
                gestion=props.get("gestion"),
                superficie_cubierta=props.get("superficie_cubierta"),
                superficie_aire=props.get("superficie_aire"),
                superficie_solar=props.get("superficie_solar"),
                estado=props.get("estado"),
                agua=props.get("agua"),
                saneamiento=props.get("saneamiento"),
                electricidad=props.get("electricidad"),
                comedor=props.get("comedor"),
                juegos_infantiles=props.get("juegos_infantiles"),
                otras_prestaciones=props.get("otras_prestaciones"),
                geo_point=item.get("geo_point"),  
                geometry=item.get("geometry"),
            )
            results.append(dto)
        return results

    # Create, Update y Delete
    def create_place(self, lugar_data: dict):
        return self.dao.create(lugar_data)
    
    def update_place(self, doc_id: str, update_data: dict):
        return self.dao.update(doc_id, update_data)
    
    def delete_place(self, doc_id: str):
        return self.dao.delete(doc_id)