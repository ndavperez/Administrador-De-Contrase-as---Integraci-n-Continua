

import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

CLAVE_SECRETA = os.getenv("SECRET_KEY", "clave_temporal")
ALGORITMO = os.getenv("ALGORITHM", "HS256")
TIEMPO_EXPIRACION = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


CLAVE_FERNET = os.getenv("FERNET_KEY")
if not CLAVE_FERNET:
    CLAVE_FERNET = Fernet.generate_key().decode()
fernet = Fernet(CLAVE_FERNET.encode())

contexto_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def crear_hash(contrasena: str) -> str:
    return contexto_pwd.hash(contrasena)

def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    return contexto_pwd.verify(contrasena_plana, contrasena_hash)


def crear_token(datos: dict, duracion: timedelta = None):
    to_encode = datos.copy()
    expiracion = datetime.utcnow() + (duracion or timedelta(minutes=TIEMPO_EXPIRACION))
    to_encode.update({"exp": expiracion})
    return jwt.encode(to_encode, CLAVE_SECRETA, algorithm=ALGORITMO)

def decodificar_token(token: str):
    try:
        return jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
    except JWTError:
        return None


def cifrar_contrasena(contrasena: str) -> str:
    return fernet.encrypt(contrasena.encode()).decode()

def descifrar_contrasena(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
