from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import router as user_router
from app.routes.role_routes import router as role_router
from app.routes.modulo_routes import router as modulo_router
from app.routes.permiso_routes import router as permiso_router
from app.routes.deporte_routes import router as deporte_router
from app.routes.entrenador_routes import router as entrenador_router
from app.routes.horario_routes import router as horario_router
from app.routes.inscripcion_routes import router as inscripcion_router
from app.routes.auditoria_routes import router as auditoria_router

app = FastAPI()

origins = [
    #"http://localhost.tiangolo.com",
    #"https://localhost.tiangolo.com",
    "http://localhost",
    #"http://localhost:8080",
    "*" # Permitiendo todos para desarrollo, ajustar en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(role_router)
app.include_router(modulo_router)
app.include_router(permiso_router)
app.include_router(deporte_router)
app.include_router(entrenador_router)
app.include_router(horario_router)
app.include_router(inscripcion_router)
app.include_router(auditoria_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)