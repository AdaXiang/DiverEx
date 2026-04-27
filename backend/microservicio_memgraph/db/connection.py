#==============================
# Conexion con memgraph
#==============================
from neo4j import GraphDatabase
from microservicio_memgraph.config import settings

# Crear driver según auth
if settings.MEMGRAPH_USER and settings.MEMGRAPH_PASSWORD:
    driver = GraphDatabase.driver(
        settings.MEMGRAPH_URL,
        auth=(settings.MEMGRAPH_USER, settings.MEMGRAPH_PASSWORD)
    )
else:
    driver = GraphDatabase.driver(settings.MEMGRAPH_URL)

# Ejecucion de consultas, usado por los DAO
def run_query(query, params=None):
    with driver.session() as session:
        return list(session.run(query, params or {}))