from fastapi import APIRouter
from app.controllers.deporte_controller import deporte_controller
from app.models.all_models import Deporte

router = APIRouter()

@router.get("/deportes/", tags=["Deportes"])
async def get_deportes():
    return deporte_controller.get_all()

@router.get("/deportes/{id}", response_model=Deporte, tags=["Deportes"])
async def get_deporte(id: int):
    return deporte_controller.get_by_id(id)

@router.post("/deportes/", tags=["Deportes"])
async def create_deporte(deporte: Deporte):
    return deporte_controller.create(deporte.dict(exclude_unset=True))

@router.put("/deportes/{id}", tags=["Deportes"])
async def update_deporte(id: int, deporte: Deporte):
    return deporte_controller.update(id, deporte.dict(exclude_unset=True))

@router.delete("/deportes/{id}", tags=["Deportes"])
async def delete_deporte(id: int):
    return deporte_controller.delete(id)
