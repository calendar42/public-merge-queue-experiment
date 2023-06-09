@Library('jenkins-shared-libraries') _

pipeline {
	agent {
		node {
			label 'ubuntu-1804-fff'
		}
	}
	stages {
        stage('Prepare') {
            when {
                anyOf {
                    branch 'master'
                    branch 'main'
                    branch 'gh-readonly-queue/**'
                    changeRequest target: 'master'
                    changeRequest target: 'main'
                }
            }
            stages {
                stage('Install python') {
                    steps {
                        sh '''hostname; printenv'''

                        script {
                            if (fileExists('Pipfile.lock')) {
                                env.PYTHON_VERSION = sh(returnStdout: true, script: 'jq -r "._meta.requires.python_version" Pipfile.lock').trim()
                                sh "if [ ! -e $HOME/.pyenv/versions/${PYTHON_VERSION} ]; then $HOME/.pyenv/bin/pyenv install ${PYTHON_VERSION}; fi"
                                sh "$HOME/.pyenv/bin/pyenv local ${PYTHON_VERSION}"
                                sh "source ~/jenkins.env && pip install -U pip && pip install pipenv && pyenv rehash"
                                sh "pipenv sync -d"
                                sh 'pipenv run pip install -U pip setuptools'
                            } else {
                                error("Pipfile.lock doesn't exist in the root directory of the repository")
                            }
                        }
                    }
                }
            }
        }
        stage('Python') {
            when {
                anyOf {
                    branch 'master'
                    branch 'main'
                    branch 'gh-readonly-queue/**'
                    changeRequest target: 'master'
                    changeRequest target: 'main'
                }
            }
            stages {
                stage('Prepare') {
                    steps {
                        script {
                            sh '''pipenv run python setup.py develop'''
                        }
                    }
                }
                stage('Tests') {
                    steps {
                        sh '''pipenv run pytest ./merge_queue_experiment/tests/test_merge_queue_experiment.py'''
                    }
                }
            }
        }
        stage('Complete merge queue') {
            when {
                anyOf {
                    branch 'gh-readonly-queue/**'
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'c42-bot token', usernameVariable: 'username', passwordVariable: 'password')]){
                    sh '''
                    curl \
                    -H "Accept: application/json" \
                    -H "Authorization: token ${password}" \
                    -X POST \
                    --data '{"state": "success", "target_url": "'${RUN_DISPLAY_URL}'", "context": "continuous-integration/jenkins/pr-merge", "description": "success"}' \
                    https://api.github.com/repos/calendar42/public-merge-queue-experiment/statuses/${GIT_COMMIT}
                    '''
                }
            }
        }
    }
}
