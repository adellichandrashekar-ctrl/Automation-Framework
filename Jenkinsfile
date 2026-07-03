pipeline{
    agent any

    triggers {
        cron('H 0 * * *')
    }

    environment {
        PYTHON = 'C:\\Users\\AdelliChandrashekar\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe'
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
                    %PYTHON% -m venv venv
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                """
            }

        }
        stage('Run API Tests') {
            steps {
                echo "Running API Test Suite..."
                bat """
                    venv\\Scripts\\python.exe -m pytest -m api -v --alluredir=allure-results
                """
            }
        }
        stage('Run UI Tests') {
            steps {
                echo "Running UI Test Suite..."
                bat """
                    venv\\Scripts\\python.exe -m pytest -m ui -v --alluredir=allure-results
                """
            }
        }
        stage('Run DB Tests') {
            steps {
                echo "Running DB Test Suite..."
                bat """
                    venv\\Scripts\\python.exe -m pytest -m db -v --alluredir=allure-results
                """
            }
        }
    }
    post {
        always {
            echo "Pipeline finished! Generating Allure Report..."
            allure([
                includeProperties: false,
                jdk: 'MyJDK',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
        }
        success {
            echo "All TESTS PASSED! Ready for deployment"
        }
        failure {
            echo "TESTS FAILED! Please Visit the Jenkins Pipeline Latest Build For More Information"
            // mail to: 'adelli_chandrashekar@epam.com',
            //      subject: "Pipeline Failed: ${env.JOB_NAME} Build #${env.BUILD_NUMBER}",
            //      body: "The nightly automation suite has failed. Please check the Allure Report!"
        }
    }
}