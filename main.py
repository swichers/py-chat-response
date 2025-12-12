from fastapi import FastAPI, Response
from src.types import ChatRequest, Message, Output, ChatResponse
from src.geminiservice import GeminiTextService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


service = GeminiTextService()


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response_text = service.generate_response(
            text=request.text,
            context=request.context,
            system_context=request.system_context,
        )
        return ChatResponse(
            output=[
                Output(
                    type="message",
                    role="assistant",
                    content=Message(text=response_text),
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return Response(status_code=500)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
