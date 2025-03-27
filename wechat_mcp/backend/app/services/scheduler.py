from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from app.models.article import Article, ArticleStatus
from app.services.wechat import WeChatService
from app.db.session import SessionLocal
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.wechat_service = WeChatService()
        self.scheduler.start()

    async def schedule_article(self, article: Article):
        """
        调度文章发布任务
        """
        if not article.scheduled_time:
            logger.error(f"文章 {article.id} 没有设置发布时间")
            return False

        # 创建定时任务
        job_id = f"article_{article.id}"
        self.scheduler.add_job(
            self._publish_article,
            CronTrigger.from_datetime(article.scheduled_time),
            id=job_id,
            args=[article.id],
            replace_existing=True
        )
        
        article.status = ArticleStatus.SCHEDULED
        return True

    async def _publish_article(self, article_id: int):
        """
        发布文章的具体实现
        """
        db = SessionLocal()
        try:
            article = db.query(Article).filter(Article.id == article_id).first()
            if not article:
                logger.error(f"文章 {article_id} 不存在")
                return

            success = await self.wechat_service.publish_article(article)
            if success:
                logger.info(f"文章 {article_id} 发布成功")
            else:
                logger.error(f"文章 {article_id} 发布失败")

            db.commit()
        except Exception as e:
            logger.error(f"发布文章 {article_id} 时发生错误: {str(e)}")
            db.rollback()
        finally:
            db.close()

    def remove_job(self, article_id: int):
        """
        移除定时任务
        """
        job_id = f"article_{article_id}"
        self.scheduler.remove_job(job_id)

    def shutdown(self):
        """
        关闭调度器
        """
        self.scheduler.shutdown() 