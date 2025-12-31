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
    """
    Generate an AI chat response using the Gemini language model.

    This endpoint accepts a text prompt along with optional context and system context,
    then generates a response using the configured Gemini AI model. The system context
    can be loaded from predefined context files to customize the AI's behavior.

    Args:
        request (ChatRequest): The chat request containing:
            - text (str): The main input text or question to generate a response for.
            - context (str, optional): Additional context to prepend to the text.
            - system_context (str, optional): Machine name of a context file to use
              as system instructions. If not provided, uses "default" context if available.

    Returns:
        ChatResponse: The generated response containing:
            - output (List[Output]): List of output messages, each containing:
                - type (str): Message type, always "message"
                - role (str): Message role, always "assistant"
                - system_context (str, optional): The system context used
                - content (Message): The message content with:
                    - text (str): The generated response text

    Raises:
        HTTPException:
            - 404: If the specified system_context file is not found
            - 500: If there's an error generating the response

    Example:
        Request:
            POST /api/v1/chat
            Content-Type: application/json

            {
                "text": "What is the capital of France?",
                "context": "The user is learning about European geography.",
                "system_context": "helpful_tutor"
            }

        Response (200 OK):
            {
                "output": [
                    {
                        "type": "message",
                        "role": "assistant",
                        "system_context": "helpful_tutor",
                        "content": {
                            "text": "The capital of France is Paris. It's one of the most famous cities in Europe..."
                        }
                    }
                ]
            }

        Error Response (404 Not Found):
            {
                "detail": "Context 'helpful_tutor' not found"
            }
    """
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
