from fastapi import APIRouter, Depends, HTTPException
from app.controllers.auth_controller import auth_controller
from app.models.user import LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest):
    return auth_controller.login(login_data)
