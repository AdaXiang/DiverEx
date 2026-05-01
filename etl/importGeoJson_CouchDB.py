import json
import requests
from requests.auth import HTTPBasicAuth
import os #trabajo de ruta
from dotenv import load_dotenv 

# =========================
# CONFIG
# =========================
load_dotenv()

COUCH_URL = os.getenv("COUCHBASE_URL")
DB_NAME = os.getenv("COUCHBASE_USER")
USER = os.getenv("COUCHBASE_USER")
PASSWORD = os.getenv("COUCHBASE_PASSWORD")
COUCHBASE_HOST = os.getenv("COUCHBASE_HOST")
BUCKET = os.getenv("COUCHBASE_BUCKET")

BATCH_SIZE = int(os.getenv("BATCH_SIZE", 1000))

# Auth para request
auth = HTTPBasicAuth(USER, PASSWORD)

#Diccionario de municipios, para no añadir solo el codigo
municipios = {
    "730": "Acedera",
    "207": "Aceuchal",
    "940": "Ahillones",
    "840": "Alange",
    "170": "Albuera (La)",
    "510": "Alburquerque",
    "131": "Alconchel",
    "393": "Alconera",
    "894": "Aljucén",
    "171": "Almendral",
    "200": "Almendralejo",
    "850": "Arroyo de San Serván",
    "329": "Atalaya",
    "920": "Azuaga",

    # Badajoz (todos mapean a 001–012 → simplificado)
    "001": "Badajoz",
    "002": "Badajoz",
    "003": "Badajoz",
    "004": "Badajoz",
    "005": "Badajoz",
    "006": "Badajoz",
    "007": "Badajoz",
    "008": "Badajoz",
    "009": "Badajoz",
    "010": "Badajoz",
    "011": "Badajoz",
    "012": "Badajoz",

    "160": "Barcarrota",
    "659": "Baterno",
    "429": "Benquerencia de la Serena",
    "930": "Berlanga",
    "250": "Bienvenida",
    "394": "Bodonal de la Sierra",
    "370": "Burguillos del Cerro",
    "600": "Cabeza del Buey",
    "293": "Cabeza la Vaca",
    "810": "Calamonte",
    "292": "Calera de León",
    "249": "Calzadilla de los Barros",
    "460": "Campanario",
    "443": "Campillo de Llerena",
    "612": "Capilla",
    "488": "Carmonita",
    "770": "Casas de Don Pedro",
    "960": "Casas de Reina",
    "680": "Castilblanco",
    "420": "Castuera",
    "105": "Cheles",
    "518": "Codosera (La)",
    "487": "Cordobilla de Lácara",
    "469": "Coronada (La)",
    "196": "Corte de Peleas",
    "479": "Cristina",
    "820": "Don Álvaro",
    "400": "Don Benito",
    "197": "Entrín Bajo",
    "860": "Esparragalejo",
    "439": "Esparragosa de la Serena",
    "620": "Esparragosa de Lares",
    "390": "Feria",
    "340": "Fregenal de la Sierra",
    "660": "Fuenlabrada de los Montes",
    "240": "Fuente de Cantos",
    "980": "Fuente del Arco",
    "360": "Fuente del Maestre",
    "280": "Fuentes de León",
    "690": "Garbayuela",
    "656": "Garlitos",
    "870": "Garrovilla (La)",
    "910": "Granja de Torrehermosa",
    "470": "Guareña",
    "714": "Haba (La)",
    "692": "Helechosa de los Montes",
    "670": "Herrera del Duque",
    "441": "Higuera de la Serena",
    "445": "Higuera de Llerena",
    "132": "Higuera de Vargas",
    "350": "Higuera la Real",
    "226": "Hinojosa del Valle",
    "228": "Hornachos",
    "380": "Jerez de los Caballeros",
    "391": "Lapa (La)",
    "227": "Llera",
    "900": "Llerena",
    "498": "Lobón",
    "468": "Magacela",
    "939": "Maguilla",
    "928": "Malcocinado",
    "440": "Malpartida de la Serena",
    "478": "Manchita",
    "411": "Medellín",
    "320": "Medina de las Torres",
    "413": "Mengabril",
    "800": "Mérida",
    "891": "Mirandilla",
    "260": "Monesterio",
    "291": "Montemolín",
    "427": "Monterrubio de la Serena",
    "480": "Montijo",
    "176": "Morera (La)",
    "486": "Nava de Santiago (La)",
    "760": "Navalvillar de Pela",
    "173": "Nogales",
    "120": "Oliva de la Frontera",
    "475": "Oliva de Mérida",
    "100": "Olivenza",
    "750": "Orellana de la Sierra",
    "740": "Orellana la Vieja",
    "476": "Palomas",
    "610": "Peñalsordo",
    "919": "Peraleda del Zaucejo",
    "630": "Puebla de Alcocer",
    "490": "Puebla de la Calzada",
    "477": "Puebla de la Reina",
    "191": "Puebla de Obando",
    "310": "Puebla de Sancho Pérez",
    "906": "Puebla del Maestre",
    "229": "Puebla del Prior",
    "184": "Pueblonuevo del Guadiana",
    "450": "Quintana de la Serena",
    "970": "Reina",
    "715": "Rena",
    "442": "Retamal de Llerena",
    "225": "Ribera del Fresno",
    "657": "Risco",
    "190": "Roca de la Sierra (La)",
    "174": "Salvaleón",
    "175": "Salvatierra de los Barros",
    "893": "San Pedro de Mérida",
    "500": "San Vicente de Alcántara",
    "655": "Sancti-Spíritus",
    "410": "Santa Amalia",
    "150": "Santa Marta",
    "230": "Santos de Maimona (Los)",
    "270": "Segura de León",
    "650": "Siruela",
    "209": "Solana de los Barros",
    "640": "Talarrubias",
    "140": "Talavera la Real",
    "133": "Táliga",
    "658": "Tamurejo",
    "172": "Torre de Miguel Sesmero",
    "880": "Torremayor",
    "210": "Torremejía",
    "909": "Trasierra",
    "892": "Trujillanos",
    "290": "Usagre",
    "689": "Valdecaballeros",
    "185": "Valdelacalzada",
    "474": "Valdetorres",
    "444": "Valencia de las Torres",
    "134": "Valencia del Mombuey",
    "330": "Valencia del Ventoso",
    "458": "Valle de la Serena",
    "177": "Valle de Matamoros",
    "178": "Valle de Santa Ana",
    "378": "Valverde de Burguillos",
    "130": "Valverde de Leganés",
    "927": "Valverde de Llerena",
    "890": "Valverde de Mérida",
    "220": "Villafranca de los Barros",
    "950": "Villagarcía de la Torre",
    "473": "Villagonzalo",
    "208": "Villalba de los Barros",
    "700": "Villanueva de la Serena",
    "110": "Villanueva del Fresno",
    "716": "Villar de Rena",
    "192": "Villar del Rey",
    "678": "Villarta de los Montes",
    "300": "Zafra",
    "129": "Zahínos",
    "430": "Zalamea de la Serena",
    "830": "Zarza (La)",
    "611": "Zarza-Capilla",
    
    # CODIGO DESCONOCIDOS #
    "013": "Atalaya",
    "014": "Azuaga",
    "016": "Barcarrota",
    "017": "Baterno",
    "018": "Benquerencia de la Serena",
    "019": "Berlanga",
    "020": "Bienvenida",
    "021": "Bodonal de la Sierra",
    "022": "Burguillos del Cerro",
    "023": "Cabeza del Buey",
    "024": "Cabeza la Vaca",
    "025": "Calamonte",
    "026": "Calera de León",
    "027": "Calzadilla de los Barros",
    "028": "Campanario",
    "029": "Campillo de Llerena",
    "030": "Capilla",
    "031": "Carmonita",
    "032": "El Carrascalejo",
    "033": "Casas de Don Pedro",
    "034": "Casas de Reina",
    "035": "Castilblanco",
    "036": "Castuera",
    "037": "La Codosera",
    "038": "Cordobilla de Lácara",
    "039": "La Coronada",
    "040": "Corte de Peleas",
    "041": "Corte de Peleas",
    "042": "Cheles",
    "043": "Don Álvaro",
    "044": "Don Benito",
    "045": "Entrín Bajo",
    "046": "Esparragalejo",
    "047": "Esparragosa de la Serena",
    "048": "Esparragosa de Lares",
    "049": "Feria",
    "050": "Fregenal de la Sierra",
    "051": "Fuenlabrada de los Montes",
    "052": "Fuente de Cantos",
    "053": "Fuente del Arco",
    "054": "Fuente del Maestre",
    "055": "Fuentes de León",
    "056": "Garbayuela",
    "057": "Garlitos",
    "058": "La Garrovilla",
    "059": "Granja de Torrehermosa",
    "060": "Guareña",
    "061": "La Haba",
    "062": "Helechosa de los Montes",
    "063": "Herrera del Duque",
    "064": "Higuera de la Serena",
    "065": "Higuera de Llerena",
    "066": "Higuera de Vargas",
    "067": "Higuera la Real",
    "068": "Hinojosa del Valle",
    "069": "Hornachos",
    "070": "Jerez de los Caballeros",
    "071": "La Lapa",
    "072": "Lobón",
    "073": "Llera",
    "074": "Llerena",
    "075": "Magacela",
    "076": "Maguilla",
    "077": "Malcocinado",
    "078": "Malpartida de la Serena",
    "079": "Manchita",
    "080": "Medellín",
    "081": "Medina de las Torres",
    "082": "Mengabril",
    "084": "Mirandilla",
    "085": "Monesterio",
    "086": "Montemolín",
    "087": "Monterrubio de la Serena",
    "088": "Montijo",
    "089": "La Morera",
    "090": "La Nava de Santiago",
    "091": "Navalvillar de Pela",
    "092": "Nogales",
    "093": "Oliva de la Frontera",
    "094": "Oliva de Mérida",
    "095": "Olivenza",
    "096": "Orellana de la Sierra",
    "097": "Orellana la Vieja",
    "098": "Palomas",
    "099": "La Parra",
    "101": "Peraleda del Zaucejo",
    "102": "Puebla de Alcocer",
    "103": "Puebla de la Calzada",
    "104": "Puebla de la Reina",
    "106": "Puebla del Prior",
    "107": "Puebla de Obando",
    "108": "San Jorge de Alor",
    "109": "Quintana de la Serena",
    "111": "Rena",
    "112": "Retamal de Llerena",
    "113": "Ribera del Fresno",
    "114": "Risco",
    "115": "La Roca de la Sierra",
    "116": "Salvaleón",
    "117": "Salvatierra de los Barros",
    "118": "Sancti-Spíritus",
    "119": "San Pedro de Mérida",
    "121": "Santa Marta",
    "122": "Los Santos de Maimona",
    "123": "San Vicente de Alcántara",
    "124": "Segura de León",
    "125": "Siruela",
    "126": "Solana de los Barros",
    "127": "Talarrubias",
    "128": "Talavera la Real",
    "135": "Trujillanos",
    "136": "Usagre",
    "137": "Valdecaballeros",
    "138": "Valdetorres",
    "139": "Valencia de las Torres",
    "141": "Valencia del Ventoso",
    "142": "Valverde de Burguillos",
    "143": "Valverde de Leganés",
    "144": "Valverde de Llerena",
    "145": "Valverde de Mérida",
    "146": "Valle de la Serena",
    "147": "Valle de Matamoros",
    "148": "Valle de Santa Ana",
    "149": "Villafranca de los Barros",
    "151": "Villagonzalo",
    "152": "Villalba de los Barros",
    "153": "Villanueva de la Serena",
    "154": "Villanueva del Fresno",
    "155": "Villar del Rey",
    "156": "Villar de Rena",
    "157": "Villarta de los Montes",
    "158": "Zafra",
    "159": "Zahínos",
    "161": "Zarza-Capilla",
    "162": "La Zarza",
    "901": "Valdelacalzada",
    "902": "Pueblonuevo del Guadiana",
    "903": "Guadiana",
}

