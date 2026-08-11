pipeline {
  agent any

  environment {
    PYTHONUNBUFFERED = '1'
  }

  stages {
    stage('Checkout') {
      steps {
        echo 'Checking out repository'
      }
    }

    stage('Setup Python') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          python -m playwright install --with-deps chromium
        '''
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          . .venv/bin/activate
          mkdir -p reports
          python -m pytest -q test/test.py --junitxml=reports/pytest-results.xml
        '''
      }
    }
  }

  post {
    always {
      junit 'reports/*.xml'
      archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
    }
  }
}
