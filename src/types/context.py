from pydantic import BaseModel
from typing import List


class CreateContextRequest(BaseModel):
    """
    Request model for creating a new context.

    This model defines the structure for creating a new system context file.
    The context name will be normalized to a machine-friendly format.

    Attributes:
        name (str): The display name for the context. This will be normalized to
            lowercase with underscores replacing non-alphanumeric characters.
            Must contain at least one alphanumeric character.

        content (str): The context content/instructions to store. This defines
            the AI's behavior when this context is used. Cannot be empty.

    Example:
        {
            "name": "Helpful Tutor",
            "content": "You are a patient and encouraging tutor who explains concepts clearly."
        }
    """

    name: str
    content: str


class CreateContextResponse(BaseModel):
    """
    Response model for context creation.

    This model defines the structure of the response returned after successfully
    creating a new context file.

    Attributes:
        machine_name (str): The normalized machine name of the created context.
            This is the name used to reference the context in API calls.

        message (str): A success message confirming the context was created.

    Example:
        {
            "machine_name": "helpful_tutor",
            "message": "Context 'helpful_tutor' created successfully"
        }
    """

    machine_name: str
    message: str


class ContextInfo(BaseModel):
    """
    Information model for a single context.

    This model represents metadata about a context file, used when listing
    available contexts.

    Attributes:
        machine_name (str): The normalized machine name of the context.
            This is used to reference the context in API calls.

        file_path (str): The absolute file system path to the context file.

    Example:
        {
            "machine_name": "helpful_tutor",
            "file_path": "/app/contexts/helpful_tutor.md"
        }
    """

    machine_name: str
    file_path: str


class ListContextsResponse(BaseModel):
    """
    Response model for listing contexts.

    This model defines the structure of the response returned when listing
    all available context files.

    Attributes:
        contexts (List[ContextInfo]): A list of context information objects,
            each containing the machine name and file path of a context.

    Example:
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

    contexts: List[ContextInfo]


class DeleteContextResponse(BaseModel):
    """
    Response model for context deletion.

    This model defines the structure of the response returned after successfully
    deleting a context file.

    Attributes:
        message (str): A success message confirming the context was deleted.

    Example:
        {
            "message": "Context 'helpful_tutor' deleted successfully"
        }
    """

    message: str


class ErrorResponse(BaseModel):
    """
    Generic error response model.

    This model defines the structure for error responses returned by the API.

    Attributes:
        error (str): A description of the error that occurred.

    Example:
        {
            "error": "Context name cannot be empty"
        }
    """

    error: str
