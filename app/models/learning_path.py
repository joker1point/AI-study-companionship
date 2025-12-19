from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.config.database import Base

class LearningPath(Base):
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # 快速入门版/全面进阶版/垂直深耕版
    duration = Column(String)  # 6个月/1年/1.5年
    description = Column(Text)  # 路径描述
    target_audience = Column(String)  # 目标人群
    structure = Column(String)  # 路径结构，如"API调用→Prompt工程→轻量应用开发"
    
    # 关系
    stages = relationship("Stage", back_populates="learning_path")
