import os
from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()

DB_URL = os.getenv("DB_URL")

async def init_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models":["models"]}
        
    )
    await Tortoise.generate_schemas()
    

try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
    if not GEMINI_API_KEY:
        raise ValueError("Gemini api key is none")
except Exception as error:
    raise ValueError(f"API KEY with error: {error}")

