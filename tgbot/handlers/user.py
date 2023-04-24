from aiogram import Router, Bot, types
from aiogram.filters import Command, Text
from aiogram.types import Message
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext
from magic_filter import F

from tgbot.misc.big_text import achievements
from tgbot.misc.functions import auth_status, sql_fetchone_with_args, sql_fetchone,\
    sql_with_args, check_last_achievement
from tgbot.keyboards.textBtn import home_keyboard, random_word_kb, der_die_das_kb, next_or_menu_kb, idk_plural_kb
from tgbot.keyboards.inlineBtn import choose_lang_keyboard, achievements_category

from tgbot.misc.states import RandomWordState, ArticlesState, PluralState, PerfectState

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


@user_router.message(Command('admin'))
async def user_cannot_be_an_admin(m: Message):
    await m.answer("Insufficient access rights",
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


@user_router.callback_query(lambda c: c.data == "perfect")
async def perfect_achievements(c: types.CallbackQuery):
    user_id = c.from_user.id
    correct = await sql_fetchone_with_args('SELECT correct_answ_perfect FROM "users" WHERE id = %s',
                                           (user_id,))
    await check_last_achievement(user_id, correct[0], "perfect")
    cur_achieve = await sql_fetchone_with_args('SELECT last_achievement_perfect FROM "users" WHERE id = %s',
                                               (user_id,))
    correct_answers = await sql_fetchone_with_args('SELECT correct_answ_perfect FROM "users" WHERE id = %s',
                                                   (user_id,))
    await c.message.delete()
    await bot.send_message(user_id, f'Achievements of the category "Participle II": \n\n'
                                    f'{achievements[cur_achieve[0]]}'
                                    f'\n\nYour amount of the correct answers now: <b>{correct_answers[0]}</b>')
    if correct_answers[0] >= 10000:
        await bot.send_message(user_id, "Congratulations! All achievements has been opened! 🎉🎉🎉")
        await bot.send_message(user_id, '🎉')


@user_router.callback_query(lambda c: c.data == "articles")
async def articles_achievements(c: types.CallbackQuery):
    user_id = c.from_user.id
    correct = await sql_fetchone_with_args('SELECT correct_answ_articles FROM "users" WHERE id = %s',
                                           (user_id,))
    await check_last_achievement(user_id, correct[0], "articles")
    cur_achieve = await sql_fetchone_with_args('SELECT last_achievement_articles FROM "users" WHERE id = %s',
                                               (user_id,))
    correct_answers = await sql_fetchone_with_args('SELECT correct_answ_articles FROM "users" WHERE id = %s',
                                                   (user_id,))
    await c.message.delete()
    await bot.send_message(user_id, f'Achievements of the category "Articles": \n\n'
                                    f'{achievements[cur_achieve[0]]}'
                                    f'\n\nYour amount of the correct answers now: <b>{correct_answers[0]}</b>')
    if correct_answers[0] >= 10000:
        await bot.send_message(user_id, "Congratulations! All achievements has been opened! 🎉🎉🎉")
        await bot.send_message(user_id, '🎉')


@user_router.callback_query(lambda c: c.data == "plural")
async def plural_achievements(c: types.CallbackQuery):
    user_id = c.from_user.id
    correct = await sql_fetchone_with_args('SELECT correct_answ_plural FROM "users" WHERE id = %s',
                                           (user_id,))
    await check_last_achievement(user_id, correct[0], "plural")
    cur_achieve = await sql_fetchone_with_args('SELECT last_achievement_plural FROM "users" WHERE id = %s',
                                               (user_id,))
    correct_answers = await sql_fetchone_with_args('SELECT correct_answ_plural FROM "users" WHERE id = %s',
                                                   (user_id,))
    await c.message.delete()
    await bot.send_message(user_id, f'Achievements of the category "Plural": \n\n'
                                    f'{achievements[cur_achieve[0]]}'
                                    f'\n\nYour amount of the correct answers now: <b>{correct_answers[0]}</b>')
    if correct_answers[0] >= 10000:
        await bot.send_message(user_id, "Congratulations! All achievements has been opened! 🎉🎉🎉")
        await bot.send_message(user_id, '🎉')



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


@user_router.message(Text("Verb"), RandomWordState.button)
async def random_word_noun(m: Message, state: FSMContext):
    noun = await sql_fetchone("select verb_ger_inf from verbs order by random() limit 1")
    await m.answer(f"Random verb: <b>{noun[0]}</b>", reply_markup=random_word_kb().as_markup(resize_keyboard=True))
    await state.set_state(RandomWordState.button)


@user_router.message(Text("Adjectives"), RandomWordState.button)
async def random_word_noun(m: Message, state: FSMContext):
    noun = await sql_fetchone("select adj_ger from adjectives order by random() limit 1")
    await m.answer(f"Random adjectives: <b>{noun[0]}</b>",
                   reply_markup=random_word_kb().as_markup(resize_keyboard=True))
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
    user_id = m.from_user.id
    if user_article == data['article']:
        await m.answer(f"✅ Correct! <b>{user_article} {data['noun']}</b>.\n"
                       f"Translation: <b><i>{data['translate']}</i></b>",
                       reply_markup=next_or_menu_kb().as_markup(resize_keyboard=True))
        await sql_with_args('UPDATE "users" SET "correct_answ_articles" = "correct_answ_articles" + 1 WHERE id = %s',
                            (user_id,))
    else:
        await m.answer(f"❌ Wrong!\n\n"
                       f"Correct: <b>{data['article']} {data['noun']}</b>.\n"
                       f"Translation: <b><i>{data['translate']}</i></b>",
                       reply_markup=next_or_menu_kb().as_markup(resize_keyboard=True))
    await state.set_state(ArticlesState.next_or_menu)


@user_router.message(Text("menu"), ArticlesState.next_or_menu)
async def back_to_menu_from_article(m: Message, state: FSMContext):
    await state.clear()
    await m.answer("You have reached the main menu",
                   reply_markup=home_keyboard().as_markup(resize_keyboard=True))


@user_router.message(Text("Plural"))
@user_router.message(Text("next"), PluralState.next_or_menu)
async def bt_plural(m: Message, state: FSMContext):
    fetch = None
    user_lang = await sql_fetchone_with_args('SELECT lang FROM "users" WHERE id = %s', (m.from_user.id,))
    if user_lang[0] == "ru":
        fetch = await sql_fetchone("select noun_single_ger, article, noun_plural_ger, noun_single_rus, noun_plural_rus "
                                   "from nouns "
                                   "order by random() limit 1")
    elif user_lang[0] == "ua":
        fetch = await sql_fetchone("select noun_single_ger, article, noun_plural_ger, noun_single_ukr, noun_plural_ukr "
                                   "from nouns "
                                   "order by random() limit 1")
    elif user_lang[0] == "en":
        fetch = await sql_fetchone("select noun_single_ger, article, noun_plural_ger, noun_single_eng, noun_plural_eng "
                                   "from nouns "
                                   "order by random() limit 1")
    await state.update_data(s_ger=fetch[0])
    await state.update_data(article=fetch[1])
    await state.update_data(p_ger=fetch[2])
    await state.update_data(s_trans=fetch[3].capitalize())
    await state.update_data(p_trans=fetch[4].capitalize())
    await m.answer(f"Write the plural form of the verb <b><u>with article</u></b>\n"
                   f"Random noun - <b>{fetch[1]} {fetch[0]}</b>",
                   reply_markup=idk_plural_kb().as_markup(resize_keyboard=True))
    await state.set_state(PluralState.answer)


@user_router.message(Text('i don`t know'), PluralState.answer)
async def idk_in_plural(m: Message, state: FSMContext):
    data = await state.get_data()
    await m.answer(f"{data['article']} {data['s_ger']} - <b>die {data['p_ger']}</b>\n"
                   f"Translation: <b><i>{data['s_trans']} - {data['p_trans']}</i></b>",
                   reply_markup=next_or_menu_kb().as_markup(resize_keyboard=True))
    await state.set_state(PluralState.next_or_menu)


@user_router.message(Text, PluralState.answer)
async def write_plural_for_noun(m: Message, state: FSMContext):
    data = await state.get_data()
    user_answer = m.text.lower()
    user_id = m.from_user.id
    if user_answer.strip() == f"die {data['p_ger'].lower()}":
        await m.answer(f"✅ Correct!\n\n"
                       f"{data['article']} {data['s_ger']} - <b>die {data['p_ger']}</b>\n"
                       f"Translation: <b><i>{data['s_trans']} - {data['p_trans']}</i></b>",
                       reply_markup=next_or_menu_kb().as_markup(resize_keyboard=True))
        await sql_with_args('UPDATE "users" SET "correct_answ_plural" = "correct_answ_plural" + 1 WHERE id = %s',
                            (user_id,))
    else:
        await m.answer(f"❌ Wrong!\n\n"
                       f"Correct:\n"
                       f"{data['article']} {data['s_ger']} - <b>die {data['p_ger']}</b>\n"
                       f"Translation: <b><i>{data['s_trans']} - {data['p_trans']}</i></b>",
                       reply_markup=next_or_menu_kb().as_markup(resize_keyboard=True))
    await state.set_state(PluralState.next_or_menu)


@user_router.message(Text("menu"), PluralState.next_or_menu)
async def back_to_menu_from_plural(m: Message, state: FSMContext):
    await state.clear()
    await m.answer("You have reached the main menu",
                   reply_markup=home_keyboard().as_markup(resize_keyboard=True))









@user_router.message(Text("Participle II (Perfect)"))
@user_router.message(Text("next"), PerfectState.next_or_menu)
async def bt_perfect(m: Message, state: FSMContext):
    fetch = None
    user_lang = await sql_fetchone_with_args('SELECT lang FROM "users" WHERE id = %s', (m.from_user.id,))
    if user_lang[0] == "ru":
        fetch = await sql_fetchone("select verb_ger_inf, verb_ger_past, verb_ger_perfect, verb_rus "
                                   "from verbs "
                                   "order by random() limit 1")
    elif user_lang[0] == "ua":
        fetch = await sql_fetchone("select verb_ger_inf, verb_ger_past, verb_ger_perfect, verb_ukr "
                                   "from verbs "
                                   "order by random() limit 1")
    elif user_lang[0] == "en":
        fetch = await sql_fetchone("select verb_ger_inf, verb_ger_past, verb_ger_perfect, verb_eng "
                                   "from verbs "
                                   "order by random() limit 1")
    await state.update_data(ger_inf=fetch[0])
    await state.update_data(ger_past=fetch[1])
    await state.update_data(ger_perf=fetch[2])
    await state.update_data(verb_trans=fetch[3])
    await m.answer(f"Write this word in Participle II:\n"
                   f"Random verb - <b>{fetch[0]}</b>",
                   reply_markup=idk_plural_kb().as_markup(resize_keyboard=True))
    await state.set_state(PerfectState.answer)


@user_router.message(Text('i don`t know'), PerfectState.answer)
async def idk_in_perfect(m: Message, state: FSMContext):
    data = await state.get_data()
    await m.answer(f"3 forms of verb:\n"
                   f"{data['ger_inf']}\n"
                   f"{data['ger_past']}\n"
                   f"<b>{data['ger_perf']}</b>\n\n"
                   f"Translate: <b>{data['verb_trans']}</b>",
                   reply_markup=next_or_menu_kb().as_markup(resize_keyboard=True))
    await state.set_state(PerfectState.next_or_menu)


@user_router.message(Text, PerfectState.answer)
async def write_in_perfect_form(m: Message, state: FSMContext):
    data = await state.get_data()
    user_answer = m.text.lower()
    user_id = m.from_user.id
    if user_answer.strip() == f"{data['ger_perf'].lower()}":
        await m.answer(f"✅ Correct!\n\n"
                       f"3 forms of verb:\n"
                       f"{data['ger_inf']}\n"
                       f"{data['ger_past']}\n"
                       f"<b>{data['ger_perf']}</b>\n\n"
                       f"Translate: <b>{data['verb_trans']}</b>",
                       reply_markup=next_or_menu_kb().as_markup(resize_keyboard=True))
        await sql_with_args('UPDATE "users" SET "correct_answ_perfect" = "correct_answ_perfect" + 1 WHERE id = %s',
                            (user_id,))
    else:
        await m.answer(f"❌ Wrong!\n\n"
                       f"Correct:\n"
                       f"3 forms of verb:\n"
                       f"{data['ger_inf']}\n"
                       f"{data['ger_past']}\n"
                       f"<b>{data['ger_perf']}</b>\n\n"
                       f"Translate: <b>{data['verb_trans']}</b>",
                       reply_markup=next_or_menu_kb().as_markup(resize_keyboard=True))
    await state.set_state(PerfectState.next_or_menu)


@user_router.message(Text("menu"), PerfectState.next_or_menu)
async def back_to_menu_from_perfect(m: Message, state: FSMContext):
    await state.clear()
    await m.answer("You have reached the main menu",
                   reply_markup=home_keyboard().as_markup(resize_keyboard=True))
