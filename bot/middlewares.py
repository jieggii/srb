from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from loguru import logger

from bot.models import User


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self):
        super(DatabaseMiddleware, self).__init__()

    async def on_process_message(self, message: Message, _) -> None:  # noqa
        user = User(user_id=message.from_user.id)
        if not await user.find_one():
            await user.create()
            logger.info(
                f"Registered a new user - @{message.from_user.username} ({message.from_user.id})"
            )
