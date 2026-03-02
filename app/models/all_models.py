from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, time
import pytz


def get_colombia_time():
    return datetime.now(pytz.timezone('America/Bogota'))



class RoleBase(BaseModel):
    nombre_rol: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: Optional[int] = None
    estado: bool = True
    create_: Optional[datetime] = Field(default_factory=get_colombia_time)
    update_: Optional[datetime] = Field(default_factory=get_colombia_time)

class ModuloBase(BaseModel):
    nombre_modulo: str
    ruta_url: Optional[str] = None

class ModuloCreate(ModuloBase):
    pass

class Modulo(ModuloBase):
    id: Optional[int] = None
    estado: bool = True
    create_: Optional[datetime] = Field(default_factory=get_colombia_time)
    update_: Optional[datetime] = Field(default_factory=get_colombia_time)

class PermisoRolBase(BaseModel):
    rol_id: int
    modulo_id: int

class PermisoRolCreate(PermisoRolBase):
    pass

class PermisoRol(PermisoRolBase):
    id: Optional[int] = None
    estado: bool = True
    create_: Optional[datetime] = Field(default_factory=get_colombia_time)
    update_: Optional[datetime] = Field(default_factory=get_colombia_time)

class DeporteBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    imagen_logro: Optional[str] = None

class DeporteCreate(DeporteBase):
    pass

class Deporte(DeporteBase):
    id: Optional[int] = None
    estado: bool = True
    create_: Optional[datetime] = Field(default_factory=get_colombia_time)
    update_: Optional[datetime] = Field(default_factory=get_colombia_time)

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

class HorarioBase(BaseModel):
    deporte_id: int
    dia_semana: str
    hora_inicio: time
    hora_fin: time
    lugar: Optional[str] = None

class HorarioCreate(HorarioBase):
    pass

class Horario(HorarioBase):
    id: Optional[int] = None
    estado: bool = True
    create_: Optional[datetime] = Field(default_factory=get_colombia_time)
    update_: Optional[datetime] = Field(default_factory=get_colombia_time)

class InscripcionBase(BaseModel):
    estudiante_id: int
    deporte_id: int
    programa_id: int

class InscripcionCreate(InscripcionBase):
    pass

class Inscripcion(InscripcionBase):
    id: Optional[int] = None
    estado: bool = True
    create_: Optional[datetime] = Field(default_factory=get_colombia_time)
    update_: Optional[datetime] = Field(default_factory=get_colombia_time)

class AuditoriaAccesosBase(BaseModel):
    admin_id: int
    tabla_afectada: str
    accion: str

class AuditoriaAccesosCreate(AuditoriaAccesosBase):
    pass

class AuditoriaAccesos(AuditoriaAccesosBase):
    id: Optional[int] = None
    fecha_cambio: Optional[datetime] = Field(default_factory=get_colombia_time)

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

# Eliminar modelo Usuario antiguo (ya no existe en la DB con ese nombre)
