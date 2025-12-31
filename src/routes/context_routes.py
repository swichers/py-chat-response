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
    """List all available context files."""
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

    The name will be normalized to lowercase with underscores replacing
    non-alphanumeric characters. The content will be saved to a .md file
    in the contexts/ directory.
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
    """Delete a context file by its machine name."""
    try:
        result = context_manager.delete_context(machine_name)
        return DeleteContextResponse(**result)
    except FileNotFoundError as e:
        logger.error(f"Context not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting context: {e}")
        raise HTTPException(status_code=500, detail=str(e))
