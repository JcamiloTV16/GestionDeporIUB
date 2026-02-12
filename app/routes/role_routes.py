from fastapi import APIRouter
from app.controllers.role_controller import role_controller
from app.models.all_models import Role

router = APIRouter()

@router.get("/roles/", tags=["Roles"])
async def get_roles():
    return role_controller.get_all()

@router.get("/roles/{id}", response_model=Role, tags=["Roles"])
async def get_role(id: int):
    return role_controller.get_by_id(id)

@router.post("/roles/", tags=["Roles"])
async def create_role(role: Role):
    return role_controller.create(role.dict(exclude_unset=True))

@router.put("/roles/{id}", tags=["Roles"])
async def update_role(id: int, role: Role):
    return role_controller.update(id, role.dict(exclude_unset=True))

@router.delete("/roles/{id}", tags=["Roles"])
async def delete_role(id: int):
    return role_controller.delete(id)
