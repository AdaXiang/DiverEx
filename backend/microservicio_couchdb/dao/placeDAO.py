from typing import Optional

import couchdb

class PlaceDAO:
    def __init__(self):
        self.server = couchdb.Server("COUCHDB_URL_AUTH") 
        self.db = self.server["geojson"]

    def get_by_id(self, doc_id: str):
        return self.db.get(doc_id)

    def get_by_dataset(self, dataset_type: str):
        # Mango Query de CouchDB
        query = {"selector": {"dataset": dataset_type}}
        return [doc for doc in self.db.find(query)]
    
    def list_all(self, dataset: Optional[str] = None):
        if dataset:
            # Consulta tipo Mango (CouchDB Query)
            query = {"selector": {"dataset": dataset}}
            return [doc for doc in self.db.find(query)]
        else:
            # Retorna todos los documentos saltando los de diseño (_design/...)
            return [self.db[doc_id] for doc_id in self.db if not doc_id.startswith('_design')]