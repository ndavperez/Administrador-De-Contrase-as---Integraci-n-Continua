

from fastapi import FastAPI
from database import Base, motor
from rutas import usuarios, credenciales
import models  

# Crear las tablas automáticamente en la base de datos si no existen

Base.metadata.create_all(bind=motor)


# Crear la aplicación FastAPI
app = FastAPI(title="Gestor de Contraseñas - Backend en Español")

# Incluir las rutas (usuarios y contraseñas)
app.include_router(usuarios.router)
app.include_router(credenciales.router)
