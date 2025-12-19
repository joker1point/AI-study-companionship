from passlib.context import CryptContext

# 密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 哈希密码
def get_password_hash(password):
    return pwd_context.hash(password)

# 验证密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
