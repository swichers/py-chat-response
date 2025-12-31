import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class for the chat response service.

    This class loads and stores configuration values from environment variables.
    It uses python-dotenv to load variables from a .env file if present.

    Attributes:
        LLM_API_KEY (str): The API key for the Gemini LLM service.
            Required for authentication with the Gemini API.
            Loaded from the LLM_API_KEY environment variable.

        LLM_MODEL (str): The name of the Gemini model to use for text generation.
            Defaults to "gemini-2.5-flash-lite" if not specified.
            Loaded from the LLM_MODEL environment variable.

    Example:
        Environment variables in .env file:
            LLM_API_KEY=your_api_key_here
            LLM_MODEL=gemini-2.5-flash-lite
    """

    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")
