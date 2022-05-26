import asyncio
import logging
from datetime import datetime

import ujson
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from loguru import logger
from srblib.config import config
from srblib.core import count_next_charge
from srblib.db import init_db
from srblib.db.models import Period, Sub, User

from bot import cliche
from bot.fsm import NewSub
from bot.inline_keyboards import generate_remove_sub_inline_keyboard
from bot.keyboards import new_sub_last_charge_kbd, new_sub_select_period_kbd
from bot.middlewares import DatabaseMiddleware

logging.basicConfig(level=logging.ERROR)

loop = asyncio.new_event_loop()
init_db(loop)

bot = Bot(token=config.Bot.TOKEN, loop=loop)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(state="*", commands="cancel")
async def handle_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
    await message.reply("Cancelled", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands="start")
async def handle_start(message: types.Message):
    first_name = message.from_user.first_name
    await message.reply(
        f"Hello there, {first_name}! I will remind you about your paid subscriptions so that "
        f"you don't forget to pay or cancel them on time.\n\n"
        f"Use /new to add a new subscription or "
        f"type /help to see other available commands.",
    )


@dp.message_handler(commands="help")
async def handle_help(message: types.Message):
    await message.reply(
        "<b>Available commands:</b>\n"
        "/help - list available commands\n"
        "/new - create a new subscription\n"
        "/all - list all subscriptions\n"
        "/remove - remove a subscription\n",
        parse_mode="HTML",
    )


@dp.message_handler(commands="new")
async def handle_new(message: types.Message):
    await message.answer(
        "All right, let's cut to the chase. What's name of the subscription?"
    )
    await NewSub.name.set()


@dp.message_handler(state=NewSub.name)
async def state_new_sub_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await message.reply(
        "Got it. What is the payment period?", reply_markup=new_sub_select_period_kbd
    )
    await NewSub.next()


@dp.message_handler(state=NewSub.period)
async def state_new_sub_period(message: types.Message, state: FSMContext):
    try:
        period = Period(message.text.lower())
    except ValueError:
        await message.reply("Wrong period. Please select it using keyboard.")
        return
    async with state.proxy() as data:
        data["period"] = period
    await message.reply(
        'Now I need you to type amount for the given payment period (with currency), for example: "10 USD".',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await NewSub.next()


@dp.message_handler(state=NewSub.amount)
async def state_new_sub_amount(message: types.Message, state: FSMContext):
    amount = message.text
    async with state.proxy() as data:
        data["amount"] = amount
        await message.reply(
            "And the final question: send me the last charge date in <b>dd.mm.yyyy</b> "
            "format (04.05.2022 for example) or press <b>Today</b> button (if the last charge has happened today).",
            parse_mode="HTML",
            reply_markup=new_sub_last_charge_kbd,
        )
        await NewSub.next()


@dp.message_handler(state=NewSub.last_charge)
async def state_new_sub_last_charge(message: types.Message, state: FSMContext):
    match message.text:
        case "Today":
            last_charge = datetime.today()
        case _:
            try:
                last_charge = datetime.strptime(message.text, "%d.%m.%Y")
            except ValueError:
                await message.reply(
                    "Wrong date. Please send the last charge date in <b>dd.mm.yyyy</b> format (04.05.2022 for example)"
                    "or press <b>Today</b> button.",
                    parse_mode="HTML",
                )
                return
    async with state.proxy() as data:
        data["last_charge"] = last_charge
        sub = Sub(**data)
        user = await User.find_one(User.user_id == message.from_user.id)
        if user.subs:
            user.subs.append(sub)
        else:
            user.subs = [sub]
        await user.save()
        logger.info(f"Created a new sub for {user}: {sub}.")
        next_charge = count_next_charge(last_charge, data["period"])
        await message.reply(
            f"Done! Added a new subscription: <b>{data['name']}</b> ({data['amount']} / {data['period']}). "
            f"Will be charged <b>{next_charge.strftime('%d.%m.%Y')}</b>.\n\n"
            f"I will notify you as the date approaches. Type /all to see all subscriptions.",
            parse_mode="HTML",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await state.finish()


@dp.message_handler(commands="all")
async def handle_all(message: types.Message):
    user = await User.find_one(User.user_id == message.from_user.id)
    if not user.subs:
        await message.reply(cliche.YOU_DO_NOT_HAVE_ANY_SUBS)
        return
    response = "<b>Your subscriptions:</b>\n"
    today = datetime.today()
    for sub in user.subs:
        next_charge = count_next_charge(sub.last_charge, sub.period)
        days_left = (next_charge - today).days
        response += f"- <b>{sub.name}</b> ({sub.amount} / {sub.period}): {next_charge.strftime('%d.%m.%Y')} ({days_left} {'days' if days_left > 1 else 'day'} left)\n"
    response += "\nType /remove to remove subscriptions."
    await message.reply(response, parse_mode="HTML")


@dp.message_handler(commands="remove")
async def handle_remove(message: types.Message):
    user = await User.find_one(User.user_id == message.from_user.id)
    if not user.subs:
        await message.reply(cliche.YOU_DO_NOT_HAVE_ANY_SUBS)
        return

    reply_markup = generate_remove_sub_inline_keyboard(message.message_id, user.subs)
    await message.reply(
        "Select subscription you want to remove:", reply_markup=reply_markup
    )


@dp.callback_query_handler()
async def inline_keyboard_handler(query: types.CallbackQuery):
    data = ujson.loads(query.data)
    command = data["command"]
    edit_message_id = data["edit_message_id"]

    match command:
        case "remove_sub":
            i = data["sub_index"]
            user = await User.find_one(User.user_id == query.from_user.id)
            if i < len(user.subs):
                sub = user.subs.pop(i)
                await user.save()
                await query.answer(
                    f"{sub.name} has been removed from your subscriptions list."
                )
                reply_markup = generate_remove_sub_inline_keyboard(
                    edit_message_id - 1, user.subs
                )
                await bot.edit_message_reply_markup(
                    chat_id=query.from_user.id,
                    message_id=edit_message_id,
                    reply_markup=reply_markup,
                )
                if not user.subs:
                    await bot.edit_message_text(
                        cliche.YOU_DO_NOT_HAVE_ANY_SUBS,
                        chat_id=query.from_user.id,
                        message_id=edit_message_id,
                    )
                return
            else:
                logger.warning(
                    f"Invalid callback query (sub_index >= subs count): {data}."
                )
        case _:
            logger.warning(f"Invalid callback query (unknown command): {data}.")
    await query.answer("Oops, something went wrong. Try again later.")


dp.middleware.setup(DatabaseMiddleware())
logger.info("Bot is running.")
executor.start_polling(dp, skip_updates=True)
