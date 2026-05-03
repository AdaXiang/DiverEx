from fastapi import FastAPI #Api para operaciones backend
from microservicio_memgraph.routes.usuarioRoutes import router as usuarioRouter
from microservicio_memgraph.routes.visitaRoutes import router as visitaRouter
from microservicio_memgraph.routes.favoritoRoutes import router as favoritoRouter
from microservicio_memgraph.routes.meGustaRoutes import router as meGustaRouter
from microservicio_memgraph.routes.comentarioRoutes import router as comentarioRouter
from microservicio_memgraph.routes.preferenciasRoutes import router as preferenciaRouter
from microservicio_memgraph.routes.lugarRoutes import router as lugarRouter
from fastapi.middleware.cors import CORSMiddleware

#Inicializar la api
app = FastAPI(
    title="DiverEx API",
    description="""
API para gestión de usuarios y recomendaciones de lugares.

## Funcionalidades
- 👤 Usuarios
- 📍 Lugares (Parques / Lonjas)
- ❤️ Likes, favoritos y visitas
- 💬 Comentarios con ranking
- 🤖 Recomendaciones personalizadas

## Notas
- Los lugares tienen media de valoración y número de likes
- Se pueden filtrar las recomendaciones por múltiples atributos
""",
    version="1.0.0",
    contact={
        "name": "Manuel Solis Gómez",
        "email": "masogo008@gmail.com"
    }
)

#CORS
origins = [
    "http://localhost:3333",
    "http://127.0.0.1:3333",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint básico
@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API de Badajoz DiverEx 🚀"
    }

# Endpoint de prueba
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "backend running"
    }
    
app.include_router(usuarioRouter, prefix="/usuarios")
app.include_router(visitaRouter, prefix="/visitas")
app.include_router(favoritoRouter, prefix="/favoritos")
app.include_router(meGustaRouter, prefix="/likes")
app.include_router(comentarioRouter, prefix="/comentarios")
app.include_router(preferenciaRouter, prefix="/preferencias")
app.include_router(lugarRouter, prefix="/lugares")