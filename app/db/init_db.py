from app.config.database import Base, engine
from app.models import user, learning_path, stage, task, user_task_progress, achievement, task_resource

# 创建所有表
Base.metadata.create_all(bind=engine)
print("数据库表创建成功！")
