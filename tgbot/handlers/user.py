from aiogram import Router, Bot, types
from aiogram.filters import Command, Text, StateFilter
from aiogram.types import Message, FSInputFile
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from magic_filter import F
from aiogram.filters.callback_data import CallbackData

from tgbot.misc.big_text import achievements
from tgbot.misc.functions import auth_status, sql_fetchone_with_args, sql_fetchone,\
    sql_with_args, check_last_achievement
from tgbot.keyboards.textBtn import home_keyboard, random_word_kb, der_die_das_kb, next_or_menu_kb
from tgbot.keyboards.inlineBtn import choose_lang_keyboard, achievements_category


import time
import datetime
import requests
import asyncio

from tgbot.misc.states import RandomWordState, ArticlesState
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
            await sql_with_args('INSERT INTO "users" (id, name, username) VALUES (%s,%s,%s)',
                                (user_id, name, user_name))
            await bot.send_message(user_id, 'Please select a language for translation',
                                   reply_markup=keyboard.as_markup())
        except():
            await bot.send_message(user_id, 'Registration failed. Contact Support')


@user_router.callback_query(lambda c: c.data == "ru")
async def ru_language(c: types.CallbackQuery):
    user_id = c.from_user.id
    await sql_with_args('UPDATE "users" SET lang = %s WHERE id = %s', ("ru", user_id))
    await c.message.delete()
    await c.answer("Язык был обновлён")
    await bot.send_message(user_id, "Hello! Are you ready to play and learn german?😉",
                           reply_markup=home_keyboard().as_markup(resize_keyboard=True))


@user_router.callback_query(lambda c: c.data == "ua")
async def ua_language(c: types.CallbackQuery):
    user_id = c.from_user.id
    await sql_with_args('UPDATE "users" SET lang = %s WHERE id = %s', ("ua", user_id))
    await c.message.delete()
    await c.answer("Мова була змінена")
    await bot.send_message(user_id, "Hello! Are you ready to play and learn german?😉",
                           reply_markup=home_keyboard().as_markup(resize_keyboard=True))


@user_router.callback_query(lambda c: c.data == "en")
async def en_language(c: types.CallbackQuery):
    user_id = c.from_user.id
    await sql_with_args('UPDATE "users" SET lang = %s WHERE id = %s', ("en", user_id))
    await c.message.delete()
    await c.answer("Language has been changed")
    await bot.send_message(user_id, "Hello! Are you ready to play and learn german?😉",
                           reply_markup=home_keyboard().as_markup(resize_keyboard=True))


