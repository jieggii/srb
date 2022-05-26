import asyncio

from beanie import init_beanie
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from srblib.config import config
from srblib.db.models import User


def init_db(loop: asyncio.AbstractEventLoop):
    client = AsyncIOMotorClient(f"mongodb://{config.Mongo.HOST}:{config.Mongo.PORT}")
    client.get_io_loop = asyncio.get_running_loop
    loop.run_until_complete(init_beanie(database=client[config.Mongo.DB_NAME], document_models=[User]))
    logger.info(f"Initialized {config.Mongo.DB_NAME} database.")
