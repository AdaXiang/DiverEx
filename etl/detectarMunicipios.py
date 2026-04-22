import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# ==============================
# CONFIG
# ==============================

load_dotenv()

COUCH_URL = os.getenv("COUCHDB_URL")
DB_NAME = os.getenv("COUCHDB_DB")
USER = os.getenv("COUCHDB_USER")
PASSWORD = os.getenv("COUCHDB_PASSWORD")

auth = HTTPBasicAuth(USER, PASSWORD)

# ==============================
# CONSULTA
# ==============================

def get_unknown_municipios():
    url = f"{COUCH_URL}/{DB_NAME}/_find"

    query = {
        "selector": {
            "properties.municipio_nombre": "Desconocido"
        },
        "fields": ["properties.codigo_municipio"],
        "limit": 10000
    }

    res = requests.post(url, json=query, auth=auth)

    if res.status_code != 200:
        print("❌ Error en consulta:", res.text)
        return set()

    data = res.json()

    codigos = {
        doc["properties"]["codigo_municipio"]
        for doc in data.get("docs", [])
    }

    return codigos


# ==============================
# GENERAR DICCIONARIO
# ==============================

def generate_mapping(codigos):
    mapping = {codigo: "TODO_NOMBRE" for codigo in sorted(codigos)}

    print("\n🧾 Diccionario generado:\n")
    print("{")
    for k, v in mapping.items():
        print(f'    "{k}": "{v}",')
    print("}")

    return mapping


# ==============================
# MAIN
# ==============================

def main():
    print("🔍 Buscando municipios desconocidos...")

    codigos = get_unknown_municipios()

    if not codigos:
        print("✅ No hay municipios desconocidos")
        return

    print(f"⚠️ Encontrados {len(codigos)} códigos únicos")

    generate_mapping(codigos)


if __name__ == "__main__":
    main()