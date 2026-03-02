from fastapi import APIRouter
from app.controllers.modulo_controller import modulo_controller
from app.models import Modulo, ModuloCreate

router = APIRouter()

@router.get("/modulos/", tags=["Modulos"])
async def get_modulos():
    return modulo_controller.get_all()

@router.get("/modulos/{id}", response_model=Modulo, tags=["Modulos"])
async def get_modulo(id: int):
    return modulo_controller.get_by_id(id)

@router.post("/modulos/", response_model=Modulo, tags=["Modulos"])
async def create_modulo(modulo: ModuloCreate):
    return modulo_controller.create(modulo.dict(exclude_unset=True))

@router.put("/modulos/{id}", tags=["Modulos"])
async def update_modulo(id: int, modulo: Modulo):
    return modulo_controller.update(id, modulo.dict(exclude_unset=True))

@router.delete("/modulos/{id}", tags=["Modulos"])
async def delete_modulo(id: int):
    return modulo_controller.delete(id)
