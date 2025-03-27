import uvicorn
from app.core.config import settings
from app.db.session import engine
from app.db.base_class import Base
from app.models import *  # 导入所有模型

# 创建数据库表
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 