from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time

class Role(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    estado: bool = True

class Modulo(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    estado: bool = True

class PermisoRol(BaseModel):
    id: Optional[int] = None
    rol_id: int
    modulo_id: int
    acceso: bool = True
    estado: bool = True

class Deporte(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    estado: bool = True

class Entrenador(BaseModel):
    id: Optional[int] = None
    usuario_id: int
    deporte_id: int
    biografia: Optional[str] = None
    estado: bool = True

class Horario(BaseModel):
    id: Optional[int] = None
    deporte_id: int
    entrenador_id: int
    dia_semana: str
    hora_inicio: time
    hora_fin: time
    lugar: Optional[str] = None
    estado: bool = True
    created_: Optional[datetime] = None
    updated_: Optional[datetime] = None

class Inscripcion(BaseModel):
    id: Optional[int] = None
    usuario_id: int
    horario_id: int
    programa_id: int
    fecha_inscripcion: Optional[datetime] = None
    estado: bool = True
    created_: Optional[datetime] = None
    updated_: Optional[datetime] = None

class AuditoriaAccesos(BaseModel):
    id: Optional[int] = None
    admin_id: int
    tabla_afectada: str
    accion: str
    fecha_cambio: Optional[datetime] = None


class Usuario(BaseModel):
    id: Optional[int] = None
    rol_id: int
    tipo_documento_id: Optional[int] = None
    numero_documento: Optional[str] = None
    facultad_id: Optional[int] = None
    nombre: str
    apellido: str
    contrasena: str
    estado: bool = True
