from aiogram import Bot
from tgbot.config import load_config

import psycopg2

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


async def sql_fetchone_with_args(query: str, args: tuple):
    cur, base = base_start()
    cur.execute(query, args)
    data = cur.fetchone()
    base.commit()
    cur.close()
    base.close()
    return data


async def sql_fetchone(query: str):
    cur, base = base_start()
    cur.execute(query)
    data = cur.fetchone()
    base.commit()
    cur.close()
    base.close()
    return data


async def sql_with_args(query: str, args: tuple):
    cur, base = base_start()
    cur.execute(query, args)
    base.commit()
    cur.close()
    base.close()


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


async def check_last_achievement(user_id, correct, category):
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

    if category == "plural":
        await sql_with_args('UPDATE "users" SET "last_achievement_plural" = %s WHERE id = %s',
                            (last, user_id))
    elif category == "articles":
        await sql_with_args('UPDATE "users" SET "last_achievement_articles" = %s WHERE id = %s',
                            (last, user_id))
    elif category == "perfect":
        await sql_with_args('UPDATE "users" SET "last_achievement_perfect" = %s WHERE id = %s',
                            (last, user_id))
