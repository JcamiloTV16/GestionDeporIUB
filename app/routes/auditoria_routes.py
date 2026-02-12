from fastapi import APIRouter
from app.controllers.auditoria_controller import auditoria_controller
from app.models.all_models import AuditoriaAccesos

router = APIRouter()

@router.get("/auditoria/", tags=["Auditoria"])
async def get_auditorias():
    return auditoria_controller.get_all()

@router.get("/auditoria/{id}", response_model=AuditoriaAccesos, tags=["Auditoria"])
async def get_auditoria(id: int):
    return auditoria_controller.get_by_id(id)

@router.post("/auditoria/", tags=["Auditoria"])
async def create_auditoria(auditoria: AuditoriaAccesos):
    return auditoria_controller.create(auditoria.dict(exclude_unset=True))
