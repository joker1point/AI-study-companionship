from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # 成就名称
    description = Column(Text)  # 成就描述
    badge_type = Column(String)  # 勋章类型
    condition = Column(String)  # 解锁条件
    is_awarded = Column(Boolean, default=False)  # 是否已授予
    awarded_at = Column(DateTime(timezone=True))  # 授予时间
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="achievements")
