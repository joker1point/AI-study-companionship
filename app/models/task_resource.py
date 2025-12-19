from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class TaskResource(Base):
    __tablename__ = "task_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    title = Column(String)  # 资源标题
    url = Column(String)  # 资源链接
    resource_type = Column(String)  # 资源类型：doc/tutorial/code/example
    description = Column(Text)  # 资源描述
    
    # 关系
    task = relationship("Task", back_populates="resources")
