from fastapi import APIRouter
from app.controllers.horario_controller import horario_controller
from app.models.all_models import Horario

router = APIRouter()

@router.get("/horarios/", tags=["Horarios"])
async def get_horarios():
    return horario_controller.get_all()

@router.get("/horarios/{id}", response_model=Horario, tags=["Horarios"])
async def get_horario(id: int):
    return horario_controller.get_by_id(id)

@router.post("/horarios/", tags=["Horarios"])
async def create_horario(horario: Horario):
    return horario_controller.create(horario.dict(exclude_unset=True))

@router.put("/horarios/{id}", tags=["Horarios"])
async def update_horario(id: int, horario: Horario):
    return horario_controller.update(id, horario.dict(exclude_unset=True))

@router.delete("/horarios/{id}", tags=["Horarios"])
async def delete_horario(id: int):
    return horario_controller.delete(id)
