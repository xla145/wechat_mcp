from fastapi import APIRouter
from app.api.api_v1.endpoints import articles

api_router = APIRouter()
api_router.include_router(articles.router, prefix="/articles", tags=["articles"]) 