from fastapi import APIRouter, Depends
from app.controllers.user_controller import user_controller
from app.models import User, UserCreate
from app.dependencies.permissions import PermissionChecker

router = APIRouter()

# Asumiendo que el ID del módulo de Usuarios es 1 (ver database.sql)
PROTECTED = Depends(PermissionChecker(modulo_id=1))

@router.get("/usuarios/", tags=["Usuarios"], dependencies=[PROTECTED])
async def get_usuarios():
    return user_controller.get_all()

@router.get("/usuarios/inactivos/", tags=["Usuarios"], dependencies=[PROTECTED])
async def get_usuarios_inactivos():
    return user_controller.get_inactive()

@router.get("/usuarios/{id}", response_model=User, tags=["Usuarios"], dependencies=[PROTECTED])
async def get_usuario(id: int):
    return user_controller.get_by_id(id)

@router.post("/usuarios/", response_model=User, tags=["Usuarios"])
def create_user(user: UserCreate): 
    return user_controller.create_user(user)

from app.models.user import User, UserCreate, UserUpdate
...
@router.put("/usuarios/{id}", tags=["Usuarios"], dependencies=[PROTECTED])
async def update_usuario(id: int, user: UserUpdate):
    return user_controller.update(id, user.dict(exclude_unset=True))

@router.delete("/usuarios/{id}", tags=["Usuarios"], dependencies=[PROTECTED])
async def delete_usuario(id: int):
    return user_controller.delete(id)

@router.post("/usuarios/{id}/reactivar/", tags=["Usuarios"], dependencies=[PROTECTED])
async def reactivate_usuario(id: int):
    return user_controller.reactivate(id)