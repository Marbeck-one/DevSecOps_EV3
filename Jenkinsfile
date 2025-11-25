pipeline {
    agent any

    stages {
        stage('Checkout & Setup') {
            steps {
                echo 'Obteniendo código...'
                // En un entorno real aquí iría el 'git checkout'
                // Simularemos la instalación de dependencias
                sh 'pip install -r app/requirements.txt'
            }
        }

        stage('Análisis Estático (SAST) - IL 3.2') {
            steps {
                echo 'Ejecutando Bandit para buscar vulnerabilidades en código Python...'
                // Bandit busca errores de seguridad comunes en Python
                sh 'bandit -r app/ -f json -o bandit_report.json || true' 
            }
        }

        stage('Revisión de Dependencias - IL 3.3') {
            steps {
                echo 'Verificando seguridad de librerías con Safety...'
                sh 'safety check -r app/requirements.txt --full-report || true'
            }
        }

        stage('Build & Deploy Test') {
            steps {
                echo 'Construyendo contenedor para pruebas...'
                // Reconstruimos el servicio webapp definido en el compose
                sh 'docker-compose up -d --build webapp'
                sleep 10 // Esperar a que levante
            }
        }

        stage('Pruebas Dinámicas (DAST) - OWASP ZAP - IL 3.1') {
            steps {
                echo 'Atacando la aplicación con OWASP ZAP...'
                // Ejecutamos ZAP usando Docker contra nuestra webapp
                sh '''
                docker run --network parcial3_devsecops-net \
                -v $(pwd):/zap/wrk/:rw \
                -t owasp/zap2docker-stable zap-baseline.py \
                -t http://webapp:5000 -r zap_report.html || true
                '''
            }
        }
        
        stage('Generar Documentación - IL 3.4') {
            steps {
                echo 'Generando documentación automática...'
                sh 'pydoc -w app/secure_app.py'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '*.html, *.json', allowEmptyArchive: true
            echo 'Pipeline finalizado. Revisa los reportes generados.'
        }
    }
}
