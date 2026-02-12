from fastapi import APIRouter
from app.controllers.permiso_controller import permiso_controller
from app.models.all_models import PermisoRol

router = APIRouter()

@router.get("/permisos/", tags=["Permisos"])
async def get_permisos():
    return permiso_controller.get_all()

@router.get("/permisos/{id}", response_model=PermisoRol, tags=["Permisos"])
async def get_permiso(id: int):
    return permiso_controller.get_by_id(id)

@router.post("/permisos/", tags=["Permisos"])
async def create_permiso(permiso: PermisoRol):
    return permiso_controller.create(permiso.dict(exclude_unset=True))

@router.put("/permisos/{id}", tags=["Permisos"])
async def update_permiso(id: int, permiso: PermisoRol):
    return permiso_controller.update(id, permiso.dict(exclude_unset=True))

@router.delete("/permisos/{id}", tags=["Permisos"])
async def delete_permiso(id: int):
    return permiso_controller.delete(id)
