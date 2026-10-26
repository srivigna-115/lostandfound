pipeline {
    agent any
    environment {
        IMAGE_NAME = 'srivigna115/campus-lost-found'
        DOCKER_CREDENTIALS = 'dockerhub-creds'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% -t %IMAGE_NAME%:latest .'
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS}",
                    usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                        @echo off
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                        docker push %IMAGE_NAME%:%BUILD_NUMBER%
                        docker push %IMAGE_NAME%:latest
                        docker logout
                    '''
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    kubectl set image deployment/campus-lost-found campus-lost-found=%IMAGE_NAME%:%BUILD_NUMBER%
                    kubectl rollout status deployment/campus-lost-found --timeout=120s
                '''
            }
        }
    }
    post { always { echo 'Check the console output for pipeline results.' } }
}
