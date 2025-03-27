from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.api import deps
from app.models.article import Article, ArticleStatus
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse
from app.services.scheduler import SchedulerService
from app.services.wechat import WeChatService
from fastapi import UploadFile, File

router = APIRouter()
scheduler_service = SchedulerService()
wechat_service = WeChatService()

from typing import Any

class BaseResponse():

    @staticmethod
    def success(data: Any):
        return {
            "data": data,
            "message": "操作成功",
            "code": 0
        }
    
    @staticmethod
    def error(message: str):
        return {
            "data": None,
            "message": message,
            "code": 1
        }

@router.post("/", description="创建新文章")
async def create_article(
    *,
    db: Session = Depends(deps.get_db),
    article_in: ArticleCreate,
): 
    """
    创建新文章
    """
    article = Article(
        title=article_in.title,
        content=article_in.content,
        author=article_in.author,
        digest=article_in.digest,
        thumbnail_url=article_in.thumbnail_url,
        category_id=article_in.category_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(article)
    db.commit()
    db.refresh(article)
    return BaseResponse.success(article)


@router.get("/", response_model=List[ArticleResponse])
async def list_articles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[ArticleStatus] = None,
):
    """
    获取文章列表
    """
    query = db.query(Article)
    if status:
        query = query.filter(Article.status == status)
    
    articles = query.offset(skip).limit(limit).all()
    return articles

@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    获取文章详情
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    return article

@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    article_in: ArticleUpdate,
    db: Session = Depends(deps.get_db),
):
    """
    更新文章
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    for field, value in article_in.dict(exclude_unset=True).items():
        setattr(article, field, value)
    
    article.updated_at = datetime.now()
    db.commit()
    db.refresh(article)
    
    return article

@router.post("/{article_id}/schedule")
async def schedule_article(
    article_id: int,
    scheduled_time: datetime,
    db: Session = Depends(deps.get_db),
):
    """
    设置文章定时发布
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    article.scheduled_time = scheduled_time
    success = await scheduler_service.schedule_article(article)
    
    if success:
        db.commit()
        return {"message": "文章已加入发布队列"}
    else:
        raise HTTPException(status_code=400, detail="设置定时发布失败")

@router.post("/{article_id}/publish")
async def publish_article(
    article_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    立即发布文章
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    success = await wechat_service.publish_article(article)
    if success:
        db.commit()
        return {"message": "文章发布成功"}
    else:
        raise HTTPException(status_code=400, detail="文章发布失败")

@router.delete("/{article_id}")
async def delete_article(
    article_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    删除文章
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 如果文章已加入发布队列，先移除定时任务
    if article.status == ArticleStatus.SCHEDULED:
        scheduler_service.remove_job(article_id)
    
    db.delete(article)
    db.commit()
    return {"message": "文章删除成功"} 



@router.post("/upload_thumbnail")
async def upload_thumbnail(
    file: UploadFile = File(...),
):
    """
    上传文章缩略图
    """
    media_id = await wechat_service.upload_image(file.file)
    return BaseResponse.success(media_id)
