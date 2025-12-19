from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    current_level = Column(String, default="beginner")  # 0基础/有编程经验/有AI基础
    daily_available_time = Column(Integer)  # 每日可学习时长（小时）
    target_direction = Column(String)  # API调用/私有知识库/RAG/Agent开发
    target_cycle = Column(String)  # 6个月/1年/1.5年
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    task_progress = relationship("UserTaskProgress", back_populates="user")
    achievements = relationship("Achievement", back_populates="user")
