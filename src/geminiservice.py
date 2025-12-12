from google import genai
from src.config import Config
import logging

logger = logging.getLogger(__name__)


class GeminiTextService:
    def __init__(self):
        self.api_key = Config.LLM_API_KEY
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = Config.LLM_MODEL

    def generate_response(
        self, text: str, context: str = None, system_context: str = None
    ) -> str:
        prompt = f"{context}\n{text}" if context else text

        sys_instruction = system_context
        if not sys_instruction:
            try:
                with open(Config.SYSTEM_CONTEXT, "r") as f:
                    sys_instruction = f.read().strip()
            except FileNotFoundError:
                sys_instruction = None

        def truncate(text, limit=10):
            if not text:
                return "None"
            words = text.split()
            if len(words) <= limit:
                return text
            return " ".join(words[:limit]) + "..."

        logger.info(
            f"Generating response for text: '{truncate(text)}' with system context: '{truncate(sys_instruction)}'"
        )

        gen_config = {"response_modalities": ["TEXT"]}
        if sys_instruction:
            gen_config["system_instruction"] = sys_instruction

        try:
            response = self.client.models.generate_content(
                model=self.model_name, contents=prompt, config=gen_config
            )
            return response.text
        except Exception as e:
            raise e
