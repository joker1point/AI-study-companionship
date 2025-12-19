from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.config.database import get_db
from app.models import User as UserModel, Task as TaskModel, UserTaskProgress as UserTaskProgressModel, Stage as StageModel, LearningPath as LearningPathModel
from app.routes.users import get_current_user

router = APIRouter()

# 获取用户学习进度概览
@router.get("/{user_id}")
def get_user_progress(user_id: int, db: Session = Depends(get_db)):
    # 检查用户是否存在
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 简化实现，实际应该根据用户选择的学习路径计算
    # 这里假设用户选择了全面进阶版路径
    learning_path = db.query(LearningPathModel).filter(LearningPathModel.name == "全面进阶版").first()
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    # 获取所有阶段
    stages = db.query(StageModel).filter(StageModel.learning_path_id == learning_path.id).all()
    stage_ids = [stage.id for stage in stages]
    
    # 获取所有任务
    total_tasks = db.query(TaskModel).filter(TaskModel.stage_id.in_(stage_ids)).count()
    
    # 获取已完成任务
    completed_tasks = db.query(UserTaskProgressModel).filter(
        UserTaskProgressModel.user_id == user_id,
        UserTaskProgressModel.is_completed == True
    ).count()
    
    # 计算阶段完成率
    stage_completion_rates = []
    for stage in stages:
        stage_tasks = db.query(TaskModel).filter(TaskModel.stage_id == stage.id).count()
        if stage_tasks == 0:
            stage_completion_rates.append({
                "stage_name": stage.name,
                "completion_rate": 0
            })
            continue
        
        completed_stage_tasks = db.query(UserTaskProgressModel).join(TaskModel).filter(
            UserTaskProgressModel.user_id == user_id,
            UserTaskProgressModel.is_completed == True,
            TaskModel.stage_id == stage.id
        ).count()
        
        stage_completion_rates.append({
            "stage_name": stage.name,
            "completion_rate": completed_stage_tasks / stage_tasks
        })
    
    # 计算累计学习时长
    total_duration = db.query(func.sum(UserTaskProgressModel.actual_duration)).filter(
        UserTaskProgressModel.user_id == user_id,
        UserTaskProgressModel.is_completed == True
    ).scalar() or 0
    total_learning_hours = round(total_duration / 60, 2)
    
    # 简化实现，实际应该根据任务完成情况计算已掌握技能数
    acquired_skills = completed_tasks // 5  # 每完成5个任务，掌握1个技能
    
    return {
        "user_id": user_id,
        "learning_path": learning_path.name,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "overall_completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
        "stage_completion_rates": stage_completion_rates,
        "total_learning_hours": total_learning_hours,
        "acquired_skills": acquired_skills
    }

# 获取当前用户的学习进度
@router.get("/me")
def get_my_progress(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_progress(current_user.id, db)

# 获取学习周报
@router.get("/{user_id}/weekly-report")
def get_weekly_report(user_id: int, db: Session = Depends(get_db)):
    # 检查用户是否存在
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 计算本周的开始和结束时间
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # 获取本周完成的任务
    completed_tasks = db.query(UserTaskProgressModel).join(TaskModel).filter(
        UserTaskProgressModel.user_id == user_id,
        UserTaskProgressModel.is_completed == True,
        UserTaskProgressModel.completed_at >= start_of_week,
        UserTaskProgressModel.completed_at <= end_of_week
    ).all()
    
    # 获取剩余任务（简化实现）
    # 实际应该根据用户当前进度计算下一阶段的剩余任务
    remaining_tasks = 8
    
    # 计算本周学习时长
    total_duration = sum(progress.actual_duration for progress in completed_tasks if progress.actual_duration)
    total_hours = round(total_duration / 60, 2)
    
    # 简化实现，实际应该根据任务类型计算解锁的技能
    unlocked_skills = len(completed_tasks) // 4  # 每完成4个任务，解锁1个技能
    
    return {
        "user_id": user_id,
        "week": f"{start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')}",
        "completed_tasks": len(completed_tasks),
        "unlocked_skills": unlocked_skills,
        "remaining_tasks": remaining_tasks,
        "total_hours": total_hours,
        "completed_task_details": [{
            "task_title": progress.task.title,
            "completed_at": progress.completed_at.strftime("%Y-%m-%d %H:%M:%S")
        } for progress in completed_tasks]
    }

# 获取当前用户的学习周报
@router.get("/me/weekly-report")
def get_my_weekly_report(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_weekly_report(current_user.id, db)

# 获取成就进度
@router.get("/{user_id}/achievements")
def get_achievements(user_id: int, db: Session = Depends(get_db)):
    # 检查用户是否存在
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 获取已完成的里程碑任务
    milestone_tasks = db.query(UserTaskProgressModel).join(TaskModel).filter(
        UserTaskProgressModel.user_id == user_id,
        UserTaskProgressModel.is_completed == True,
        TaskModel.is_milestone == True
    ).all()
    
    # 计算连续打卡天数（简化实现）
    # 实际应该根据连续完成任务的天数计算
    consecutive_days = 5
    
    # 简化实现，实际应该根据成就体系规则生成
    achievements = [
        {
            "name": "API调用能手",
            "description": "完成大模型API调用相关任务",
            "is_achieved": len(milestone_tasks) >= 1
        },
        {
            "name": "RAG实战达人",
            "description": "完成RAG系统开发相关任务",
            "is_achieved": len(milestone_tasks) >= 2
        },
        {
            "name": "坚持奖励",
            "description": "连续打卡30天",
            "is_achieved": consecutive_days >= 30
        }
    ]
    
    return {
        "user_id": user_id,
        "consecutive_days": consecutive_days,
        "milestone_tasks_completed": len(milestone_tasks),
        "achievements": achievements
    }

# 获取当前用户的成就进度
@router.get("/me/achievements")
def get_my_achievements(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_achievements(current_user.id, db)
