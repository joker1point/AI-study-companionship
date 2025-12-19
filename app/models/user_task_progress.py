from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserTaskProgress(Base):
    __tablename__ = "user_task_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    is_completed = Column(Boolean, default=False)  # 是否已完成
    completed_at = Column(DateTime(timezone=True))  # 完成时间
    actual_duration = Column(Integer)  # 实际完成时间（分钟）
    notes = Column(String)  # 用户笔记
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="task_progress")
    task = relationship("Task", back_populates="user_task_progress")
