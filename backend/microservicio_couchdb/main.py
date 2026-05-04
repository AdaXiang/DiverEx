from fastapi import FastAPI #Api para operaciones backend
from dotenv import load_dotenv #Seguridad de variables de entorno
from fastapi.middleware.cors import CORSMiddleware
from routes.LugarRoutes import router as place_router
import os 

#Variables entorno
load_dotenv()
COUCHDB_URL = os.getenv("COUCHDB_URL") #Prueba de que va bien las variables de entorno

#Inicializar la api
app = FastAPI(
    title="API de Sitios de Interés - Badajoz",
    description="Backend para consultar lonjas, parques y otros puntos de interés de la provincia.",
    version="1.0.0"
)

# Configuración de CORS
# Esto es vital para que el frontend (React) pueda hacer peticiones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambiar "*" por la URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de rutas
# El 'prefix' ayuda a organizar la URL, ej: http://localhost:8000/api/sitio/...
app.include_router(place_router, prefix="/api", tags=["Sitios"])

# Endpoint básico
@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API de Badajoz GeoApp 🚀"
    }

# Endpoint de prueba
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "backend running"
    }