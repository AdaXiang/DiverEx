from fastapi import FastAPI #Api para operaciones backend
from microservicio_memgraph.routes.usuarioRoutes import router as usuarioRouter
from microservicio_memgraph.routes.visitaRoutes import router as visitaRouter
from microservicio_memgraph.routes.favoritoRoutes import router as favoritoRouter
from microservicio_memgraph.routes.meGustaRoutes import router as meGustaRouter
from microservicio_memgraph.routes.comentarioRoutes import router as comentarioRouter
from microservicio_memgraph.routes.preferenciasRoutes import router as preferenciaRouter
from microservicio_memgraph.routes.lugarRoutes import router as lugarRouter

#Inicializar la api
app = FastAPI()

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