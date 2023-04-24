pipeline {
    agent {
        docker {
            image 'selenium/standalone-chrome'
            args '-u root'
        }
    }
    parameters {
        string(name: 'ENV', defaultValue: 'Test', description: '')
        string(name: 'user', defaultValue: '1', description: '')
    }
    stages {
        stage('Clone the repo') {
            steps {
                // git 'https://github.com/chaitanyarajugithub/scale-pharma.git'
                git branch: 'main', url: 'git@github.com:chaitanyarajugithub/scale-pharma.git'
                // sh "git checkout loadtest"
            }
        }
        stage('Install requirements') {
            steps {
                sh 'apt-get update'
                sh 'apt-get install -y python3-virtualenv'
                sh 'apt-get install -y python3-pip'
                sh 'apt-get install -y postgresql'
                sh 'apt-get install libpq-dev'
                // sh 'apt-get install -y python3'
                // sh 'python3 -m pip'
                // sh 'apt-get install python3.8-venv'
                sh 'python3 -m pip'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run the Cypress scenario tests') {
            steps {
                sh """
                python3 test_apc.py
                """
            }
        }
    }
}