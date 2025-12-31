from fastapi import APIRouter, HTTPException
import logging
from src.types.chat import ChatRequest, Message, Output, ChatResponse
from src.context_manager import ContextManager
from src.geminiservice import GeminiTextService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])
service = GeminiTextService()
context_manager = ContextManager()


@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        system_context = None

        if request.system_context:
            system_context = context_manager.get_context_content(request.system_context)
            if system_context is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Context '{request.system_context}' not found",
                )
        else:
            system_context = context_manager.get_context_content("default")

        response_text = service.generate_response(
            text=request.text,
            context=request.context,
            system_context=system_context,
        )
        return ChatResponse(
            output=[
                Output(
                    type="message",
                    role="assistant",
                    system_context=request.system_context,
                    content=Message(text=response_text),
                )
            ]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
