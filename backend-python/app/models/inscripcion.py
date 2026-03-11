from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.base_models import get_colombia_time

class InscripcionBase(BaseModel):
    estudiante_id: int
    deporte_id: int
    programa_id: int

class InscripcionCreate(InscripcionBase):
    pass

class Inscripcion(InscripcionBase):
    id: Optional[int] = None
    estado: bool = True
    created_: Optional[datetime] = Field(default_factory=get_colombia_time)
    updated_: Optional[datetime] = Field(default_factory=get_colombia_time)
