from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.base_models import get_colombia_time

class DeporteBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    imagen_logro: Optional[str] = None

class DeporteCreate(DeporteBase):
    pass

class Deporte(DeporteBase):
    id: Optional[int] = None
    estado: bool = True
    created_: Optional[datetime] = Field(default_factory=get_colombia_time)
    updated_: Optional[datetime] = Field(default_factory=get_colombia_time)
