from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models import LearningPath as LearningPathModel, Stage as StageModel, Task as TaskModel
from app.models.schemas import LearningPath, LearningPathCreate, Stage, Task

router = APIRouter()

# 获取所有学习路径
@router.get("/", response_model=list[LearningPath])
def get_learning_paths(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    paths = db.query(LearningPathModel).offset(skip).limit(limit).all()
    return paths

# 获取单个学习路径
@router.get("/{path_id}", response_model=LearningPath)
def get_learning_path(path_id: int, db: Session = Depends(get_db)):
    path = db.query(LearningPathModel).filter(LearningPathModel.id == path_id).first()
    if path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")
    return path

# 创建学习路径
@router.post("/", response_model=LearningPath, status_code=status.HTTP_201_CREATED)
def create_learning_path(path: LearningPathCreate, db: Session = Depends(get_db)):
    # 检查名称是否已存在
    existing_path = db.query(LearningPathModel).filter(LearningPathModel.name == path.name).first()
    if existing_path:
        raise HTTPException(status_code=400, detail="Learning path name already exists")
    
    db_path = LearningPathModel(**path.dict())
    db.add(db_path)
    db.commit()
    db.refresh(db_path)
    return db_path

# 更新学习路径
@router.put("/{path_id}", response_model=LearningPath)
def update_learning_path(path_id: int, path: LearningPathCreate, db: Session = Depends(get_db)):
    db_path = db.query(LearningPathModel).filter(LearningPathModel.id == path_id).first()
    if db_path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    # 更新字段
    for key, value in path.dict().items():
        setattr(db_path, key, value)
    
    db.commit()
    db.refresh(db_path)
    return db_path

# 删除学习路径
@router.delete("/{path_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_learning_path(path_id: int, db: Session = Depends(get_db)):
    db_path = db.query(LearningPathModel).filter(LearningPathModel.id == path_id).first()
    if db_path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    db.delete(db_path)
    db.commit()
    return None

# 获取学习路径的阶段
@router.get("/{path_id}/stages", response_model=list[Stage])
def get_path_stages(path_id: int, db: Session = Depends(get_db)):
    # 检查学习路径是否存在
    path = db.query(LearningPathModel).filter(LearningPathModel.id == path_id).first()
    if path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    stages = db.query(StageModel).filter(StageModel.learning_path_id == path_id).order_by(StageModel.order).all()
    return stages

# 获取学习路径的任务
@router.get("/{path_id}/tasks", response_model=list[Task])
def get_path_tasks(path_id: int, db: Session = Depends(get_db)):
    # 检查学习路径是否存在
    path = db.query(LearningPathModel).filter(LearningPathModel.id == path_id).first()
    if path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    # 获取所有阶段
    stages = db.query(StageModel).filter(StageModel.learning_path_id == path_id).all()
    stage_ids = [stage.id for stage in stages]
    
    # 获取所有任务
    tasks = db.query(TaskModel).filter(TaskModel.stage_id.in_(stage_ids)).order_by(TaskModel.week, TaskModel.day).all()
    return tasks
