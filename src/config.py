import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")
    SYSTEM_CONTEXT = os.getenv("SYSTEM_CONTEXT", "system_context.md")
