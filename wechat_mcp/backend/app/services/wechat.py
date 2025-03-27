from app.core.config import settings
from app.models.article import Article, ArticleStatus
from datetime import datetime
import logging
from app.util.wechat import WeixinPublisherUtil
from wechatpy.exceptions import WeChatClientException
import json

logger = logging.getLogger(__name__)

class WeChatService:
    def __init__(self):
        self.publisher = WeixinPublisherUtil(settings.WECHAT_APP_ID, settings.WECHAT_APP_SECRET)

    async def publish_article(self, article: Article) -> bool:
        """
        发布文章到微信公众号
        """
        try:
            # 准备文章数据
            articles = [{
                'title': article.title,
                'thumb_media_id': article.thumbnail_url,  # 需要先上传图片获取media_id
                'author': article.author,
                'digest': article.digest,
                'content': article.content,
                'content_source_url': '',  # 原文链接
                'need_open_comment': 1,  # 是否打开评论
                'only_fans_can_comment': 0  # 是否粉丝才可评论
            }]
            # 发布文章
            result = await self.publisher.publish(articles)
            
            if result.get('publish_id'):
                article.wechat_article_id = result['publish_id']
                article.status = ArticleStatus.PUBLISHED
                article.published_time = datetime.now()
                return True
            return False

        except WeChatClientException as e:
            logger.error(f"发布文章失败: {str(e)}")
            article.status = ArticleStatus.FAILED
            return False

    async def upload_image(self, image_data: bytes) -> str:
        """
        上传图片到微信服务器
        """
        try:
            return await self.publisher.upload_image(image_data)
        except WeChatClientException as e:
            logger.error(f"上传图片失败: {str(e)}")
            return None