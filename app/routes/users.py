from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models import User as UserModel
from app.models.schemas import User, UserCreate
from app.utils.auth import get_password_hash

router = APIRouter()

# 简化版：直接获取用户（跳过认证）
def get_current_user(user_id: int = 1, db: Session = Depends(get_db)):
    """简化实现，直接返回指定ID的用户"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        # 如果用户不存在，创建一个默认用户
        default_user = UserModel(
            username="default_user",
            email="default@example.com",
            password_hash=get_password_hash("password123"),
            current_level="beginner",
            daily_available_time=2,
            target_direction="API调用",
            target_cycle="1年"
        )
        db.add(default_user)
        db.commit()
        db.refresh(default_user)
        return default_user
    return user

# 用户注册
@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # 检查邮箱是否已存在
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 创建新用户
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        current_level=user.current_level,
        daily_available_time=user.daily_available_time,
        target_direction=user.target_direction,
        target_cycle=user.target_cycle
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 获取当前用户信息（简化版，直接返回默认用户）
@router.get("/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

# 获取所有用户
@router.get("/", response_model=list[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

# 获取特定用户信息
@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
