#==============================
# Configuraciones centralizadas, aislamos los cambios y configuraciones del microservicio
#==============================
import os
from dotenv import load_dotenv

#Carga las variables del entorno
load_dotenv()

#Clase de configuraciones
class Settings:
    MEMGRAPH_HOST = os.getenv("MEMGRAPH_HOST", "localhost")
    MEMGRAPH_PORT = os.getenv("MEMGRAPH_PORT", "7687")
    MEMGRAPH_URL = os.getenv("MEMGRAPH_URL", f"bolt://{self.MEMGRAPH_HOST}:{self.MEMGRAPH_PORT}")
    #Por defecto no aporta seguridad Memgraph
    MEMGRAPH_USER = os.getenv("MEMGRAPH_USER", "")
    MEMGRAPH_PASSWORD = os.getenv("MEMGRAPH_PASSWORD", "")


settings = Settings()