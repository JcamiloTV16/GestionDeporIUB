from fastapi import APIRouter
from app.controllers.torneo_controller import torneo_controller
from app.models.torneo import Torneo, TorneoCreate

router = APIRouter()

@router.get("/torneos/", tags=["Torneos"])
async def get_torneos():
    return torneo_controller.get_all()

@router.get("/torneos/{id}", response_model=Torneo, tags=["Torneos"])
async def get_torneo(id: int):
    return torneo_controller.get_by_id(id)

@router.post("/torneos/", response_model=Torneo, tags=["Torneos"])
async def create_torneo(torneo: TorneoCreate):
    return torneo_controller.create(torneo.dict(exclude_unset=True))

@router.put("/torneos/{id}", tags=["Torneos"])
async def update_torneo(id: int, torneo: Torneo):
    return torneo_controller.update(id, torneo.dict(exclude_unset=True))

@router.delete("/torneos/{id}", tags=["Torneos"])
async def delete_torneo(id: int):
    return torneo_controller.delete(id)
