from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.base_models import get_colombia_time

class UserBase(BaseModel):
    rol_id: int
    tipo_documento_id: int
    numero_documento: str
    facultad_id: int
    nombre: str
    correo: str

class UserCreate(UserBase):
    contrasena: str

class User(UserBase):
    id: Optional[int] = None
    estado: bool = True
    created_: datetime = Field(default_factory=get_colombia_time)
    updated_: datetime = Field(default_factory=get_colombia_time)

class LoginRequest(BaseModel):
    correo: str
    contrasena: str

class UserData(BaseModel):
    id: int
    nombre: str
    correo: str
    rol: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserData

class TokenData(BaseModel):
    user_id: Optional[str] = None
