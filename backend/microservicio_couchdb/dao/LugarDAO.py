import requests
from typing import Optional, List, Dict

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