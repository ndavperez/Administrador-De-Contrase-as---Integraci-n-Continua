# rutas/usuarios.py
# Rutas relacionadas con registro y autenticación

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from esquemas import UsuarioCrear, UsuarioMostrar, Token
from models import Usuario
from seguridad import crear_hash, verificar_contrasena, crear_token
from database import obtener_sesion

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/registro", response_model=UsuarioMostrar, status_code=201)
def registrar_usuario(usuario: UsuarioCrear, db: Session = Depends(obtener_sesion)):
    """Registrar un nuevo usuario."""
    existente = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        correo=usuario.correo,
        contrasena_hash=crear_hash(usuario.contrasena)
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.post("/login", response_model=Token)
def iniciar_sesion(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(obtener_sesion)):
    """Iniciar sesión y obtener un token JWT."""
    usuario = db.query(Usuario).filter(Usuario.correo == form_data.username).first()
    if not usuario or not verificar_contrasena(form_data.password, usuario.contrasena_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")

    duracion = timedelta(minutes=60)
    token = crear_token({"sub": str(usuario.id)}, duracion)
    return {"token_acceso": token, "tipo_token": "bearer"}
