import os
from dotenv import load_dotenv

load_dotenv()
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("Gemini api key is none")
except Exception as error:
    raise ValueError(f"API KEY with error: {error}")