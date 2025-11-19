# 🔐 Gestor de Contraseñas con FastAPI, PostgreSQL, Docker y Jenkins CI

Sistema de gestión segura de contraseñas con backend en FastAPI, base de datos PostgreSQL y frontend en JavaScript, orquestado con Docker Compose y con **pipeline de Integración Continua en Jenkins** que construye imágenes, levanta el stack en modo CI y ejecuta pruebas automáticas (_smoke tests_) sobre la API.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.121.2-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-informational.svg)
![Jenkins](https://img.shields.io/badge/Jenkins-CI/CD-red.svg)
![Security](https://img.shields.io/badge/Security-JWT%20%7C%20Fernet%20%7C%20bcrypt-critical.svg)
![Status](https://img.shields.io/badge/pipeline-Jenkins%20SUCCESS-brightgreen.svg)

---

## ⚙️ Stack principal

- **Backend:** FastAPI (Python 3.10), SQLAlchemy, JWT (`python-jose`), cifrado simétrico con **Fernet** (`cryptography`) y hashing de contraseñas con **bcrypt**.
- **Base de datos:** PostgreSQL.
- **Frontend:** Build con Node + npm y servido con **Nginx** en contenedor.
- **Infraestructura:** Docker y Docker Compose.
- **CI/CD:** Jenkins Pipeline con:
  - Build de imágenes Docker (`api` y `frontend`).
  - Generación automática de `.env` a partir de credenciales de Jenkins.
  - Levantamiento controlado de `db` + `api` en entorno de CI.
  - **Smoke test** de `/usuarios/registro` desde dentro del contenedor `api`.
  - Limpieza automática con `docker compose down`.

## 🛠️ Integración Continua con Jenkins + Docker Compose
Proyecto: Gestor de Contraseñas – CI Seguro

Este documento describe el proceso completo de Integración Continua (CI) implementado para el proyecto Administrador de Contraseñas, incluyendo configuración de Jenkins, manejo seguro de credenciales, construcción de imágenes Docker, levantamiento del stack controlado, generación del archivo .env y pruebas automáticas.

### 📌 1. Arquitectura del CI

El pipeline de Jenkins ejecuta:

Checkout del código

Build de imágenes Docker (API y Frontend)

Ejecución del stack (DB + API)

Generación automática del archivo .env

Smoke Test automático

Limpieza del entorno

El frontend se construye, pero no se levanta en CI para evitar conflictos de puertos y porque no es necesario para las pruebas.

### 🔐 2. Credenciales Configuradas en Jenkins

En:

Manage Jenkins → Credentials

Se crearon los siguientes secretos:

| ID                  | Tipo   | Uso                        |
| ------------------- | ------ | -------------------------- |
| `vault-db-user`     | String | Usuario de PostgreSQL      |
| `vault-db-password` | String | Contraseña de PostgreSQL   |
| `vault-db-name`     | String | Nombre de la base de datos |
| `vault-secret-key`  | String | Llave de JWT               |
| `vault-fernet-key`  | String | Llave Fernet (32 bytes)    |

Estas credenciales se inyectan automáticamente en el archivo .env.

### 📄 3. Jenkinsfile Final

pipeline {
agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {

        stage('Checkout código') {
            steps {
                checkout scm
            }
        }

        stage('Build imágenes Docker') {
            steps {
                sh '''
                echo "===> Construyendo imágenes de api y frontend..."
                docker compose -f ${COMPOSE_FILE} build api frontend
                '''
            }
        }

        stage('Levantar stack (db + api)') {
            steps {
                withCredentials([
                    string(credentialsId: 'vault-db-user',       variable: 'CI_DB_USER'),
                    string(credentialsId: 'vault-db-password',   variable: 'CI_DB_PASSWORD'),
                    string(credentialsId: 'vault-db-name',       variable: 'CI_DB_NAME'),
                    string(credentialsId: 'vault-secret-key',    variable: 'CI_SECRET_KEY'),
                    string(credentialsId: 'vault-fernet-key',    variable: 'CI_FERNET_KEY')
                ]) {

                    sh '''
                      echo "===> Creando archivo .env para CI en Jenkins..."

                      cat > .env <<EOF

        DB_USER=${CI_DB_USER}
        DB_PASSWORD=${CI_DB_PASSWORD}
        DB_NAME=${CI_DB_NAME}
        DB_HOST=db
        DB_PORT=5432
        SECRET_KEY=${CI_SECRET_KEY}
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=60
        FERNET_KEY=${CI_FERNET_KEY}
        EOF

                      echo "===> Levantando servicios db y api (sin frontend en CI)..."
                      docker compose -f ${COMPOSE_FILE} up -d db api

                      echo "===> Esperando a que la API esté lista dentro del contenedor api..."
                      i=1
                      max=15
                      while [ "$i" -le "$max" ]; do
                        if docker compose -f ${COMPOSE_FILE} exec -T api curl -sSf http://localhost:5000/docs > /dev/null 2>&1; then
                          echo "API disponible en intento $i"
                          exit 0
                        fi
                        echo "API no lista aún, reintento $i/$max..."
                        i=$((i+1))
                        sleep 5
                      done

                      echo "La API no respondió a tiempo"
                      exit 1
                    '''
                }
            }
        }

        stage('Smoke test /usuarios/registro') {
            steps {
                sh '''
                echo "===> Ejecutando smoke test de registro de usuario..."

                docker compose -f ${COMPOSE_FILE} exec -T api curl -sSf -X POST \
                  http://localhost:5000/usuarios/registro \
                  -H "accept: application/json" \
                  -H "Content-Type: application/json" \
                  -d '{
                    "nombre": "CI",
                    "apellido": "User",
                    "correo": "ci-user@example.com",
                    "contrasena": "ci1234"
                  }'

                echo "Smoke test OK "
                '''
            }
        }
    }

    post {
        always {
            echo "===> Limpiando: bajando contenedores..."
            sh '''
            docker compose -f ${COMPOSE_FILE} down || true
            '''
        }
        success {
            echo "Pipeline completado correctamente"
        }
        failure {
            echo "Pipeline falló, revisar logs en Jenkins"
        }
    }

}

### ⚙️ 4. Cómo se genera el archivo .env

Jenkins no necesita ningún .env dentro del repositorio.

En su lugar, genera el archivo en tiempo de ejecución:

cat > .env <<EOF
DB_USER=${CI_DB_USER}
DB_PASSWORD=${CI_DB_PASSWORD}
DB_NAME=${CI_DB_NAME}
DB_HOST=db
DB_PORT=5432
SECRET_KEY=${CI_SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
FERNET_KEY=${CI_FERNET_KEY}
EOF

Este archivo:

No se sube al repositorio

Solo existe durante el pipeline

Se elimina al finalizar

### 🚀 5. Levantamiento del Stack en CI

Sólo se levantan los servicios:

    docker compose up -d db api

El frontend no se levanta en CI para evitar conflictos y porque no afecta las pruebas.

### 🔍 6. Healthcheck Interno

El pipeline espera a que la API responda:

    docker compose exec -T api curl -sSf http://localhost:5000/docs

Se reintenta 15 veces cada 5 segundos.

### 🧪 7. Smoke Test Automático

Una vez la API está lista, Jenkins ejecuta el siguiente test:

    curl -X POST http://localhost:5000/usuarios/registro \
    -H "Content-Type: application/json" \
    -d '{"nombre":"CI","apellido":"User","correo":"ci-user@example.com","contrasena":"ci1234"}'

Si responde correctamente → CI aprobado.

### 🧹 8. Limpieza Automática

Siempre se ejecuta:

    docker compose down

Esto garantiza:

Sin contenedores sobrantes

Sin puertos ocupados

Sin estado previo contaminando nuevas pruebas

### 🧰 9. Probar Localmente Antes del Commit

1. Crear .env local

   cp .env.example .env

2. Levantar servicios

   docker compose up -d db api

3. Verificar API

   curl http://localhost:5000/docs

4. Ejecutar smoke test

   curl -X POST http://localhost:5000/usuarios/registro \
   -H "Content-Type: application/json" \
   -d '{"nombre":"Test"}'

### 🔒 10. Checklist de Seguridad Implementado

-Sin secretos en GitHub

-.env generado por Jenkins

-Variables enmascaradas en consola

-Llaves JWT y Fernet seguras

-Pipeline reproducible

-Docker Compose aislado

### 📚 11. Dependencias

-Jenkins Pipeline

-Docker & Docker Compose

-FastAPI

-PostgreSQL

-bcrypt

-PyJWT

-cryptography (Fernet)
