from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite数据库URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./study_plan.db"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite特定参数，允许多线程访问
)

# 创建SessionLocal类，每个实例将是一个数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建Base类，所有模型类将继承自这个类
Base = declarative_base()

# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
