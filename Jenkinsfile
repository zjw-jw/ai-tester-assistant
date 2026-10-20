pipeline {
    agent any
    stages {
        stage('Run Pytest') {
            steps {
                // 切换到测试脚本所在目录
                dir('C:\\Users\\sclodc\\PycharmProjects\\ai-tester-assistant\\storage\\execution\\generated') {
                    // 执行 pytest 并生成 allure 数据
                    bat 'C:\\Users\\sclodc\\PycharmProjects\\ai-tester-assistant\\.venv\\Scripts\\python.exe -m pytest --alluredir=allure-results --clean-alluredir'

                    // 将生成的数据拷贝到 Jenkins 工作空间，避免路径解析问题
                    bat 'xcopy /E /I /Y allure-results C:\\Users\\sclodc\\AppData\\Local\\Jenkins\\.jenkins\\workspace\\WeCom_Test_V2\\allure-results'
                }
            }
        }
    }
    post {
        always {
            // 生成 Allure 报告
            allure commandline: 'allure', includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}