from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.config.database import get_db
from app.models import Task as TaskModel, UserTaskProgress as UserTaskProgressModel, User as UserModel
from app.models.schemas import Task, UserTaskProgress, UserTaskProgressCreate
from app.routes.users import get_current_user

router = APIRouter()

# 获取所有任务
@router.get("/", response_model=list[Task])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).offset(skip).limit(limit).all()
    return tasks

# 获取单个任务
@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# 获取用户的任务进度
@router.get("/user/{user_id}", response_model=list[UserTaskProgress])
def get_user_tasks(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    progress = db.query(UserTaskProgressModel).filter(UserTaskProgressModel.user_id == user_id).offset(skip).limit(limit).all()
    return progress

# 获取当前用户的任务进度
@router.get("/me/progress", response_model=list[UserTaskProgress])
def get_my_tasks_progress(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    progress = db.query(UserTaskProgressModel).filter(UserTaskProgressModel.user_id == current_user.id).all()
    return progress

# 获取当前用户的今日任务
@router.get("/me/today")
def get_today_tasks(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    # 简化实现，实际应该根据当前日期计算周数和天数
    # 这里假设当前是第1周的第1天
    week = 1
    day = 1
    
    # 获取当前用户学习路径的任务
    # 简化实现，实际应该根据用户选择的学习路径获取任务
    tasks = db.query(TaskModel).filter(TaskModel.week == week, TaskModel.day == day).all()
    
    # 获取用户的任务进度
    task_ids = [task.id for task in tasks]
    progress = db.query(UserTaskProgressModel).filter(
        UserTaskProgressModel.user_id == current_user.id,
        UserTaskProgressModel.task_id.in_(task_ids)
    ).all()
    
    # 组合任务和进度信息
    result = []
    for task in tasks:
        task_progress = next((p for p in progress if p.task_id == task.id), None)
        result.append({
            "task": task,
            "is_completed": task_progress.is_completed if task_progress else False,
            "completed_at": task_progress.completed_at if task_progress else None
        })
    
    return result

# 获取当前用户的今日进步清单
@router.get("/me/today-achievements")
def get_today_achievements(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    # 获取今天完成的任务
    today = datetime.now().date()
    completed_tasks = db.query(UserTaskProgressModel).join(TaskModel).filter(
        UserTaskProgressModel.user_id == current_user.id,
        UserTaskProgressModel.is_completed == True,
        UserTaskProgressModel.completed_at >= datetime(today.year, today.month, today.day)
    ).all()
    
    # 生成今日进步清单
    achievements = []
    for progress in completed_tasks:
        achievements.append(f"✅ 完成任务：{progress.task.title}")
    
    return {
        "today": today.strftime("%Y-%m-%d"),
        "achievements": achievements,
        "total_completed": len(achievements)
    }

# 打卡完成任务
@router.post("/{task_id}/complete", response_model=UserTaskProgress)
def complete_task(task_id: int, actual_duration: int = None, notes: str = None, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    # 检查任务是否存在
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 查找或创建用户任务进度
    progress = db.query(UserTaskProgressModel).filter(
        UserTaskProgressModel.user_id == current_user.id,
        UserTaskProgressModel.task_id == task_id
    ).first()
    
    if progress:
        # 更新现有进度
        progress.is_completed = True
        progress.completed_at = datetime.now()
        if actual_duration:
            progress.actual_duration = actual_duration
        if notes:
            progress.notes = notes
    else:
        # 创建新进度
        progress = UserTaskProgressModel(
            user_id=current_user.id,
            task_id=task_id,
            is_completed=True,
            completed_at=datetime.now(),
            actual_duration=actual_duration,
            notes=notes
        )
        db.add(progress)
    
    db.commit()
    db.refresh(progress)
    return progress

# 取消任务完成状态
@router.post("/{task_id}/uncomplete", response_model=UserTaskProgress)
def uncomplete_task(task_id: int, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    # 查找用户任务进度
    progress = db.query(UserTaskProgressModel).filter(
        UserTaskProgressModel.user_id == current_user.id,
        UserTaskProgressModel.task_id == task_id
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="Task progress not found")
    
    # 更新进度
    progress.is_completed = False
    progress.completed_at = None
    
    db.commit()
    db.refresh(progress)
    return progress

# 更新任务进度
@router.put("/{task_id}/progress", response_model=UserTaskProgress)
def update_task_progress(task_id: int, progress_data: UserTaskProgressCreate, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    # 查找或创建用户任务进度
    progress = db.query(UserTaskProgressModel).filter(
        UserTaskProgressModel.user_id == current_user.id,
        UserTaskProgressModel.task_id == task_id
    ).first()
    
    if progress:
        # 更新现有进度
        for key, value in progress_data.dict().items():
            setattr(progress, key, value)
        
        # 如果标记为完成但没有完成时间，则设置完成时间
        if progress.is_completed and not progress.completed_at:
            progress.completed_at = datetime.now()
        # 如果取消完成，则清除完成时间
        elif not progress.is_completed:
            progress.completed_at = None
    else:
        # 创建新进度
        progress = UserTaskProgressModel(
            user_id=current_user.id,
            task_id=task_id,
            **progress_data.dict()
        )
        
        # 如果标记为完成，设置完成时间
        if progress.is_completed:
            progress.completed_at = datetime.now()
        
        db.add(progress)
    
    db.commit()
    db.refresh(progress)
    return progress
