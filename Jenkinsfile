pipeline {
    agent any

    environment {
        IMAGE_NAME = "task-tracker-api"
        CONTAINER_NAME = "task-tracker-api"
        APP_PORT = "5000"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Virtual Env') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 app.py --max-line-length=100 || true
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest test_app.py --cov=app --cov-report=xml -v
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                sh '''
                    docker run --rm \
                      -v $(pwd):/usr/src \
                      -w /usr/src \
                      sonarsource/sonar-scanner-cli \
                      -Dsonar.host.url=http://host.docker.internal:9000
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:5000 ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    sleep 5
                    curl -f http://localhost:${APP_PORT}/health
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded - app deployed on port ${APP_PORT}"
        }
        failure {
            echo "Pipeline failed - check console output above"
        }
    }
}
