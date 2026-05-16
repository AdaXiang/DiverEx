import json

import requests
from typing import Optional, List, Dict
from couchbase.search import SearchOptions, GeoDistanceQuery
from couchbase.options import Any, SearchOptions

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
    def search(self, filters: Dict[str, Any]):
        where_clauses = []

        for key, value in filters.items():
            if value is None:
                continue
                
            # 1. Si es una lista (Ej: estados=['B', 'R']) -> Usamos IN
            if isinstance(value, list):
                # Convertimos la lista de Python en un array de N1QL: ['B', 'R']
                array_str = ", ".join([f"'{v}'" for v in value])
                where_clauses.append(f"t.{key} IN [{array_str}]")
                
            # 2. Si es un Booleano (Ej: acceso_silla_ruedas=True) -> Sin comillas
            elif isinstance(value, bool):
                val_str = "TRUE" if value else "FALSE"
                where_clauses.append(f"t.{key} = {val_str}")
                
            # 3. Si es un String normal (Ej: municipio="Don Benito") -> Usamos =
            else:
                where_clauses.append(f"t.{key} = '{value}'")

        # Si no hay filtros, traemos todo (o puedes poner LIMIT)
        where_statement = " AND ".join(where_clauses) if where_clauses else "1=1"

        query = f"""
            SELECT META(t).id AS id, t.*
            FROM `{self.bucket}` t
            WHERE {where_statement}
        """
        
        print("N1QL Query:", query) # Útil para ver qué está montando
        return self._execute(query)
    
    # -----------------------------
    # Búsqueda geoespacial (ejemplo básico)
    # -----------------------------
    def search_by_location(self, lat, lon, radius_km):
        host = self.url.split(":8093")[0].replace("http://", "")
        
        fts_url = f"http://{host}:8094/api/bucket/places/scope/_default/index/idx_geo/query"

        payload = {
            "query": {
                "field": "geo_point",
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
 

    def filter_places(self, lat, lon, distancia_max, acceso_silla_ruedas, zona_infantil, comedor, tipos, estados, nombre, municipio, ids_recomendaciones=None):
    
        where_clauses = ["t.type = 'feature'"]
        distance_expr = "NULL"

        # ==========================================
        # 1. FILTRO ESPACIAL
        # ==========================================
        if lat is not None and lon is not None and distancia_max is not None:
            fts_query = {
                "field": "geo_point.coordinates",
                "location": {"lon": float(lon), "lat": float(lat)},  # objeto, no array
                "distance": f"{distancia_max}km"
            }
            query_str = json.dumps(fts_query)
            
            # Nombre completo del índice
            where_clauses.append(f"SEARCH(t, {query_str}, {{\"index\": \"places._default.idx_geo\"}})")
            
            # Haversine en lugar de SEARCH_META (más fiable con geopoint)
            distance_expr = f"""ROUND(
                ACOS(
                    SIN(RADIANS({float(lat)})) * SIN(RADIANS(t.geo_point.coordinates[1])) +
                    COS(RADIANS({float(lat)})) * COS(RADIANS(t.geo_point.coordinates[1])) *
                    COS(RADIANS(t.geo_point.coordinates[0]) - RADIANS({float(lon)}))
                ) * 6371000, 0
            )"""

        # ==========================================
        # 2. FILTROS DE ATRIBUTOS
        # ==========================================
        if acceso_silla_ruedas is not None:
            val = "TRUE" if acceso_silla_ruedas else "FALSE"
            where_clauses.append(f"t.properties.acceso_silla_ruedas = {val}")
            
        if zona_infantil is not None:
            val = "TRUE" if zona_infantil else "FALSE"
            where_clauses.append(f"t.properties.juegos_infantiles = {val}")

        if comedor is not None:
            val = "TRUE" if comedor else "FALSE"
            where_clauses.append(f"t.properties.comedor = {val}")

        if estados:
            estados_str = ", ".join([f"'{e}'" for e in estados])
            where_clauses.append(f"t.properties.estado IN [{estados_str}]")

        if tipos:
            tipos_str = ", ".join([f"'{ti}'" for ti in tipos])  # evitamos shadowing de 't'
            where_clauses.append(f"t.tipo_lugar IN [{tipos_str}]")

        if ids_recomendaciones:
            print("IDs de recomendaciones para filtrar:", ids_recomendaciones)
            ids_str = ", ".join([f"'{i}'" for i in ids_recomendaciones])
            where_clauses.append(f"META(t).id IN [{ids_str}]")

        if nombre:
            where_clauses.append(f"LOWER(t.properties.nombre) LIKE '%{nombre.lower()}%'")
            
        if municipio:
            where_clauses.append(f"LOWER(t.properties.municipio_nombre) LIKE '%{municipio.lower()}%'")

        # ==========================================
        # 3. EJECUCIÓN FINAL
        # ==========================================
        where_statement = " AND ".join(where_clauses)
        
        # ORDER BY solo si hay distancia
        order_by = "ORDER BY distancia_metros ASC" if lat is not None and lon is not None else ""
        
        query = f"""
        SELECT
            META(t).id AS id,
            {distance_expr} AS distancia_metros,
            ROUND(({distance_expr}) / 1000, 2) AS distancia_km,
            t.*
        FROM `{self.bucket}`._default._default AS t
        WHERE {where_statement}
        {order_by}
        """
        
        return self._execute(query)
           