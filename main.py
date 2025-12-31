from fastapi import FastAPI
from src.routes import context_routes, chat_routes
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(context_routes.router)
app.include_router(chat_routes.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
