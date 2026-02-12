from fastapi import APIRouter, Depends
from app.controllers.user_controller import user_controller
from app.models.all_models import Usuario
from app.dependencies.permissions import PermissionChecker

router = APIRouter()

# Asumiendo que el ID del módulo de Usuarios es 1 (ver database.sql)
PROTECTED = Depends(PermissionChecker(modulo_id=1))

@router.get("/usuarios/", tags=["Usuarios"], dependencies=[PROTECTED])
async def get_usuarios():
    return user_controller.get_all()

@router.get("/usuarios/{id}", response_model=Usuario, tags=["Usuarios"], dependencies=[PROTECTED])
async def get_usuario(id: int):
    return user_controller.get_by_id(id)

@router.post("/usuarios/", tags=["Usuarios"], dependencies=[PROTECTED])
async def create_usuario(usuario: Usuario):
    return user_controller.create(usuario.dict(exclude_unset=True))

@router.put("/usuarios/{id}", tags=["Usuarios"], dependencies=[PROTECTED])
async def update_usuario(id: int, usuario: Usuario):
    return user_controller.update(id, usuario.dict(exclude_unset=True))

@router.delete("/usuarios/{id}", tags=["Usuarios"], dependencies=[PROTECTED])
async def delete_usuario(id: int):
    return user_controller.delete(id)