from fastapi import APIRouter
from app.controllers.inscripcion_torneo_controller import inscripcion_torneo_controller
from app.models.inscripcion_torneo import InscripcionTorneoCreate, InscripcionTorneoUpdate

router = APIRouter()

@router.post("/inscripciones-torneo/", tags=["Inscripciones Torneo"])
async def inscribir_estudiante(data: InscripcionTorneoCreate):
    return inscripcion_torneo_controller.inscribir_estudiante(data.torneo_id, data.estudiante_id)

@router.get("/inscripciones-torneo/torneo/{torneo_id}", tags=["Inscripciones Torneo"])
async def get_inscritos_por_torneo(torneo_id: int):
    return inscripcion_torneo_controller.get_inscritos_por_torneo(torneo_id)

@router.get("/inscripciones-torneo/estudiante/{estudiante_id}", tags=["Inscripciones Torneo"])
async def get_torneos_por_estudiante(estudiante_id: int):
    return inscripcion_torneo_controller.get_torneos_por_estudiante(estudiante_id)

@router.patch("/inscripciones-torneo/{id}/estado", tags=["Inscripciones Torneo"])
async def actualizar_estado_inscripcion(id: int, data: InscripcionTorneoUpdate):
    return inscripcion_torneo_controller.actualizar_estado_inscripcion(id, data.estado_inscripcion)

@router.delete("/inscripciones-torneo/{id}", tags=["Inscripciones Torneo"])
async def cancelar_inscripcion(id: int):
    return inscripcion_torneo_controller.cancelar_inscripcion(id)
