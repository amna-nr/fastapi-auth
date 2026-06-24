from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.core.redis import redis_client
from app.core.logging import setup_logging, logger
from app.routes.auth import router as auth_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("app_started")
    await redis_client.ping()
    logger.info("redis_connected")
    yield
    await redis_client.aclose()
    logger.info("app_shutdown")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "welcome to fastapi auth"}