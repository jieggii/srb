from typing import List

import ujson
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.models import Sub


def generate_remove_sub_inline_keyboard(
    user_message_id: int, subs: List[Sub]
) -> InlineKeyboardMarkup:
    kbd = InlineKeyboardMarkup(row_width=3)
    kbd.add(
        *(
            InlineKeyboardButton(
                text=sub.name,
                callback_data=ujson.dumps(
                    {
                        "command": "remove_sub",
                        "sub_index": i,
                        "edit_message_id": user_message_id + 1,
                    }
                ),
            )
            for i, sub in enumerate(subs)
        )
    )
    return kbd
