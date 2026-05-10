import json
import random
from neo4j import GraphDatabase
import os #trabajo de ruta
from dotenv import load_dotenv 

# =========================
# CONFIG
# =========================
load_dotenv()
MEMGRAPH_URL = os.getenv("MEMGRAPH_URL",f"bolt://{os.getenv('MEMGRAPH_HOST', 'localhost')}:{os.getenv('MEMGRAPH_PORT', '7687')}")

# Conectamos a la memgraph
driver = GraphDatabase.driver(MEMGRAPH_URL)

# Archivos GeoJSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES = [
    ("lonjas", os.path.join(BASE_DIR, "../data/lonjasmercadosferias2025.geojson")),
    ("parques", os.path.join(BASE_DIR, "../data/parques2025.geojson"))
]

total_lugares = {"lonjas": 0, "parques": 0}
sublabel = {"lonjas": "Lonja", "parques": "Parque"}

# =========================
# UTILIDADES
# =========================
def run_query(query, params=None):
    with driver.session() as session:
        session.run(query, params or {})
        
def to_bool(value):
    if not value:
        return False
    return str(value).lower() == "si"

# =========================
# 1. AÑADIR LUGARES
# =========================
def load_geojson(file_path, tipo):
    print(f"📂 Cargando {file_path} como {tipo}...")

    #Leemos archivo
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    #Recorremos todos los elementos
    for i, feature in enumerate(data["features"]):
        total_lugares[tipo] += 1
        
        #Propiedades, donde esta la informacion
        props = feature["properties"]

        #Respetamos id como couchDB
        lugar_id = f"{tipo}_{i}"

        #Query general
        query = f"""
        MERGE (l:Lugar:{sublabel[tipo]} {{id: $id}})
        SET l.name = $name,
            l.codigo_municipio = $codigo,
            l.estado = $estado,
            l.acceso_silla_ruedas = $acceso,
            l.tipo = $tipo,
            l.likes = 0,
            l.media = 0
        """

        params = {
            "id": lugar_id,
            "name": props.get("nombre"),
            "codigo": props.get("codigo_municipio"),
            "estado": props.get("estado"),
            "acceso": to_bool(props.get("acceso_silla_ruedas")),
            "tipo": props.get(f"tipo_{sublabel[tipo].lower()}"), #Depende del geojson, respeta (tipo_lonja/tipo_parque)
        }

        # Si es parque debemos tener en cuenta que tiene mas propiedades utiles para consultar
        if tipo == "parques":
            query += """
            SET l.agua = $agua,
                l.electricidad = $electricidad,
                l.comedor = $comedor,
                l.juegos_infantiles = $juegos_infantiles
            """
            params.update({
                "agua": to_bool(props.get("agua")),
                "electricidad": to_bool(props.get("electricidad")),
                "comedor": to_bool(props.get("comedor")),
                "juegos_infantiles": to_bool(props.get("juegos_infantiles")),
            })

        run_query(query, params)

    print("✅ Lugares cargados")

# =========================
# 2. CREAR USUARIOS
# =========================
def create_users(n_users):
    print(f"👤 Creando {n_users} usuarios...")

    #Bucle de n_usuarios, el indice del bucle sera nuestro id
    for i in range(n_users):
        query = """
        MERGE (u:Usuario {id: $id})
        SET u.name = $name,
            u.email = $email,
            u.password = $password
        """

        run_query(query, {
            "id": f"{i}",
            "name": f"User {i}",
            "email": f"user{i}@test.com",
            "password": "1234"
        })

    print("✅ Usuarios creados")

# =========================
# 3. RELACIONES RANDOM
# =========================
def create_random_relations(n_users):
    print("🔗 Creando relaciones aleatorias...")

    #Relaciones Usuario -> Lugar
    relaciones = ["VISITA", "FAVORITO", "ME_GUSTA"]

    #Bucle de relaciones random
    for i in range(n_users):
        for _ in range(random.randint(1, 5)):

            #Valores al azar
            user_id = f"{i}"
            tipo = random.choice(["lonjas", "parques"])
            lugar_id = f"{tipo}_{random.randint(0, total_lugares[tipo] - 1)}"

            #Relacion al azar
            rel = random.choice(relaciones)

            #Merge hacemos que no sean unicas las relaciones
            query = f"""
            MATCH (u:Usuario {{id: $uid}})
            MATCH (l:Lugar {{id: $lid}})
            MERGE (u)-[:{rel}]->(l)
            """

            run_query(query, {
                "uid": user_id,
                "lid": lugar_id
            })

    print("✅ Relaciones creadas")

# =========================
# 4. COMENTARIOS CONTROLADOS
# =========================
def create_comments():
    print("💬 Creando comentarios controlados...")

    for i in range(5):  # primeros 5 usuarios
        for j in range(2):  # primeros 2 lugares
            tipo = random.choice(["lonjas", "parques"])

            query = """
            MATCH (u:Usuario {id: $uid})
            MATCH (l:Lugar {id: $lid})

            MERGE (c:Comentario {id: $cid})
            SET c.mensaje = $mensaje,
                c.ranking = $ranking,
                c.fecha = datetime()

            MERGE (u)-[:ESCRIBE]->(c)
            MERGE (c)-[:SOBRE]->(l)
            """

            #Datos controlados para pruebas
            run_query(query, {
                "uid": f"{i}",
                "lid": f"{tipo}_{j}",
                "cid": f"{i}_{tipo}_{j}",
                "mensaje": "Buen sitio",
                "ranking": random.randint(1, 5)
            })

    print("✅ Comentarios creados")
    
# =========================
# 5. RECALCULAR LIKES
# =========================
def update_likes():
    print("👍 Recalculando likes...")

    query = """
    MATCH (l:Lugar)

    OPTIONAL MATCH (l)<-[r:ME_GUSTA]-()

    WITH l, count(r) AS total
    SET l.likes = total
    """

    run_query(query)

    print("✅ Likes actualizados")


# =========================
# 6. RECALCULAR MEDIA
# =========================
def update_media():
    print("⭐ Recalculando medias...")

    query = """
    MATCH (l:Lugar)

    OPTIONAL MATCH (l)<-[:SOBRE]-(c:Comentario)

    WITH l, AVG(c.ranking) AS media
    SET l.media = coalesce(media, 0)
    """

    run_query(query)

    print("✅ Medias actualizadas")

# =========================
# MAIN
# =========================
def main():
    for tipo, file_path in FILES:
        load_geojson(file_path, tipo)

    #Controlamos el numero de usuarios random a crear
    n_users = 20

    create_users(n_users)
    create_random_relations(n_users)
    create_comments()

    update_likes()
    update_media()

    print("🎉 ETL MEMGRAPH COMPLETADO 🎉")

if __name__ == "__main__":
    main()