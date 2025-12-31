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
    """
    Health check endpoint for the API.

    This endpoint is used to verify that the API service is running and responsive.
    It returns a simple status message indicating the service is operational.

    Returns:
        dict: A dictionary containing the health status.
            - status (str): Always returns "ok" when the service is running.

    Example:
        Request:
            GET /health

        Response (200 OK):
            {
                "status": "ok"
            }
    """
    return {"status": "ok"}
