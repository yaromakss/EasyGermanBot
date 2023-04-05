from aiogram import Router, Bot, types
from aiogram.types import Message, FSInputFile
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from magic_filter import F

import time
import datetime
import requests
import asyncio

from tgbot.keyboards.adminInlineBtn import noun_correct_kb
from tgbot.keyboards.adminTextBtn import admin_action_keyboard, admin_der_die_das
from tgbot.misc.admin_states import AddNoun
from tgbot.misc.functions import base_start
from tgbot.services.del_message import delete_message

from tgbot.keyboards.inlineBtn import CastomCallback
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from aiogram.filters import Command, Text
from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


@admin_router.message(Command('admin'))
async def admin_start(m: Message):
    await m.reply("Вітаю, адміне!")
    await m.answer("Please, choose action", reply_markup=admin_action_keyboard().as_markup(resize_keyboard=True))


@admin_router.message(Text('Users'))
async def bt_achievements(m: Message):
    cur, base = base_start()
    cur.execute('SELECT count(*) FROM "users"')
    amount = cur.fetchone()
    await m.answer(f"currently registered users in the bot: {amount[0]}")
    base.commit()
    cur.close()
    base.close()


@admin_router.message(Text('Add noun'))
async def bt_add_noun(m: Message, state: FSMContext):
    await m.answer(f"Write the noun (without article)", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddNoun.write_noun)


@admin_router.message(Text, AddNoun.write_noun)
async def get_noun(m: Message, state: FSMContext):
    noun = m.text
    await state.update_data(noun=noun)
    await m.answer("Good! Please, choose the article",
                   reply_markup=admin_der_die_das().as_markup(resize_keyboard=True))
    await state.set_state(AddNoun.choose_article)


@admin_router.message(Text, AddNoun.choose_article)
async def choose_article(m: Message, state: FSMContext):
    article = m.text
    if article not in ['der', 'die', 'das']:
        await m.answer("Please use navigation buttons!",
                       reply_markup=admin_der_die_das().as_markup(resize_keyboard=True))
        await state.set_state(AddNoun.choose_article)
    else:
        await state.update_data(article=article)
        await m.answer("Alright. Now, write plural form of the noun (without article)",
                       reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AddNoun.plural)


@admin_router.message(Text, AddNoun.plural)
async def plural_form(m: Message, state: FSMContext):
    plural = m.text
    await state.update_data(plural=plural)
    await m.answer("Good! Please write a translation for <b>English</b> in <b>Single</b>")
    await state.set_state(AddNoun.sing_eng)


@admin_router.message(Text, AddNoun.sing_eng)
async def en_translation(m: Message, state: FSMContext):
    english = m.text
    await state.update_data(s_eng=english)
    await m.answer("Good! Please write a translation for <b>English</b> in <b>Plural</b>")
    await state.set_state(AddNoun.plural_eng)


@admin_router.message(Text, AddNoun.plural_eng)
async def en_translation(m: Message, state: FSMContext):
    english = m.text
    await state.update_data(p_eng=english)
    await m.answer("Good! Please write a translation for <b>Ukrainian</b> in <b>Single</b>")
    await state.set_state(AddNoun.sing_ukr)


@admin_router.message(Text, AddNoun.sing_ukr)
async def en_translation(m: Message, state: FSMContext):
    ukrainian = m.text
    await state.update_data(s_ukr=ukrainian)
    await m.answer("Good! Please write a translation for <b>Ukrainian</b> in <b>Plural</b>")
    await state.set_state(AddNoun.plural_ukr)


@admin_router.message(Text, AddNoun.plural_ukr)
async def uk_translation(m: Message, state: FSMContext):
    ukrainian = m.text
    await state.update_data(p_ukr=ukrainian)
    await m.answer("Good! Please write a translation for <b>Russian</b> in <b>Single</b>")
    await state.set_state(AddNoun.sing_rus)


@admin_router.message(Text, AddNoun.sing_rus)
async def uk_translation(m: Message, state: FSMContext):
    russian = m.text
    await state.update_data(s_rus=russian)
    await m.answer("Good! Please write a translation for <b>Russian</b> in <b>Plural</b>")
    await state.set_state(AddNoun.plural_rus)


@admin_router.message(Text, AddNoun.plural_rus)
async def ru_translation(m: Message, state: FSMContext):
    russian = m.text
    await state.update_data(p_rus=russian)
    data = await state.get_data()
    await m.answer(f"Perfect! Check if everything is written correctly:\n\n"
                   f"noun: {data['noun']}\n"
                   f"article: {data['article']}\n"
                   f"plural: {data['plural']}\n"
                   f"sing_eng: {data['s_eng']}\n"
                   f"plural_eng: {data['p_eng']}\n"
                   f"sing_ukr: {data['s_ukr']}\n"
                   f"plural_ukr: {data['p_ukr']}\n"
                   f"sing_rus: {data['s_rus']}\n"
                   f"plural_rus: {data['p_rus']}",
                   reply_markup=noun_correct_kb().as_markup(resize_keyboard=True))


@admin_router.callback_query(lambda c: c.data == "noun_correct")
async def noun_correct(c: types.CallbackQuery, state: FSMContext):
    user_id = c.from_user.id
    await c.message.delete()
    cur, base = base_start()
    data = await state.get_data()
    cur.execute('INSERT INTO "nouns" (article,'
                ' noun_single_ger,'
                ' noun_plural_ger,'
                ' noun_single_eng,'
                ' noun_plural_eng,'
                ' noun_single_ukr,'
                ' noun_plural_ukr,'
                ' noun_single_rus,'
                ' noun_plural_rus) VALUES (%s, %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s)', (data['article'],
                                                                                         data['noun'],
                                                                                         data['plural'],
                                                                                         data['s_eng'],
                                                                                         data['p_eng'],
                                                                                         data['s_ukr'],
                                                                                         data['p_ukr'],
                                                                                         data['s_rus'],
                                                                                         data['p_rus'],))
    await state.clear()
    base.commit()
    cur.close()
    base.close()
    await bot.send_message(user_id, "Congratulations! New word has been added",
                           reply_markup=admin_action_keyboard().as_markup(resize_keyboard=True))


@admin_router.callback_query(lambda c: c.data == "noun_incorrect")
async def noun_incorrect(c: types.CallbackQuery, state: FSMContext):
    user_id = c.from_user.id
    await c.message.delete()
    await state.clear()
    await bot.send_message(user_id, "You have reached the main menu")
    await bot.send_message(user_id,
                           "Okay. Please, choose action",
                           reply_markup=admin_action_keyboard().as_markup(resize_keyboard=True))


@admin_router.message(Command('menu'), State('*'))
async def back_to_menu(m: Message, state: FSMContext):
    await state.clear()
    await m.answer("You have reached the main menu")
    await m.answer("Okay. Please, choose action",
                   reply_markup=admin_action_keyboard().as_markup(resize_keyboard=True))

