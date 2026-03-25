from fastapi import APIRouter
from app.controllers.inscripcion_controller import inscripcion_controller
from app.models import Inscripcion, InscripcionCreate

router = APIRouter()

@router.get("/inscripciones/", tags=["Inscripciones"])
async def get_inscripciones():
    return inscripcion_controller.get_all()

@router.get("/inscripciones/{id}", response_model=Inscripcion, tags=["Inscripciones"])
async def get_inscripcion(id: int):
    return inscripcion_controller.get_by_id(id)

@router.get("/inscripciones/horario/{horario_id}", tags=["Inscripciones"])
async def get_estudiantes_por_horario(horario_id: int):
    return inscripcion_controller.get_estudiantes_por_horario(horario_id)

@router.get("/inscripciones/estudiante/{estudiante_id}/deportes", tags=["Inscripciones"])
async def get_deportes_por_estudiante(estudiante_id: int):
    return inscripcion_controller.get_deportes_por_estudiante(estudiante_id)
@router.post("/inscripciones/", response_model=Inscripcion, tags=["Inscripciones"])
async def create_inscripcion(inscripcion: InscripcionCreate):
    return inscripcion_controller.create(inscripcion.dict(exclude_unset=True))

@router.put("/inscripciones/{id}", tags=["Inscripciones"])
async def update_inscripcion(id: int, inscripcion: Inscripcion):
    return inscripcion_controller.update(id, inscripcion.dict(exclude_unset=True))

@router.delete("/inscripciones/{id}", tags=["Inscripciones"])
async def delete_inscripcion(id: int):
    return inscripcion_controller.delete(id)
