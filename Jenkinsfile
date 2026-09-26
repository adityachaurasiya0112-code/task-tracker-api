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
