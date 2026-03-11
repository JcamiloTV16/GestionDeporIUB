from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.base_models import get_colombia_time

class RoleBase(BaseModel):
    nombre_rol: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: Optional[int] = None
    estado: bool = True
    created_: Optional[datetime] = Field(default_factory=get_colombia_time)
    updated_: Optional[datetime] = Field(default_factory=get_colombia_time)
