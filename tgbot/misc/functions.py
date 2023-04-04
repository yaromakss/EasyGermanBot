from aiogram import Router, Bot, types
from aiogram.types import Message, FSInputFile
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

import datetime
import asyncio

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
# bot2 = Bot(token=config.tg_bot.token2, parse_mode="HTML")


def base_start():
    base = psycopg2.connect(
        dbname=config.db.database,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,
    )
    cur = base.cursor()
    return cur, base


async def auth_status(user_id):
    cur, base = base_start()

    user_id = str(user_id)
    cur.execute('SELECT * FROM "users"')
    users = cur.fetchall()
    answer = False
    for user in users:
        if str(user[0]) == user_id:
            answer = True
    base.commit()
    cur.close()
    base.close()
    return answer


async def add_user(user_id, user_name, name):
    cur, base = base_start()

    data = (user_id, name, user_name)
    cur.execute('INSERT INTO "users" (id, name, username) VALUES (%s,%s,%s)', data)
    base.commit()
    cur.close()
    base.close()


async def get_lang(user_id):
    cur, base = base_start()

    cur.execute('SELECT lang FROM "users" WHERE id = %s', (user_id,))
    lang = cur.fetchone()
    base.commit()
    cur.close()
    base.close()
    return lang[0]


async def get_last_achievements(user_id):
    await check_last_achievement(user_id)
    cur, base = base_start()
    cur.execute('SELECT last_achievement FROM "users" WHERE id = %s', (user_id,))
    achive = cur.fetchone()
    base.commit()
    cur.close()
    base.close()
    return achive[0]


async def get_correct_answers(user_id):
    cur, base = base_start()
    cur.execute('SELECT correct_answers FROM "users" WHERE id = %s', (user_id,))
    answ = cur.fetchone()
    base.commit()
    cur.close()
    base.close()
    return answ[0]


async def check_last_achievement(user_id):
    cur, base = base_start()
    cur.execute('SELECT correct_answers FROM "users" WHERE id = %s', (user_id,))
    correct = cur.fetchone()[0]
    last = 0
    if correct < 10:
        last = 0
    elif correct < 100:
        last = 1
    elif correct < 500:
        last = 2
    elif correct < 1000:
        last = 3
    elif correct < 3000:
        last = 4
    elif correct < 5000:
        last = 5
    elif correct < 10000:
        last = 6
    elif correct >= 10000:
        last = 7
    cur.execute('UPDATE "users" SET "last_achievement" = %s WHERE id = %s', (last, user_id))
    base.commit()
    cur.close()
    base.close()
    print(f'last: {last}')
