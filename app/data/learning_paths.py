# 3条核心学习路径的数据定义

learning_paths_data = [
    {
        "name": "快速入门版",
        "duration": "6个月",
        "description": "聚焦API调用→Prompt工程→轻量应用开发，适合想快速就业的转行人群",
        "target_audience": "0基础转行，想快速就业的人群",
        "structure": "API调用→Prompt工程→轻量应用开发",
        "stages": [
            {
                "name": "基础搭建",
                "description": "掌握Python基础和开发环境搭建",
                "order": 1,
                "tasks": [
                    # 第1周任务
                    {"title": "学习Python基础语法", "description": "变量、数据类型、控制流", "duration": 90, "difficulty": "easy", "week": 1, "day": 1},
                    {"title": "练习Python函数", "description": "定义和调用函数", "duration": 60, "difficulty": "easy", "week": 1, "day": 2},
                    {"title": "学习Python模块", "description": "使用标准库和第三方库", "duration": 90, "difficulty": "easy", "week": 1, "day": 3},
                    {"title": "搭建开发环境", "description": "安装Python和IDE", "duration": 60, "difficulty": "easy", "week": 1, "day": 4},
                    {"title": "学习Git基础", "description": "版本控制入门", "duration": 90, "difficulty": "easy", "week": 1, "day": 5},
                    {"title": "周末实战：创建GitHub仓库", "description": "创建并推送第一个项目", "duration": 120, "difficulty": "medium", "week": 1, "day": 6, "is_weekend": True},
                ]
            },
            {
                "name": "核心技能",
                "description": "掌握API调用和Prompt工程",
                "order": 2,
                "tasks": [
                    # 示例任务，实际会有更多
                    {"title": "学习HTTP请求", "description": "使用requests库调用API", "duration": 90, "difficulty": "medium", "week": 2, "day": 1},
                    {"title": "注册OpenAI账号", "description": "获取API Key", "duration": 30, "difficulty": "easy", "week": 2, "day": 2},
                    {"title": "调用OpenAI API", "description": "实现简单的文本生成", "duration": 120, "difficulty": "medium", "week": 2, "day": 3},
                ]
            },
            {
                "name": "项目实战",
                "description": "开发轻量应用",
                "order": 3,
                "tasks": [
                    # 示例任务，实际会有更多
                    {"title": "开发对话机器人", "description": "使用Gradio封装API调用", "duration": 180, "difficulty": "medium", "week": 4, "day": 1},
                    {"title": "实现Prompt工程优化", "description": "学习提示词设计技巧", "duration": 120, "difficulty": "medium", "week": 4, "day": 2},
                ]
            }
        ]
    },
    {
        "name": "全面进阶版",
        "duration": "1年",
        "description": "覆盖基础→进阶→实战→部署全流程，含RAG/Agent/微调技术",
        "target_audience": "目标大模型应用开发师的用户",
        "structure": "基础→进阶→实战→部署",
        "stages": [
            {
                "name": "基础搭建",
                "description": "掌握Python进阶和开发环境",
                "order": 1,
                "tasks": [
                    # 第1周任务
                    {"title": "学习装饰器+闭包", "description": "Python高级特性", "duration": 90, "difficulty": "medium", "week": 1, "day": 1},
                    {"title": "练习函数式编程", "description": "lambda/map/filter", "duration": 60, "difficulty": "medium", "week": 1, "day": 2},
                    {"title": "用AI工具复盘代码", "description": "使用AI优化代码", "duration": 30, "difficulty": "easy", "week": 1, "day": 3},
                    {"title": "搭建Python3.10+Gradio/FastAPI环境", "description": "开发环境配置", "duration": 60, "difficulty": "medium", "week": 1, "day": 4},
                    {"title": "学习HTTP请求与JSON解析", "description": "网络请求基础", "duration": 60, "difficulty": "medium", "week": 1, "day": 5},
                    {"title": "周末实战：用装饰器写接口请求耗时统计工具", "description": "实战项目", "duration": 120, "difficulty": "medium", "week": 1, "day": 6, "is_weekend": True},
                ]
            },
            {
                "name": "核心技能",
                "description": "掌握大模型API调用和Prompt工程",
                "order": 2,
                "tasks": [
                    # 示例任务，实际会有更多
                    {"title": "注册OpenAI/通义千问平台", "description": "获取API Key", "duration": 30, "difficulty": "easy", "week": 4, "day": 1},
                    {"title": "学习API参数调优", "description": "temperature/top_p等参数", "duration": 60, "difficulty": "medium", "week": 4, "day": 2},
                    {"title": "实现多轮对话代码", "description": "保持对话上下文", "duration": 90, "difficulty": "medium", "week": 4, "day": 3},
                    {"title": "周末实战：用Gradio封装对话机器人Web界面", "description": "实战项目", "duration": 180, "difficulty": "medium", "week": 4, "day": 6, "is_weekend": True, "is_milestone": True},
                ]
            },
            {
                "name": "项目实战",
                "description": "开发RAG和Agent应用",
                "order": 3,
                "tasks": [
                    # 示例任务，实际会有更多
                    {"title": "学习RAG基础", "description": "检索增强生成", "duration": 120, "difficulty": "hard", "week": 12, "day": 1},
                    {"title": "实现基础RAG系统", "description": "文档检索和生成", "duration": 180, "difficulty": "hard", "week": 12, "day": 2},
                ]
            },
            {
                "name": "深化进阶",
                "description": "学习模型微调和部署",
                "order": 4,
                "tasks": [
                    # 示例任务，实际会有更多
                    {"title": "学习模型微调基础", "description": "参数高效微调方法", "duration": 120, "difficulty": "hard", "week": 24, "day": 1},
                    {"title": "部署模型应用", "description": "将应用部署到服务器", "duration": 180, "difficulty": "hard", "week": 24, "day": 2},
                ]
            }
        ]
    },
    {
        "name": "垂直深耕版",
        "duration": "1.5年",
        "description": "在全面进阶基础上，增加行业垂类应用和开源协作",
        "target_audience": "想形成技术壁垒的用户",
        "structure": "基础→进阶→实战→部署→行业垂类→开源协作",
        "stages": [
            {
                "name": "基础搭建",
                "description": "掌握Python进阶和开发环境",
                "order": 1,
                "tasks": [
                    # 与全面进阶版类似，实际会有更多任务
                ]
            },
            {
                "name": "核心技能",
                "description": "掌握大模型API调用和Prompt工程",
                "order": 2,
                "tasks": [
                    # 与全面进阶版类似，实际会有更多任务
                ]
            },
            {
                "name": "项目实战",
                "description": "开发RAG和Agent应用",
                "order": 3,
                "tasks": [
                    # 与全面进阶版类似，实际会有更多任务
                ]
            },
            {
                "name": "深化进阶",
                "description": "学习模型微调和部署",
                "order": 4,
                "tasks": [
                    # 与全面进阶版类似，实际会有更多任务
                ]
            },
            {
                "name": "行业垂类应用",
                "description": "开发医疗/金融/教育等行业应用",
                "order": 5,
                "tasks": [
                    # 示例任务，实际会有更多
                    {"title": "学习医疗行业大模型应用", "description": "了解医疗领域需求", "duration": 120, "difficulty": "hard", "week": 36, "day": 1},
                    {"title": "开发医疗问答系统", "description": "实现医疗知识问答", "duration": 240, "difficulty": "hard", "week": 36, "day": 2},
                ]
            },
            {
                "name": "开源协作",
                "description": "参与开源项目，提升技术影响力",
                "order": 6,
                "tasks": [
                    # 示例任务，实际会有更多
                    {"title": "学习开源项目贡献流程", "description": "了解GitHub协作规范", "duration": 90, "difficulty": "medium", "week": 48, "day": 1},
                    {"title": "贡献第一个开源PR", "description": "参与开源项目开发", "duration": 180, "difficulty": "hard", "week": 48, "day": 2},
                ]
            }
        ]
    }
]
