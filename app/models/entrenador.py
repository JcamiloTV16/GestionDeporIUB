from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.base_models import get_colombia_time

class EntrenadorBase(BaseModel):
    usuario_id: int
    deporte_id: int
    biografia: Optional[str] = None

class EntrenadorCreate(EntrenadorBase):
    pass

class Entrenador(EntrenadorBase):
    id: Optional[int] = None
    estado: bool = True
    create_: Optional[datetime] = Field(default_factory=get_colombia_time)
    update_: Optional[datetime] = Field(default_factory=get_colombia_time)
