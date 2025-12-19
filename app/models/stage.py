from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Stage(Base):
    __tablename__ = "stages"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # 基础搭建/核心技能/项目实战/深化进阶
    description = Column(Text)  # 阶段描述
    order = Column(Integer)  # 阶段顺序
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"))
    
    # 关系
    learning_path = relationship("LearningPath", back_populates="stages")
    tasks = relationship("Task", back_populates="stage")
