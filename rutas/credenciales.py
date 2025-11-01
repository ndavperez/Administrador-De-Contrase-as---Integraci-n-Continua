# rutas/credenciales.py
# Rutas CRUD para las contraseñas de los servicios

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from esquemas import ContrasenaCrear, ContrasenaMostrar
from models import Contrasena, Usuario
from seguridad import cifrar_contrasena, decodificar_token
from database import obtener_sesion

router = APIRouter(prefix="/contrasenas", tags=["Contraseñas"])


# --- Middleware simple (token en Authorization) ---
def obtener_usuario_actual(token: str, db: Session):
    """Verifica el token y devuelve el usuario actual."""
    datos = decodificar_token(token)
    if not datos or "sub" not in datos:
        raise HTTPException(status_code=401, detail="Token inválido.")
    
    usuario = db.query(Usuario).filter(Usuario.id == int(datos["sub"])).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado.")
    
    return usuario


# --- Crear una nueva contraseña ---
@router.post("/", response_model=ContrasenaMostrar, status_code=201)
def crear_contrasena(datos: ContrasenaCrear, db: Session = Depends(obtener_sesion)):
    """Guarda una nueva contraseña cifrada en la base de datos."""
    cifrada = cifrar_contrasena(datos.contrasena)
    
    nueva = Contrasena(
        servicio=datos.servicio,
        usuario_servicio=datos.usuario_servicio,
        contrasena_cifrada=cifrada,
        url=datos.url,
        notas=datos.notas,
        propietario_id=1  # temporal: más adelante se obtendrá desde el token
    )
    
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    
    return nueva


# --- Listar contraseñas ---
@router.get("/", response_model=List[ContrasenaMostrar])
def listar_contrasenas(buscar: Optional[str] = None, db: Session = Depends(obtener_sesion)):
    """Lista todas las contraseñas guardadas. Permite buscar por nombre del servicio."""
    consulta = db.query(Contrasena)
    
    if buscar:
        texto = f"%{buscar}%"
        consulta = consulta.filter(Contrasena.servicio.ilike(texto))
    
    return consulta.all()