# =========================
# UTILIDADES
# =========================
def calcular_centroide(geometry: dict):
    """
    Calcula un punto representativo (lat, lon)
    a partir de una geometría GeoJSON (Polygon o MultiPolygon).
    """

    coords = geometry.get("coordinates", [])

    all_points = []

    # Detectar tipo
    geom_type = geometry.get("type")

    if geom_type == "Polygon":
        # coords: [ [ [lon, lat], ... ] ]
        for ring in coords:
            for point in ring:
                all_points.append(point)

    elif geom_type == "MultiPolygon":
        # coords: [ [ [ [lon, lat] ] ] ]
        for polygon in coords:
            for ring in polygon:
                for point in ring:
                    all_points.append(point)

    else:
        return None  # o lanzar error

    if not all_points:
        return None

    # Promedio simple
    lon = sum(p[0] for p in all_points) / len(all_points)
    lat = sum(p[1] for p in all_points) / len(all_points)

    return {
        "lat": lat,
        "lon": lon
    }

def to_bool(value):
    if not value:
        return False
    return str(value).lower() == "si"

# Archivos GeoJSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES = [
    ("lonjas", os.path.join(BASE_DIR, "../data/lonjasmercadosferias2025.geojson")),
    ("parques", os.path.join(BASE_DIR, "../data/parques2025.geojson"))
]

