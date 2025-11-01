# database.py
# Configuración de conexión a la base de datos MySQL

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

USUARIO_BD = os.getenv("DB_USER", "root")
CLAVE_BD = os.getenv("DB_PASSWORD", "root")
HOST_BD = os.getenv("DB_HOST", "localhost")
PUERTO_BD = os.getenv("DB_PORT", "3306")
NOMBRE_BD = os.getenv("DB_NAME", "gestor_contrasenas")

URL_BD = f"postgresql+psycopg2://{USUARIO_BD}:{CLAVE_BD}@{HOST_BD}:{PUERTO_BD}/{NOMBRE_BD}"



motor = create_engine(URL_BD, pool_pre_ping=True)
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)
Base = declarative_base()

def obtener_sesion():
    """Devuelve una sesión de base de datos para usar en los endpoints"""
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()
