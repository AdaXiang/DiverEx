from fastapi import FastAPI #Api para operaciones backend
from dotenv import load_dotenv #Seguridad de variables de entorno
import os #Trabajar con rutas 

#Variables entorno
load_dotenv()
COUCHDB_URL = os.getenv("COUCHDB_URL") #Prueba de que va bien las variables de entorno

#Inicializar la api
app = FastAPI()
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