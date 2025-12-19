from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# 用户相关模型
class UserBase(BaseModel):
    username: str
    email: EmailStr
    current_level: Optional[str] = "beginner"
    daily_available_time: Optional[int] = 2
    target_direction: Optional[str] = "API调用"
    target_cycle: Optional[str] = "1年"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    current_level: Optional[str] = None
    daily_available_time: Optional[int] = None
    target_direction: Optional[str] = None
    target_cycle: Optional[str] = None

class UserInDB(UserBase):
    id: int
    password_hash: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 认证相关模型
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# 学习路径相关模型
class LearningPathBase(BaseModel):
    name: str
    duration: str
    description: str
    target_audience: str
    structure: str

class LearningPathCreate(LearningPathBase):
    pass

class LearningPath(LearningPathBase):
    id: int

    class Config:
        from_attributes = True

# 阶段相关模型
class StageBase(BaseModel):
    name: str
    description: str
    order: int
    learning_path_id: int

class StageCreate(StageBase):
    pass

class Stage(StageBase):
    id: int

    class Config:
        from_attributes = True

# 任务相关模型
class TaskBase(BaseModel):
    title: str
    description: str
    duration: int
    difficulty: str
    stage_id: int
    week: int
    day: int
    is_weekend: bool = False
    is_milestone: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True

# 用户任务进度相关模型
class UserTaskProgressBase(BaseModel):
    user_id: int
    task_id: int
    is_completed: bool = False
    actual_duration: Optional[int] = None
    notes: Optional[str] = None

class UserTaskProgressCreate(UserTaskProgressBase):
    pass

class UserTaskProgress(UserTaskProgressBase):
    id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
