from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from loguru import logger
from srblib.db.models import User


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self):
        super(DatabaseMiddleware, self).__init__()

    async def on_process_message(self, message: Message, _) -> None:  # noqa
        user = await User.find_one(User.user_id == message.from_user.id)
        if not user:
            await User(user_id=message.from_user.id).create()
            logger.info(
                f"Registered a new user - @{message.from_user.username} ({message.from_user.id})."
            )
