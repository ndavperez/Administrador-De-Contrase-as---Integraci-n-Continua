

from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioCrear(BaseModel):
    nombre: str
    apellido: str
    correo: EmailStr
    contrasena: str

class UsuarioMostrar(BaseModel):
    id: int
    nombre: str
    apellido: str
    correo: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    token_acceso: str
    tipo_token: str


class ContrasenaCrear(BaseModel):
    servicio: str
    usuario_servicio: str
    contrasena: str
    url: Optional[str] = None
    notas: Optional[str] = None

class ContrasenaMostrar(BaseModel):
    id: int
    servicio: str
    usuario_servicio: str
    url: Optional[str] = None
    notas: Optional[str] = None

    class Config:
        orm_mode = True
