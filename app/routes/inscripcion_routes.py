from fastapi import APIRouter
from app.controllers.inscripcion_controller import inscripcion_controller
from app.models.all_models import Inscripcion

router = APIRouter()

@router.get("/inscripciones/", tags=["Inscripciones"])
async def get_inscripciones():
    return inscripcion_controller.get_all()

@router.get("/inscripciones/{id}", response_model=Inscripcion, tags=["Inscripciones"])
async def get_inscripcion(id: int):
    return inscripcion_controller.get_by_id(id)

@router.post("/inscripciones/", tags=["Inscripciones"])
async def create_inscripcion(inscripcion: Inscripcion):
    return inscripcion_controller.create(inscripcion.dict(exclude_unset=True))

@router.put("/inscripciones/{id}", tags=["Inscripciones"])
async def update_inscripcion(id: int, inscripcion: Inscripcion):
    return inscripcion_controller.update(id, inscripcion.dict(exclude_unset=True))

@router.delete("/inscripciones/{id}", tags=["Inscripciones"])
async def delete_inscripcion(id: int):
    return inscripcion_controller.delete(id)
