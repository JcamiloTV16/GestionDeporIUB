from fastapi import APIRouter
from app.controllers.entrenador_controller import entrenador_controller
from app.models.all_models import Entrenador

router = APIRouter()

@router.get("/entrenadores/", tags=["Entrenadores"])
async def get_entrenadores():
    return entrenador_controller.get_all()

@router.get("/entrenadores/{id}", response_model=Entrenador, tags=["Entrenadores"])
async def get_entrenador(id: int):
    return entrenador_controller.get_by_id(id)

@router.post("/entrenadores/", tags=["Entrenadores"])
async def create_entrenador(entrenador: Entrenador):
    return entrenador_controller.create(entrenador.dict(exclude_unset=True))

@router.put("/entrenadores/{id}", tags=["Entrenadores"])
async def update_entrenador(id: int, entrenador: Entrenador):
    return entrenador_controller.update(id, entrenador.dict(exclude_unset=True))

@router.delete("/entrenadores/{id}", tags=["Entrenadores"])
async def delete_entrenador(id: int):
    return entrenador_controller.delete(id)
