from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.config.database import Base

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # 任务标题
    description = Column(Text)  # 任务描述
    duration = Column(Integer)  # 预计完成时间（分钟）
    difficulty = Column(String)  # easy/medium/hard
    stage_id = Column(Integer, ForeignKey("stages.id"))
    week = Column(Integer)  # 所属周数
    day = Column(Integer)  # 所属天数（1-7）
    is_weekend = Column(Boolean, default=False)  # 是否为周末实战任务
    is_milestone = Column(Boolean, default=False)  # 是否为里程碑项目
    
    # 关系
    stage = relationship("Stage", back_populates="tasks")
    user_task_progress = relationship("UserTaskProgress", back_populates="task")
    resources = relationship("TaskResource", back_populates="task")
