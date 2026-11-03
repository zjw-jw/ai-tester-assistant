pipeline {
    agent any
    stages {
        stage('Run Tests in Docker') {
            steps {
                echo '正在启动测试容器执行 pytest...'
                // 注意：这里假设你的测试脚本在 testing/ 目录下
                // -v 参数把容器内的 allure-results 挂载到 Windows 当前目录
                bat 'docker run --rm -v "%cd%\\allure-results:/app/allure-results" ai-tester-app pytest testing/ --alluredir=/app/allure-results --clean-alluredir'
            }
        }
    }
    post {
        always {
            echo '正在读取测试结果生成 Allure 报告...'
            // 直接读取挂载出来的 allure-results
            allure commandline: 'allure', includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}