-- ===========================================================
--  Inicialización de base de datos para VAULT PASSWORD MANAGER
--  Proyecto: Integración Continua - FastAPI + PostgreSQL + Docker
--  Archivo ejecutado AUTOMÁTICAMENTE al crear el volumen por primera vez
-- ===========================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS seguridad;

-- ===========================================================
-- TABLA: usuarios
-- ===========================================================
CREATE TABLE IF NOT EXISTS seguridad.usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    nombre      VARCHAR(100) NOT NULL,
    apellido    VARCHAR(100) NOT NULL,
    correo      VARCHAR(120) UNIQUE NOT NULL,

    -- Contraseña HASH, no la contraseña real
    contrasena  TEXT NOT NULL,

    creado_en   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_usuarios_correo
    ON seguridad.usuarios (correo);


-- ===========================================================
-- TABLA: contrasenas
-- ===========================================================
CREATE TABLE IF NOT EXISTS seguridad.contrasenas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    usuario_id UUID NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    usuario_login VARCHAR(150),
    password_cifrada TEXT NOT NULL,
    sitio_web TEXT,
    notas TEXT,

    creado_en   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES seguridad.usuarios(id)
        ON DELETE CASCADE
);


CREATE INDEX IF NOT EXISTS idx_contrasenas_usuario
    ON seguridad.contrasenas (usuario_id);


-- ===========================================================
-- Actualización automática del campo "actualizado_en"
-- ===========================================================

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_update_usuarios
BEFORE UPDATE ON seguridad.usuarios
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();


CREATE TRIGGER t_update_contrasenas
BEFORE UPDATE ON seguridad.contrasenas
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

