import os
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import requests


class WeixinToken:
    def __init__(self, access_token: str, expires_in: int):
        self.access_token = access_token
        self.expires_in = expires_in
        self.expires_at = datetime.now() + timedelta(seconds=expires_in)

class WeixinDraft:
    def __init__(self, media_id: str, article_id: Optional[str] = None):
        self.media_id = media_id
        self.article_id = article_id

class WeixinPublisherUtil:
    def __init__(self, app_id: str, app_secret: str):
        self.access_token: Optional[WeixinToken] = None
        self.app_id: Optional[str] = app_id
        self.app_secret: Optional[str] = app_secret


    async def ensure_access_token(self) -> str:
        """确保access_token有效"""
        # 检查现有token是否有效
        if (self.access_token and 
            self.access_token.expires_at > datetime.now() + timedelta(minutes=1)):
            return self.access_token.access_token

        # 获取新token
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"

        try:
            response = requests.get(url)
            data = response.json()

            print(data,"data")
            
            if 'access_token' not in data:
                raise ValueError(f"获取access_token失败: {data}")

            self.access_token = WeixinToken(
                access_token=data['access_token'],
                expires_in=data['expires_in']
            )

            return self.access_token.access_token
        except Exception as e:
            print(f"获取微信access_token失败: {e}")
            raise

    async def upload_draft(self, articles: List[Dict[str, Any]]) -> WeixinDraft:
        """上传草稿"""
        token = await self.ensure_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"

        articles_json = []

        for article in articles:
            articles_json.append({
                "title": article['title'],
                "author": article['author'],
                "digest": article['digest'],
                "content": article['content'],
                "thumb_media_id": article['thumb_media_id'],
            })

        try:
            response = requests.post(url, json={"articles": articles_json})
            data = response.json()
            if 'errcode' in data:
                raise ValueError(f"上传草稿失败: {data['errmsg']}")

            return WeixinDraft(media_id=data['media_id'])
        except Exception as e:
            print(f"上传微信草稿失败: {e}")
            raise

    async def upload_image(self, image_data: bytes) -> str:
        """上传图片"""

        token = await self.ensure_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"

        try:
            files = {
                'media': (
                    f'image_{os.urandom(3).hex()}.jpg',
                    image_data,
                    'image/jpeg'
                )
            }
            response = requests.post(url, files=files)
            data = response.json()
            print(data,"data")
            if 'errcode' in data:
                raise ValueError(f"上传图片失败: {data['errmsg']}")
            return data
        except Exception as e:
            print(f"上传微信图片失败: {e}")
            raise


    async def publish(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """发布文章"""
        try:
            draft = await self.upload_draft(articles)
            """上传文章"""
            token = await self.ensure_access_token()
            url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={token}"
            try:
                response = requests.post(url, json={"media_id": draft.media_id})
                data = response.json()
                
            except Exception as e:
                print(f"上传文章失败: {e}")
                raise

            return {
                "publish_id": data['publish_id'],
                "url": f"https://mp.weixin.qq.com/s/{draft.media_id}"
            }
        except Exception as e:
            print(f"微信发布失败: {e}")
            raise
