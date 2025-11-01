# models.py
# Definición de las tablas de la base de datos

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120))
    apellido = Column(String(120))
    correo = Column(String(255), unique=True, index=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)

    contrasenas = relationship("Contrasena", back_populates="propietario", cascade="all, delete-orphan")

class Contrasena(Base):
    __tablename__ = "contrasenas"
    id = Column(Integer, primary_key=True, index=True)
    servicio = Column(String(150), index=True)
    usuario_servicio = Column(String(150), index=True)
    contrasena_cifrada = Column(Text, nullable=False)
    url = Column(String(255), nullable=True)
    notas = Column(Text, nullable=True)
    propietario_id = Column(Integer, ForeignKey("usuarios.id"))

    propietario = relationship("Usuario", back_populates="contrasenas")
