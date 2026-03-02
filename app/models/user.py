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
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: Optional[int] = None
    estado: bool = True
    create_: datetime = Field(default_factory=get_colombia_time)
    update_: datetime = Field(default_factory=get_colombia_time)