# ==============================
# 1. LIMPIAMOS BASE DE DATOS
# ==============================

auth = HTTPBasicAuth(USER, PASSWORD)
print(f"🔐 Conectando a CouchDB en {COUCH_URL} con usuario '{USER}'")

"""
Borra las base de dayos creadas, limpiando el conjunto de datos
"""
def recreate_db():
    print("🔄 Reiniciando base de datos...")
    
    #Eliminamos base de datos
    res = requests.delete(f"{COUCH_URL}/{DB_NAME}", auth=auth)
    if res.status_code not in [200, 202, 404]:
        print("❌ Error borrando DB:", res.text)
        
    #La volvemos a añadir, ya vacia
    res = requests.put(f"{COUCH_URL}/{DB_NAME}", auth=auth)
    if res.status_code in [201, 202]:
        print("✅ DB creada")
    else:
        print("⚠️ DB ya existía o error:", res.text)

# ===============================
# 2. TRANSFORMAR GEOJSON A JSON
# ===============================
def load_geojson(file_path, tipo):
    print(f"📂 Procesando {file_path}...")

    #Leemos archivo
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    #Transformamos un elemento del geoJSON a un JSON
    docs = []
    for i, feature in enumerate(data["features"]):
        props = feature.get("properties", {})
        props["acceso_silla_ruedas"] = to_bool(props.get("acceso_silla_ruedas"))
        geom = feature.get("geometry", {})
        codigo = props.get("codigo_municipio")
        nombre_municipio = municipios.get(codigo, "Desconocido")
        geo_point = calcular_centroide(geom)

        doc = {
            "_id": f"{tipo}_{i}",
            "type": "feature",
            "dataset": tipo,
            "geometry": geom,
            "geo_point": geo_point,
            "properties": {
                **props,
                "municipio_nombre": nombre_municipio #añadir el nombre del municipio
            }
        }

        docs.append(doc)

    print(f"✅ {len(docs)} documentos preparados")
    return docs

