"""
Here you should do all needed actions. Standart configuration of docker container
will run your application with this file.
"""
from fastapi import FastAPI
from loguru import logger
from tortoise import Tortoise

from app.config import openapi_config
from app.config.db import DB_MODELS
from app.initializer import init

app = FastAPI(
    title=openapi_config.name,
    version=openapi_config.version,
    description=openapi_config.description,
)

Tortoise.init_models(DB_MODELS, 'models')

logger.info("Starting application initialization...")
init(app)
logger.success("Successfully initialized!")
