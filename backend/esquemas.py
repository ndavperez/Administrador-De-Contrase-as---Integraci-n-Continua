from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# -------- Usuarios --------
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
    # v2: reemplaza orm_mode=True
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    token_acceso: str
    tipo_token: str


# -------- Contraseñas --------
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
    model_config = ConfigDict(from_attributes=True)

# (Opcional) Para detalle con la contraseña en claro cuando la pidas expresamente
class ContrasenaDetalle(BaseModel):
    id: int
    servicio: str
    usuario_servicio: str
    contrasena: str
    url: Optional[str] = None
    notas: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
