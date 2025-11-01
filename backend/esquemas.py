# esquemas.py
# Modelos Pydantic (entrada y salida de datos)

from pydantic import BaseModel, EmailStr
from typing import Optional

# ----- Usuario -----
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

# ----- Token -----
class Token(BaseModel):
    token_acceso: str
    tipo_token: str

# ----- Contraseñas -----
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
