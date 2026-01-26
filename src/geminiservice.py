from google import genai
from src.config import Config
import logging

logger = logging.getLogger(__name__)


class GeminiTextService:
    """
    Service class for interacting with Google's Gemini AI API.

    This service handles text generation using the Gemini language model.
    It manages API authentication, client initialization, and request formatting.

    Attributes:
        api_key (str): The API key for authenticating with Gemini API.
        client (genai.Client): The initialized Gemini API client.
        model_name (str): The name of the Gemini model to use for generation.
    """

    def __init__(self):
        """
        Initialize the GeminiTextService.

        Loads configuration from the Config class and initializes the Gemini API client.
        The API key and model name are retrieved from environment variables via Config.

        Raises:
            Exception: If the API key is not set or client initialization fails.
        """
        self.api_key = Config.LLM_API_KEY
        if not self.api_key:
            logger.warning("LLM_API_KEY not found. GeminiTextService calls will fail.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
        self.model_name = Config.LLM_MODEL

    def generate_response(
        self, text: str, context: str = None, system_context: str = None
    ) -> str:
        """
        Generate a text response using the Gemini AI model.

        This method sends a prompt to the Gemini API and returns the generated text.
        It supports optional context and system instructions to guide the response.

        Args:
            text (str): The main input text or question to generate a response for.
                This is the primary prompt sent to the model.

            context (str, optional): Additional context to prepend to the text.
                This provides background information that helps the model generate
                more relevant responses. Defaults to None.

            system_context (str, optional): System-level instructions for the model.
                This sets the behavior, personality, or constraints for the AI.
                Loaded from context files when specified. Defaults to None.

        Returns:
            str: The generated text response from the Gemini model.

        Raises:
            Exception: If the API request fails or returns an error.

        Example:
            >>> service = GeminiTextService()
            >>> response = service.generate_response(
            ...     text="What is the weather like?",
            ...     context="The user is in San Francisco.",
            ...     system_context="You are a helpful weather assistant."
            ... )
            >>> print(response)
            "The weather in San Francisco is typically mild..."
        """
        prompt = f"{context}\n{text}" if context else text

        def truncate(text, limit=10):
            """
            Truncate text to a specified number of words for logging.

            Args:
                text (str): The text to truncate.
                limit (int, optional): Maximum number of words to include. Defaults to 10.

            Returns:
                str: The truncated text with "..." appended if truncated,
                     or "None" if the input text is empty.
            """
            if not text:
                return "None"
            words = text.split()
            if len(words) <= limit:
                return text
            return " ".join(words[:limit]) + "..."

        logger.info(
            f"Generating response for text: '{truncate(text)}' with system context: '{truncate(system_context)}'"
        )

        gen_config = {"response_modalities": ["TEXT"]}
        if system_context:
            gen_config["system_instruction"] = system_context

        try:
            if not self.client:
                raise ValueError(
                    "Gemini API client is not initialized. Please set LLM_API_KEY."
                )

            response = self.client.models.generate_content(
                model=self.model_name, contents=prompt, config=gen_config
            )
            return response.text
        except Exception as e:
            raise e
