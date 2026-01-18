from fastapi import FastAPI
from app.routers import router

app = FastAPI(title="Wallet API")

app.include_router(router, prefix="/api/v1")
