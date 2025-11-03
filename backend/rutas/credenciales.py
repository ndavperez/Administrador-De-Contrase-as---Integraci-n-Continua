

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from esquemas import ContrasenaCrear, ContrasenaMostrar, ContrasenaDetalle
from models import Contrasena, Usuario
from seguridad import cifrar_contrasena, decodificar_token, oauth2_scheme, descifrar_contrasena
from database import obtener_sesion
from database import obtener_sesion
from fastapi import Depends

router = APIRouter(prefix="/contrasenas", tags=["Contraseñas"])


# --- Middleware simple (token en Authorization) ---
def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(obtener_sesion),
):
    datos = decodificar_token(token)
    if not datos or "sub" not in datos:
        raise HTTPException(status_code=401, detail="Token inválido.")
    usuario = db.query(Usuario).filter(Usuario.id == int(datos["sub"])).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado.")
    return usuario



@router.post("/", response_model=ContrasenaMostrar, status_code=201)
def crear_contrasena(
    datos: ContrasenaCrear,
    db: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
):
    cifrada = cifrar_contrasena(datos.contrasena)
    nueva = Contrasena(
        servicio=datos.servicio,
        usuario_servicio=datos.usuario_servicio,
        contrasena_cifrada=cifrada,
        url=datos.url,
        notas=datos.notas,
        propietario_id=usuario_actual.id  
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.get("/", response_model=List[ContrasenaMostrar])
def listar_contrasenas(buscar: Optional[str] = None, db: Session = Depends(obtener_sesion)):
    """Lista todas las contraseñas guardadas. Permite buscar por nombre del servicio."""
    consulta = db.query(Contrasena)
    
    if buscar:
        texto = f"%{buscar}%"
        consulta = consulta.filter(Contrasena.servicio.ilike(texto))
    
    return consulta.all()

@router.get("/{id}", response_model=ContrasenaDetalle)
def obtener_contrasena(
    id: int,
    db: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
):
    item = db.query(Contrasena).filter(
        Contrasena.id == id,
        Contrasena.propietario_id == usuario_actual.id
    ).first()
    if not item:
        raise HTTPException(404, "No encontrado")
    return ContrasenaDetalle(
        id=item.id,
        servicio=item.servicio,
        usuario_servicio=item.usuario_servicio,
        contrasena=descifrar_contrasena(item.contrasena_cifrada),
        url=item.url,
        notas=item.notas
    )
