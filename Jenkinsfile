pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "vault-ci-${BUILD_NUMBER}"
    }

    stages {
        stage('Limpiar') {
            steps {
                sh '''
                echo "===> Desactivando override para CI..."
                [ -f docker-compose.override.yml ] && mv docker-compose.override.yml docker-compose.override.yml.bak || true
                
                echo "===> Limpiando contenedores previos..."
                docker compose down -v --remove-orphans 2>/dev/null || true
                sleep 2
                '''
            }
        }

        stage('Checkout código') {
            steps {
                checkout scm
            }
        }

        stage('Build imágenes') {
            steps {
                sh '''
                echo "===> Construyendo imágenes..."
                docker compose build api db
                '''
            }
        }

        stage('Levantar stack (db + api)') {
            steps {
                withCredentials([
                    string(credentialsId: 'vault-db-user', variable: 'CI_DB_USER'),
                    string(credentialsId: 'vault-db-password', variable: 'CI_DB_PASSWORD'),
                    string(credentialsId: 'vault-db-name', variable: 'CI_DB_NAME'),
                    string(credentialsId: 'vault-secret-key', variable: 'CI_SECRET_KEY'),
                    string(credentialsId: 'vault-fernet-key', variable: 'CI_FERNET_KEY')
                ]) {
                    sh '''
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

                    echo "===> Levantando servicios (SIN puertos expuestos)..."
                    docker compose up -d db api

                    echo "===> Esperando a que DB esté ready..."
                    sleep 5
                    '''
                }
            }
        }

        stage('Smoke test /usuarios/registro') {
            steps {
                sh '''
                echo "===> Ejecutando smoke test..."

                EMAIL_CI="ci-user-${BUILD_NUMBER}@example.com"
                echo "Email: ${EMAIL_CI}"

                for i in {1..15}; do
                    if docker compose exec -T api curl -sSf http://localhost:5000/docs > /dev/null 2>&1; then
                        echo "✓ API disponible en intento $i"
                        
                        docker compose exec -T api \
                          curl -X POST http://localhost:5000/usuarios/registro \
                          -H "Content-Type: application/json" \
                          -d "{\\"nombre\\":\\"CI\\",\\"apellido\\":\\"User\\",\\"correo\\":\\"${EMAIL_CI}\\",\\"contrasena\\":\\"ci1234\\"}"
                        
                        echo ""
                        echo "✓ Smoke test completado exitosamente"
                        exit 0
                    fi
                    echo "Intento $i/15 - esperando a API..."
                    sleep 2
                done

                echo "❌ API no respondió a tiempo"
                docker compose logs api || true
                exit 1
                '''
            }
        }
    }

    post {
        always {
            sh '''
            echo "===> Limpiando contenedores..."
            docker compose down -v --remove-orphans 2>/dev/null || true
            
            echo "===> Restaurando override para desarrollo..."
            [ -f docker-compose.override.yml.bak ] && mv docker-compose.override.yml.bak docker-compose.override.yml || true
            '''
        }
        success {
            echo "✓ Pipeline completado correctamente"
        }
        failure {
            echo "❌ Pipeline falló - revisar logs"
        }
    }
}
