from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, learning_paths, tasks, progress

app = FastAPI(
    title="AI大模型应用开发学习计划工具",
    description="专为0基础转行/技能升级人群打造的大模型应用开发学习计划工具",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(learning_paths.router, prefix="/api/learning-paths", tags=["learning-paths"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])

@app.get("/")
def read_root():
    return {"message": "欢迎使用AI大模型应用开发学习计划工具"}
