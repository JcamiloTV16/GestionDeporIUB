from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.base_models import get_colombia_time

class ModuloBase(BaseModel):
    nombre_modulo: str
    ruta_url: Optional[str] = None

class ModuloCreate(ModuloBase):
    pass

class Modulo(ModuloBase):
    id: Optional[int] = None
    estado: bool = True
    created_: Optional[datetime] = Field(default_factory=get_colombia_time)
    updated_: Optional[datetime] = Field(default_factory=get_colombia_time)
