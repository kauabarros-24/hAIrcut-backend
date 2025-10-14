import os
from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DB_URL = os.getenv("DB_URL")

TORTOISE_ORM = {
    "connections": {"default": DB_URL},  
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],  
            "default_connection": "default",
        }
    }
}
    

try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
    if not GEMINI_API_KEY:
        raise ValueError("Gemini api key is none")
except Exception as error:
    raise ValueError(f"API KEY with error: {error}")

