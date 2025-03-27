from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.article import ArticleStatus

class ArticleBase(BaseModel):
    title: str
    content: str
    author: Optional[str] = None
    digest: Optional[str] = None
    thumbnail_url: Optional[str] = None
    category_id: Optional[int] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    digest: Optional[str] = None
    thumbnail_url: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[int] = None

class ArticleResponse(ArticleBase):
    id: int
    status: int
    scheduled_time: Optional[datetime] = None
    published_time: Optional[datetime] = None
    wechat_article_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 