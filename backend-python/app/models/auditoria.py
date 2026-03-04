from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.base_models import get_colombia_time

class AuditoriaAccesosBase(BaseModel):
    admin_id: int
    tabla_afectada: str
    accion: str

class AuditoriaAccesosCreate(AuditoriaAccesosBase):
    pass

class AuditoriaAccesos(AuditoriaAccesosBase):
    id: Optional[int] = None
    fecha_cambio: Optional[datetime] = Field(default_factory=get_colombia_time)
