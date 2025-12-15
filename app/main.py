from fastapi import FastAPI
from app.routers.chat import router

app = FastAPI(title="Healthcare AI Prototype")
app.include_router(router)
