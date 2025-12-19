from sqlalchemy.orm import Session
from app.config.database import engine, SessionLocal
from app.models import LearningPath, Stage, Task
from app.data.learning_paths import learning_paths_data

# 创建数据库会话
db = SessionLocal()

try:
    # 清空现有数据
    db.query(Task).delete()
    db.query(Stage).delete()
    db.query(LearningPath).delete()
    db.commit()
    
    # 导入学习路径数据
    for path_data in learning_paths_data:
        # 创建学习路径
        path = LearningPath(
            name=path_data["name"],
            duration=path_data["duration"],
            description=path_data["description"],
            target_audience=path_data["target_audience"],
            structure=path_data["structure"]
        )
        db.add(path)
        db.commit()
        db.refresh(path)
        
        # 创建阶段
        for stage_data in path_data["stages"]:
            stage = Stage(
                name=stage_data["name"],
                description=stage_data["description"],
                order=stage_data["order"],
                learning_path_id=path.id
            )
            db.add(stage)
            db.commit()
            db.refresh(stage)
            
            # 创建任务
            for task_data in stage_data["tasks"]:
                task = Task(
                    title=task_data["title"],
                    description=task_data["description"],
                    duration=task_data["duration"],
                    difficulty=task_data["difficulty"],
                    stage_id=stage.id,
                    week=task_data["week"],
                    day=task_data["day"],
                    is_weekend=task_data.get("is_weekend", False),
                    is_milestone=task_data.get("is_milestone", False)
                )
                db.add(task)
        
    db.commit()
    print("数据导入成功！")
except Exception as e:
    db.rollback()
    print(f"数据导入失败：{e}")
finally:
    db.close()
