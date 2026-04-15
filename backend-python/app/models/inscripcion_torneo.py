from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.base_models import get_colombia_time

class InscripcionTorneoBase(BaseModel):
    torneo_id: int
    estudiante_id: int

class InscripcionTorneoCreate(InscripcionTorneoBase):
    pass

class InscripcionTorneoUpdate(BaseModel):
    estado_inscripcion: str  # Pendiente, Aprobada, Rechazada

class InscripcionTorneo(InscripcionTorneoBase):
    id: Optional[int] = None
    estado_inscripcion: Optional[str] = "Pendiente"
    estado: bool = True
    create_: Optional[datetime] = Field(default_factory=get_colombia_time)
    update_: Optional[datetime] = Field(default_factory=get_colombia_time)
