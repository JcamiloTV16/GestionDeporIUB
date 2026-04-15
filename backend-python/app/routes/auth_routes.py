from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.controllers.auth_controller import auth_controller
from app.models.user import LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class RecoverRequest(BaseModel):
    email: str

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest):
    return auth_controller.login(login_data)

@router.post("/recover")
def recover_password(data: RecoverRequest):
    return auth_controller.recover_password(data.email)
