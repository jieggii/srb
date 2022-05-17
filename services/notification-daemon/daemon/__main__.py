import asyncio
from datetime import datetime
from typing import NoReturn

import aiohttp
from loguru import logger
from srblib.config import config
from srblib.core import count_next_charge
from srblib.db import init_db
from srblib.db.models import Period, Sub, User


async def send_notification(user: User, sub: Sub, notification: str) -> None:
    text = f"<b>{sub.name}</b> ({sub.amount} / {sub.period}): {notification}."
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://api.telegram.org/bot{config.TOKEN}/sendMessage",
            data={"text": text, "chat_id": user.user_id, "parse_mode": "HTML"},
        ) as response:
            json = await response.json()
            if json.get("ok"):
                logger.info(f"Successfully sent notification to {user}.")
            else:
                logger.info(f"Could not send notification to {user}. Response: {json}.")


async def daemon() -> NoReturn:
    logger.info("Started notifications daemon.")
    while True:
        users = await User.find_all().to_list()
        logger.info(f"Fetched {len(users)} users.")
        for user in users:
            if user.subs:
                for sub in user.subs:
                    today = datetime.today()
                    next_charge = count_next_charge(sub.last_charge, sub.period)
                    days_left = (next_charge - today).days
                    notified_today = (sub.last_notification - today) == 0 if sub.last_notification else None

                    if days_left < 0:
                        logger.warning(
                            f"Detected outdated sub ({sub}). Incremented its last_charge."
                        )
                        sub.last_charge = next_charge

                    if not notified_today:
                        if days_left == 0:
                            sub.last_charge = next_charge
                            sub.last_notification = today
                            await send_notification(
                                user,
                                sub,
                                f"will be charged today. Next charge: <b>{next_charge}</b>.",
                            )

                        elif days_left == 1:
                            sub.last_notification = today
                            await send_notification(
                                user, sub, f"will be charged tomorrow."
                            )

                        elif days_left == 3:
                            sub.last_notification = today
                            await send_notification(
                                user, sub, f"will be charged <b>in three days</b>."
                            )

                        elif days_left == 7 and sub.period != Period.WEEK:
                            sub.last_notification = today
                            await send_notification(
                                user, sub, f"will be charged <b>in a week</b>."
                            )

                await user.save()

        await asyncio.sleep(3)


loop = asyncio.new_event_loop()
init_db(loop)
loop.run_until_complete(daemon())