@user_router.message(Command('menu'))
async def back_to_main_menu(m: Message, state: FSMContext):
    await state.clear()
    await m.answer("You have reached the main menu",
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
    await check_last_achievement(user_id)
    cur_achieve = await sql_fetchone_with_args('SELECT last_achievement FROM "users" WHERE id = %s', (user_id,))
    correct_answers = await sql_fetchone_with_args('SELECT correct_answers FROM "users" WHERE id = %s', (user_id,))
    await c.message.delete()
    await bot.send_message(user_id, f'Achievements of the category "participle": \n\n'
                                    f'{achievements[cur_achieve[0]]}'
                                    f'\n\nYour amount of the correct answers now: {correct_answers[0]}')


@user_router.callback_query(lambda c: c.data == "articles")
async def participle_achievements(c: types.CallbackQuery):
    user_id = c.from_user.id
    await check_last_achievement(user_id)
    cur_achieve = await sql_fetchone_with_args('SELECT last_achievement FROM "users" WHERE id = %s', (user_id,))
    correct_answers = await sql_fetchone_with_args('SELECT correct_answers FROM "users" WHERE id = %s', (user_id,))
    await c.message.delete()
    await bot.send_message(user_id, f'Achievements of the category "articles": \n\n'
                                    f'{achievements[cur_achieve[0]]}'
                                    f'\n\nYour amount of the correct answers now: {correct_answers[0]}')


@user_router.callback_query(lambda c: c.data == "plural")
async def participle_achievements(c: types.CallbackQuery):
    user_id = c.from_user.id
    await check_last_achievement(user_id)
    cur_achieve = await sql_fetchone_with_args('SELECT last_achievement FROM "users" WHERE id = %s', (user_id,))
    correct_answers = await sql_fetchone_with_args('SELECT correct_answers FROM "users" WHERE id = %s', (user_id,))
    await c.message.delete()
    await bot.send_message(user_id, f'Achievements of the category "plural": \n\n'
                                    f'{achievements[cur_achieve[0]]}'
                                    f'\n\nYour amount of the correct answers now: {correct_answers[0]}')


@user_router.message(Text("Random word"))
async def bt_random_word(m: Message, state: FSMContext):
    await m.answer("Choose a part of speech", reply_markup=random_word_kb().as_markup(resize_keyboard=True))
    await state.set_state(RandomWordState.button)


@user_router.message(Text("Menu"), RandomWordState.button)
async def bt_main_menu(m: Message, state: FSMContext):
    await m.answer("You have reached the main menu", reply_markup=home_keyboard().as_markup(resize_keyboard=True))
    await state.clear()


@user_router.message(Text("Noun"), RandomWordState.button)
async def random_word_noun(m: Message, state: FSMContext):
    noun = await sql_fetchone("select noun_single_ger from nouns order by random() limit 1")
    await m.answer(f"Random noun: <b>{noun[0]}</b>", reply_markup=random_word_kb().as_markup(resize_keyboard=True))
    await state.set_state(RandomWordState.button)


@user_router.message(Text("Articles"))
@user_router.message(Text("next"), ArticlesState.next_or_menu)
async def bt_articles(m: Message, state: FSMContext):
    fetch = None
    user_lang = await sql_fetchone_with_args('SELECT lang FROM "users" WHERE id = %s', (m.from_user.id,))
    if user_lang[0] == "ru":
        fetch = await sql_fetchone("select noun_single_ger, article, noun_single_rus "
                                   "from nouns "
                                   "order by random() limit 1")
    elif user_lang[0] == "ua":
        fetch = await sql_fetchone("select noun_single_ger, article, noun_single_ukr "
                                   "from nouns "
                                   "order by random() limit 1")
    elif user_lang[0] == "en":
        fetch = await sql_fetchone("select noun_single_ger, article, noun_single_eng "
                                   "from nouns "
                                   "order by random() limit 1")
    await state.update_data(noun=fetch[0])
    await state.update_data(article=fetch[1])
    await state.update_data(translate=fetch[2])
    await m.answer(f"Choose article for <b>{fetch[0]}</b>",
                   reply_markup=der_die_das_kb().as_markup(resize_keyboard=True))
    await state.set_state(ArticlesState.answer)


@user_router.message(F.text.in_({'der', 'die', 'das'}), ArticlesState.answer)
async def choose_article(m: Message, state: FSMContext):
    user_article = m.text
    data = await state.get_data()
    if user_article == data['article']:
        await m.answer(f"✅ Correct! <b>{user_article} {data['noun']}</b>.\n"
                       f"Translation: <b><i>{data['translate']}</i></b>",
                       reply_markup=next_or_menu_kb().as_markup(resize_keyboard=True))
    else:
        await m.answer(f"❌ Wrong!\n"
                       f"Correct: <b>{data['article']} {data['noun']}</b>.\n"
                       f"Translation: <b><i>{data['translate']}</i></b>",
                       reply_markup=next_or_menu_kb().as_markup(resize_keyboard=True))
    await state.set_state(ArticlesState.next_or_menu)


@user_router.message(Text("menu"), ArticlesState.next_or_menu)
async def back_to_menu_from_article(m: Message, state: FSMContext):
    await state.clear()
    await m.answer("You have reached the main menu",
                   reply_markup=home_keyboard().as_markup(resize_keyboard=True))
















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
