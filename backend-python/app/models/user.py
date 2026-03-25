from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.base_models import get_colombia_time

class UserBase(BaseModel):
    rol_id: int
    tipo_documento_id: int
    numero_documento: str
    facultad_id: int
    nivel_educativo_id: Optional[int] = None
    programa_id: Optional[int] = None
    nombre: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: Optional[int] = None
    estado: bool = True
    create_: datetime = Field(default_factory=get_colombia_time)
    update_: datetime = Field(default_factory=get_colombia_time)

class UserUpdate(BaseModel):
    rol_id: Optional[int] = None
    tipo_documento_id: Optional[int] = None
    numero_documento: Optional[str] = None
    facultad_id: Optional[int] = None
    nivel_educativo_id: Optional[int] = None
    programa_id: Optional[int] = None
    nombre: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    estado: Optional[bool] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class UserData(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    programa_id: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserData

class TokenData(BaseModel):
    user_id: Optional[str] = None
