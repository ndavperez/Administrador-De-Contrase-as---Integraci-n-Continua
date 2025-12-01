pipeline {
    agent any

    environment {
        COMPOSE_BASE = 'docker-compose.yml'
        COMPOSE_CI   = 'docker-compose.ci.yml'
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
                docker compose -f ${COMPOSE_BASE} -f ${COMPOSE_CI} build api frontend
                '''
            }
        }

        stage('Levantar stack (db + api)') {
            steps {
                withCredentials([
                    string(credentialsId: 'vault-db-user',     variable: 'CI_DB_USER'),
                    string(credentialsId: 'vault-db-password', variable: 'CI_DB_PASSWORD'),
                    string(credentialsId: 'vault-db-name',     variable: 'CI_DB_NAME'),
                    string(credentialsId: 'vault-secret-key',  variable: 'CI_SECRET_KEY'),
                    string(credentialsId: 'vault-fernet-key',  variable: 'CI_FERNET_KEY')
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
UVICORN_HOST=0.0.0.0
UVICORN_PORT=5000
ENVIRONMENT=ci
API_PORT=5500
EOF

                    echo "===> Levantando servicios db y api (sin frontend en CI)..."
                    docker compose -f ${COMPOSE_BASE} -f ${COMPOSE_CI} up -d db api

                    echo "===> Esperando a que la API esté lista dentro del contenedor api (http://localhost:5000/docs)..."

                    i=1
                    max=15
                    while [ "$i" -le "$max" ]; do
                      if docker compose -f ${COMPOSE_BASE} -f ${COMPOSE_CI} exec -T api curl -sSf http://localhost:5000/docs > /dev/null 2>&1; then
                        echo "API disponible en intento $i"
                        exit 0
                      fi
                      echo "API no lista aún, reintento $i/$max..."
                      i=$((i+1))
                      sleep 5
                    done

                    echo "La API no respondió a tiempo"
                    docker compose -f ${COMPOSE_BASE} -f ${COMPOSE_CI} logs api || true
                    exit 1
                    '''
                }
            }
        }

        stage('Smoke test /usuarios/registro') {
            steps {
                sh '''
                echo "===> Ejecutando smoke test de registro de usuario (desde el contenedor api)..."

                EMAIL_CI="ci-user-${BUILD_NUMBER}@example.com"
                echo "Usando correo: ${EMAIL_CI}"

                docker compose -f ${COMPOSE_BASE} -f ${COMPOSE_CI} exec -T api curl -sSf -X POST \
                  http://localhost:5000/usuarios/registro \
                  -H "accept: application/json" \
                  -H "Content-Type: application/json" \
                  -d "{\"nombre\":\"CI\",\"apellido\":\"User\",\"correo\":\"${EMAIL_CI}\",\"contrasena\":\"ci1234\"}"

                echo "Smoke test OK"
                '''
            }
        }
    }

    post {
        always {
            echo "===> Limpiando: bajando contenedores..."
            sh '''
            docker compose -f ${COMPOSE_BASE} -f ${COMPOSE_CI} down || true
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