# ===============================
# 3. AÑADIR DOCS EN BULK A COUCH
# ===============================
def bulk_insert(docs):

    #Rutas de peticiones bulk
    url = f"{COUCH_URL}/{DB_NAME}/_bulk_docs"
    #Bucle de documentos con maximo
    # 
    for i in range(0, len(docs), BATCH_SIZE):
        batch = docs[i:i+BATCH_SIZE]

        print(f"📤 Insertando batch {i} - {i+len(batch)}")


        for doc in batch:
            key = doc["_id"]
            statement = f"""
            INSERT INTO `places` (KEY, VALUE)
            VALUES ("{key}", {json.dumps(doc)})
            """

            res = requests.post(
                "http://localhost:8093/query/service",
                auth=(USER, PASSWORD),
                headers={
                    "Content-Type": "application/json"
                },
                json={
                    "statement": statement
                }
            )

            if res.status_code not in [200, 201]:
                print("❌ Error:", res.text)
                return

    print("✅ Todos los documentos insertados")

# ==============================
# MAIN
# ==============================
def main():
    #recreate_db()

    all_docs = []

    for tipo, file_path in FILES:
        docs = load_geojson(file_path, tipo)
        all_docs.extend(docs)

    bulk_insert(all_docs)

    print("🎉 ETL COUCH COMPLETADO 🎉")


if __name__ == "__main__":
    main()