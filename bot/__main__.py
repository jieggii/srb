from aiogram import Bot, Dispatcher, executor, types

from bot.config import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def handle_start(message: types.Message):
    first_name = message.from_user.first_name
    await message.reply(
        f"Hello, {first_name}. I will remind you about your paid subscriptions so that "
        f"you don't forget to pay or cancel them on time!\n\n"
        f"Use /new to add a new subscription.\n"
        f"Type /help to see all available commands.",
    )


@dp.message_handler(commands="help")
async def handle_help(message: types.Message):
    await message.reply(
        "<b>Available commands:</b>\n"
        "/help - get list of available commands\n"
        "/new - add a new subscription\n"
        "/all - get list of all subscriptions\n"
        "/upcoming - get list of upcoming subscriptions\n"
        "/remove - remove subscription",
        parse_mode="HTML",
    )


@dp.message_handler(commands="all")
async def handle_all(message: types.Message):
    await message.reply("start")


@dp.message_handler(commands="upcoming")
async def handle_upcoming(message: types.Message):
    await message.reply("start")


@dp.message_handler(commands="new")
async def handle_new(message: types.Message):
    await message.reply("start")


@dp.message_handler(commands="remove")
async def handle_remove(message: types.Message):
    await message.reply("start")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
