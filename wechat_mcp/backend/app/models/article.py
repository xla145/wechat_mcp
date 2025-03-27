from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class ArticleStatus(str, enum.Enum):
    DRAFT = 0
    SCHEDULED = 1
    PUBLISHED = 2
    FAILED = 3

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100))
    status = Column(Integer, default=ArticleStatus.DRAFT.value)
    scheduled_time = Column(DateTime, nullable=True)
    published_time = Column(DateTime, nullable=True)
    wechat_article_id = Column(String(100), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    digest = Column(String(500), nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    # 关联
    category_id = Column(Integer, ForeignKey("categories.id", ondelete='SET NULL'), nullable=True)
    category = relationship("Category", back_populates="articles")
    tags = relationship("Tag", secondary="article_tags", back_populates="articles") 