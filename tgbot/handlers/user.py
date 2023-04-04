from aiogram import Router, Bot, types
from aiogram.filters import Command, Text, StateFilter
from aiogram.types import Message, FSInputFile
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from magic_filter import F
from aiogram.filters.callback_data import CallbackData

from tgbot.misc.big_text import achievements
from tgbot.misc.functions import auth_status, add_user, get_lang, base_start, get_last_achievements, get_correct_answers
from tgbot.keyboards.textBtn import home_keyboard
from tgbot.keyboards.inlineBtn import choose_lang_keyboard, achievements_category


import time
import datetime
import requests
import asyncio

from tgbot.services.del_message import delete_message

from tgbot.keyboards.inlineBtn import CastomCallback
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext


import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

user_router = Router()
config = load_config(".env")

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


# handler for commands
@user_router.message(Command("start"))
async def user_start(m: Message):
    user_id = m.from_user.id
    user_name = m.from_user.username
    name = m.from_user.first_name
    auth = await auth_status(user_id)
    keyboard = choose_lang_keyboard()
    if auth:
        await bot.send_message(user_id, 'Please select a language for translation',
                               reply_markup=keyboard.as_markup())
    else:
        await bot.send_message(user_id, 'You are not registered in the bot')
        await bot.send_message(user_id, 'Attempt to register in the database....')
        try:
            await add_user(user_id, user_name, name)
            await bot.send_message(user_id, 'Please select a language for translation',
                                   reply_markup=keyboard.as_markup())
        except():
            await bot.send_message(user_id, 'Registration failed. Contact Support')


@user_router.callback_query(lambda c: c.data == "ru")
async def ru_language(c: types.CallbackQuery):
    cur, base = base_start()
    user_id = c.from_user.id
    cur.execute('UPDATE "users" SET lang = %s WHERE id = %s', ("ru", user_id))
    base.commit()
    cur.close()
    base.close()
    await c.message.delete()
    await c.answer("Язык был обновлён")
    await bot.send_message(user_id, "Hello! Are you ready to play and learn german?😉",
                           reply_markup=home_keyboard().as_markup(resize_keyboard=True))


@user_router.callback_query(lambda c: c.data == "ua")
async def ua_language(c: types.CallbackQuery):
    cur, base = base_start()
    user_id = c.from_user.id
    cur.execute('UPDATE "users" SET lang = %s WHERE id = %s', ("ua", user_id))
    base.commit()
    cur.close()
    base.close()
    await c.message.delete()
    await c.answer("Мова була змінена")
    await bot.send_message(user_id, "Hello! Are you ready to play and learn german?😉",
                           reply_markup=home_keyboard().as_markup(resize_keyboard=True))


@user_router.callback_query(lambda c: c.data == "en")
async def en_language(c: types.CallbackQuery):
    cur, base = base_start()
    user_id = c.from_user.id
    cur.execute('UPDATE "users" SET lang = %s WHERE id = %s', ("en", user_id))
    base.commit()
    cur.close()
    base.close()
    await c.message.delete()
    await c.answer("Language has been changed")
    await bot.send_message(user_id, "Hello! Are you ready to play and learn german?😉",
                           reply_markup=home_keyboard().as_markup(resize_keyboard=True))


@user_router.message(Text('Achievements'))
async def bt_achievements(m: Message):
    user_id = m.from_user.id
    kb = achievements_category()
    await bot.send_message(user_id, "Choose a category",
                           reply_markup=kb.as_markup())


@user_router.callback_query(lambda c: c.data == "participle")
async def participle_achievements(c: types.CallbackQuery):
    user_id = c.from_user.id
    cur_achieve = await get_last_achievements(user_id)
    correct_answers = await get_correct_answers(user_id)
    await c.message.delete()
    await bot.send_message(user_id, f'Achievements of the category "participle": \n\n'
                                    f'{achievements[cur_achieve]}'
                                    f'\n\nYour amount of the correct answers now: {correct_answers}')


@user_router.callback_query(lambda c: c.data == "articles")
async def participle_achievements(c: types.CallbackQuery):
    user_id = c.from_user.id
    cur_achieve = await get_last_achievements(user_id)
    correct_answers = await get_correct_answers(user_id)
    await c.message.delete()
    await bot.send_message(user_id, f'Achievements of the category "articles": \n\n'
                                    f'{achievements[cur_achieve]}'
                                    f'\n\nYour amount of the correct answers now: {correct_answers}')


@user_router.callback_query(lambda c: c.data == "plural")
async def participle_achievements(c: types.CallbackQuery):
    user_id = c.from_user.id
    cur_achieve = await get_last_achievements(user_id)
    correct_answers = await get_correct_answers(user_id)
    await c.message.delete()
    await bot.send_message(user_id, f'Achievements of the category "plural": \n\n'
                                    f'{achievements[cur_achieve]}'
                                    f'\n\nYour amount of the correct answers now: {correct_answers}')

















# @user_router.message(F.text.in_({'Achievements', 'Досягнення', 'Достижения', 'achievements', 'досягнення', 'достижения'}))
# async def bt_achievements(m: types.Message, state: FSMContext):
#     user_id = m.from_user.id
#     lang = await check_lang(user_id)
#     if lang == "en":
#         await bot.send_message(user_id, "Choose a category", reply_markup=achievements_category())
#     elif lang == "ua":
#         await bot.send_message(user_id, "Оберіть категорію", reply_markup=achievements_category())
#     elif lang == "ru":
#         await bot.send_message(user_id, "Выберите категорию", reply_markup=achievements_category())











# version for some text messages
# @user_router.message(F.text.in_({'Покупка акаунтов бирж', 'Покупка кошелька Юмани'}))
