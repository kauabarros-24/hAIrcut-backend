from fastapi import FastAPI
from src import routers
from tortoise.contrib.fastapi import register_tortoise
from src.config import TORTOISE_ORM

app = FastAPI(title="My API")

app.include_router(routers.router, prefix="/api", tags=["users"])

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
