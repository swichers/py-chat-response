from fastapi import APIRouter, HTTPException
from src.types.context import (
    CreateContextRequest,
    CreateContextResponse,
    ListContextsResponse,
    DeleteContextResponse,
    ContextInfo,
)
from src.context_manager import ContextManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/contexts", tags=["contexts"])
context_manager = ContextManager()


@router.get("", response_model=ListContextsResponse)
async def list_contexts():
    """
    List all available context files.

    This endpoint retrieves all context files stored in the contexts directory.
    Each context file contains system instructions that can be used to customize
    the AI's behavior in chat responses.

    Returns:
        ListContextsResponse: Response containing:
            - contexts (List[ContextInfo]): List of context information, each containing:
                - machine_name (str): The normalized machine name of the context
                - file_path (str): The absolute path to the context file

    Raises:
        HTTPException: 500 error if there's an issue reading the contexts directory

    Example:
        Request:
            GET /api/v1/contexts

        Response (200 OK):
            {
                "contexts": [
                    {
                        "machine_name": "default",
                        "file_path": "/app/contexts/default.md"
                    },
                    {
                        "machine_name": "helpful_tutor",
                        "file_path": "/app/contexts/helpful_tutor.md"
                    }
                ]
            }
    """
    try:
        contexts = context_manager.list_contexts()
        return ListContextsResponse(contexts=[ContextInfo(**ctx) for ctx in contexts])
    except Exception as e:
        logger.error(f"Error listing contexts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=CreateContextResponse)
async def create_context(request: CreateContextRequest):
    """
    Create a new context file.

    This endpoint creates a new system context file that can be used to customize
    the AI's behavior. The context name is automatically normalized to a machine-friendly
    format (lowercase with underscores), and the content is saved as a Markdown file
    in the contexts directory.

    Args:
        request (CreateContextRequest): The context creation request containing:
            - name (str): The display name for the context. Will be normalized to
              lowercase with underscores replacing non-alphanumeric characters.
            - content (str): The context content/instructions to store. This defines
              the AI's behavior when this context is used.

    Returns:
        CreateContextResponse: Response containing:
            - machine_name (str): The normalized machine name of the created context
            - message (str): Success message confirming creation

    Raises:
        HTTPException:
            - 400: If name or content is empty, or name contains no alphanumeric characters
            - 500: If there's an error writing the context file

    Example:
        Request:
            POST /api/v1/contexts
            Content-Type: application/json

            {
                "name": "Helpful Tutor",
                "content": "You are a patient and encouraging tutor who explains concepts clearly."
            }

        Response (200 OK):
            {
                "machine_name": "helpful_tutor",
                "message": "Context 'helpful_tutor' created successfully"
            }

        Error Response (400 Bad Request):
            {
                "detail": "Context name cannot be empty"
            }
    """
    try:
        result = context_manager.create_context(
            name=request.name, content=request.content
        )
        return CreateContextResponse(**result)
    except ValueError as e:
        logger.error(f"Validation error creating context: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating context: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{machine_name}", response_model=DeleteContextResponse)
async def delete_context(machine_name: str):
    """
    Delete a context file by its machine name.

    This endpoint permanently removes a context file from the contexts directory.
    The machine name must match exactly (lowercase with underscores).

    Args:
        machine_name (str): The normalized machine name of the context to delete.
            This should be the exact machine_name returned when the context was created
            or listed (e.g., "helpful_tutor", not "Helpful Tutor").

    Returns:
        DeleteContextResponse: Response containing:
            - message (str): Success message confirming deletion

    Raises:
        HTTPException:
            - 404: If the context file with the specified machine_name doesn't exist
            - 500: If there's an error deleting the context file

    Example:
        Request:
            DELETE /api/v1/contexts/helpful_tutor

        Response (200 OK):
            {
                "message": "Context 'helpful_tutor' deleted successfully"
            }

        Error Response (404 Not Found):
            {
                "detail": "Context 'helpful_tutor' not found"
            }
    """
    try:
        result = context_manager.delete_context(machine_name)
        return DeleteContextResponse(**result)
    except FileNotFoundError as e:
        logger.error(f"Context not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting context: {e}")
        raise HTTPException(status_code=500, detail=str(e))
