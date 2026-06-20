import redis.asyncio as redis 
from app.core.config import settings
from fastapi import Depends
from typing import Annotated

REDIS_URL = settings.REDIS_URL

redis_client = redis.from_url(
    REDIS_URL, 
    decode_responses=True
)

async def get_redis():
    yield redis_client

redis_dependency = Annotated[redis.Redis, Depends(get_redis)]
    