pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout código') {
            steps {
                // Usa el repositorio configurado en el  pipeline
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

        stage('Levantar stack (db + api + frontend)') {
            steps {
                sh '''
                echo "===> Levantando servicios db, api y frontend..."
                docker compose -f ${COMPOSE_FILE} up -d db api frontend

                echo "===> Esperando a que la API esté lista en http://api:5000/docs ..."
                # Jenkins corre dentro de la misma red docker, así que usamos el hostname del servicio: api
                for i in {1..15}; do
                  if curl -sSf http://api:5000/docs > /dev/null; then
                    echo "API disponible "
                    exit 0
                  fi
                  echo "API no lista aún, reintento $i/15..."
                  sleep 5
                done

                echo "La API no respondió a tiempo"
                exit 1
                '''
            }
        }

        stage('Smoke test /usuarios/registro') {
            steps {
                sh '''
                echo "===> Ejecutando smoke test de registro de usuario..."

                # Llamamos a la API por nombre de servicio dentro de la red docker
                curl -sSf -X POST \
                  'http://api:5000/usuarios/registro' \
                  -H 'accept: application/json' \
                  -H 'Content-Type: application/json' \
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

        // Opcional: si luego agregas tests automáticos (pytest, npm test, etc.)
        // los puedes poner en un stage aparte.
        // stage('Tests backend/frontend') { ... }
    }

    post {
        always {
            echo "===> Limpiando: bajando contenedores..."
            sh '''
            docker compose -f ${COMPOSE_FILE} down
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
