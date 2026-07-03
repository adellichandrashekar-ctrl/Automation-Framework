pipeline{
    agent {
        node {
            label '' // Empty label tells jenkins to run on ANY avilable node
        }
    }

    triggers {
        cron('H 0 * * *')
    }

    environment {
        PYTHON = '"C:\\Users\\AdelliChandrashekar\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe"'
    }
    stages {
        stage('Checkout & Verify') {
            steps {
                echo "Code successfully pulled from GitHub!"
                bat 'dir'
            }
        }
        stage('Setup Environment') {
            steps {
                echo "Setting up Python Virtual Environment..."
                bat """
                    $(PYTHON) -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install -r requirements.txt
                """
            }

        }
        stage('Run API Tests') {
            steps {
                echo "Running API Test Suite..."
                bat """
                    call venv\\Scripts\\activate.bat
                    pytest -m api -v --alluredir=allure-results
                """
            }
        }
        stage('Run UI Tests') {
            steps {
                echo "Running UI Test Suite..."
                bat """
                    call venv\\Scripts\\activate.bat
                    pytest -m ui -v --alluredir=allure-results
                """
            }
        }
        stage('Run DB Tests') {
            steps {
                echo "Running DB Test Suite..."
                bat """
                    call venv\\Scripts\\activate.bat
                    pytest -m db -v --alluredir=allure-results
                """
            }
        }
    }
    post {
        always {
            echo "Pipeline finished! Generating Allure Report..."
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPlicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
        }
        success {
            echo "All TESTS PASSED! Ready for deployment"
        }
        failure {
            echo "TESTS FAILED! Sending alert to development team"
            mail to: 'adelli_chandrashekar@epam.com',
                 subject: "Pipeline Failed: ${env.JOB_NAME} Build #${env.BUILD_NUMBER}",
                 body: "The nightly automation suite has failed. Please check the Allure Report!"
        }
    }
}