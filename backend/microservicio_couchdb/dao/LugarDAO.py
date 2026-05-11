import json

import requests
from typing import Optional, List, Dict
from couchbase.search import SearchOptions, GeoDistanceQuery
from couchbase.options import SearchOptions

class LugarDAO:
    def __init__(self, host, user, password, bucket):
        self.url = f"http://{host}:8093/query/service"
        self.auth = (user, password)
        self.bucket = bucket

    # -----------------------------
    # Ejecutar query base
    # -----------------------------
    def _execute(self, statement: str) -> List[Dict]:
        res = requests.post(
            self.url,
            auth=self.auth,
            json={"statement": statement},
            headers={"Content-Type": "application/json"}
        )

        if res.status_code != 200:
            raise Exception(f"Couchbase error: {res.text}")

        return res.json().get("results", [])

    # -----------------------------
    # Obtener por ID (KEY real)
    # -----------------------------
    def get_by_id(self, doc_id: str):
        query = f"""
        SELECT META(t).id AS id, t.*
        FROM `{self.bucket}` t
        USE KEYS "{doc_id}"
        """
        results = self._execute(query)
        return results[0] if results else None

    # -----------------------------
    # Filtrar por dataset
    # -----------------------------
    def get_by_dataset(self, dataset_type: str):
        query = f"""
        SELECT META(t).id AS id, t.*
        FROM `{self.bucket}` t
        WHERE t.dataset = "{dataset_type}"
        """
        return self._execute(query)

    # -----------------------------
    # Listar todo (con filtro opcional)
    # -----------------------------
    def list_all(self, dataset: Optional[str] = None):
        if dataset:
            query = f"""
            SELECT META(t).id AS id, t.*
            FROM `{self.bucket}` t
            WHERE t.dataset = "{dataset}"
            """
        else:
            query = f"""
            SELECT META(t).id AS id, t.*
            FROM `{self.bucket}` t
            """
        return self._execute(query)
    
    # -----------------------------
    # Búsqueda avanzada (filtros dinámicos)
    # -----------------------------
    def search(self, filters: Dict[str, str]):
        where_clauses = [f't.{key} = "{value}"' for key, value in filters.items()]
        where_statement = " AND ".join(where_clauses)
        
        query = f"""
        SELECT META(t).id AS id, t.*
        FROM `{self.bucket}` t
        WHERE {where_statement}
        """
        return self._execute(query)
    
    # -----------------------------
    # Búsqueda geoespacial (ejemplo básico)
    # -----------------------------
    def search_by_location(self, lat, lon, radius_km):
        host = self.url.split(":8093")[0].replace("http://", "")
        
        fts_url = f"http://{host}:8094/api/bucket/places/scope/_default/index/idx_geo/query"

        payload = {
            "query": {
                "field": "geo_point.coordinates",
                "location": {"lon": float(lon), "lat": float(lat)},
                "distance": f"{radius_km}km"
            },
            "size": 500
        }
        # Realizamos la consulta FTS para obtener los IDs de los documentos que cumplen con el filtro geoespacial
        res = requests.post(fts_url, auth=self.auth, json=payload)
        
        if res.status_code != 200:
            print(f"Error FTS: {res.text}")
            return []

        hits = res.json().get("hits", [])
        print(f"FTS hits: {len(hits)}")
        doc_ids = [hit.get("id") for hit in hits if hit.get("id")]

        if not doc_ids:
            return []

        # N1QL para traer los documentos completos
        ids_list = ", ".join([f"'{i}'" for i in doc_ids])
        query = f"SELECT META(t).id AS id, t.* FROM `{self.bucket}` t WHERE META(t).id IN [{ids_list}]"
        
        return self._execute(query)
    # -----------------------------
    # Crear, actualizar, eliminar (CRUD básico)
    # -----------------------------
    def create(self, data: Dict):
        # Para crear un documento, normalmente usaríamos el SDK de Couchbase
        # Aquí solo mostramos un ejemplo de cómo se podría hacer con una query N1QL
        query = f"""
        INSERT INTO `{self.bucket}` (KEY, VALUE)
        VALUES ("{data['id']}", {data})
        """
        return self._execute(query)
    
    def update(self, doc_id: str, data: Dict):
        # Para actualizar, también es mejor usar el SDK, pero aquí un ejemplo con N1QL
        set_clauses = ", ".join([f"{key} = {value}" for key, value in data.items()])
        query = f"""
        UPDATE `{self.bucket}`
        SET {set_clauses}
        WHERE META().id = "{doc_id}"
        """
        return self._execute(query)
    
    def delete(self, doc_id: str):
        query = f"""
        DELETE FROM `{self.bucket}`
        WHERE META().id = "{doc_id}"
        """
        return self._execute(query)