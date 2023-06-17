from aiogram import Router, Bot, types
from aiogram.types import Message
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext

from tgbot.keyboards.adminInlineBtn import noun_correct_kb, adj_correct_kb, verb_correct_kb
from tgbot.keyboards.adminTextBtn import admin_action_keyboard, admin_der_die_das
from tgbot.keyboards.textBtn import home_keyboard
from tgbot.misc.admin_states import AddNoun, AddAdjectives, AddVerb
from tgbot.misc.functions import sql_with_args, sql_fetchone

from aiogram.filters import Command, Text
from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


@admin_router.message(Command('admin'))
async def admin_start(m: Message):
    await m.reply("Hi, admin!")
    await m.answer("Please, choose action", reply_markup=admin_action_keyboard().as_markup(resize_keyboard=True))


@admin_router.message(Command('cancel'))
async def cancel_add_noun(m: Message, state: FSMContext):
    await state.clear()
    await m.answer("You have reached the main menu")
    await m.answer("Okay. Please, choose action",
                   reply_markup=admin_action_keyboard().as_markup(resize_keyboard=True))


@admin_router.message(Command('exit'))
async def exit_to_user_menu(m: Message, state: FSMContext):
    await state.clear()
    await m.reply("You have reached the user main menu",
                  reply_markup=home_keyboard().as_markup(resize_keyboard=True))


@admin_router.message(Text('Users'))
async def bt_users(m: Message):
    amount = await sql_fetchone('SELECT count(*) FROM "users"')
    await m.answer(f"currently registered users in the bot: {amount[0]}")


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
async def uk_translation(m: Message, state: FSMContext):
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
    data = await state.get_data()
    await sql_with_args('INSERT INTO "nouns" (article,'
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
    await bot.send_message(user_id, "Congratulations! New noun has been added",
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


@admin_router.message(Text('Add adjective'))
async def bt_add_adj(m: Message, state: FSMContext):
    await m.answer(f"Write the adjective (in the male form)", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddAdjectives.write_adj)


@admin_router.message(Text, AddAdjectives.write_adj)
async def get_adj(m: Message, state: FSMContext):
    adj = m.text
    await state.update_data(adj=adj)
    await m.answer("Great! Please write a translation for <b>English</b>")
    await state.set_state(AddAdjectives.adj_eng)


@admin_router.message(Text, AddAdjectives.adj_eng)
async def get_adj_on_eng(m: Message, state: FSMContext):
    adj_eng = m.text
    await state.update_data(adj_eng=adj_eng)
    await m.answer("Good! Please write a translation for <b>Ukrainian</b>")
    await state.set_state(AddAdjectives.adj_ukr)


@admin_router.message(Text, AddAdjectives.adj_ukr)
async def get_adj_on_ukr(m: Message, state: FSMContext):
    adj_ukr = m.text
    await state.update_data(adj_ukr=adj_ukr)
    await m.answer("Alright! Please write a translation for <b>Russian</b>")
    await state.set_state(AddAdjectives.adj_rus)


@admin_router.message(Text, AddAdjectives.adj_rus)
async def get_adj_on_rus(m: Message, state: FSMContext):
    adj_rus = m.text
    await state.update_data(adj_rus=adj_rus)
    data = await state.get_data()
    await m.answer(f"Perfect! Check if everything is written correctly:\n\n"
                   f"adjectives: {data['adj']}\n"
                   f"adj_eng: {data['adj_eng']}\n"
                   f"adj_ukr: {data['adj_ukr']}\n"
                   f"adj_rus: {data['adj_rus']}\n",
                   reply_markup=adj_correct_kb().as_markup(resize_keyboard=True))


@admin_router.callback_query(lambda c: c.data == "adj_correct")
async def adj_correct(c: types.CallbackQuery, state: FSMContext):
    user_id = c.from_user.id
    await c.message.delete()
    data = await state.get_data()
    await sql_with_args('INSERT INTO "adjectives" (adj_ger,'
                        ' adj_eng,'
                        ' adj_ukr,'
                        ' adj_rus) VALUES (%s, %s,  %s,  %s)', (data['adj'],
                                                                data['adj_eng'],
                                                                data['adj_ukr'],
                                                                data['adj_rus']))
    await state.clear()
    await bot.send_message(user_id, "Congratulations! New adjective has been added",
                           reply_markup=admin_action_keyboard().as_markup(resize_keyboard=True))


@admin_router.callback_query(lambda c: c.data == "adj_incorrect")
async def adj_incorrect(c: types.CallbackQuery, state: FSMContext):
    user_id = c.from_user.id
    await c.message.delete()
    await state.clear()
    await bot.send_message(user_id, "You have reached the main menu")
    await bot.send_message(user_id,
                           "Okay. Please, choose action",
                           reply_markup=admin_action_keyboard().as_markup(resize_keyboard=True))


@admin_router.message(Text('Add verb'))
async def bt_add_verb(m: Message, state: FSMContext):
    await m.answer(f"Write the verb in infinitive", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddVerb.write_verb)


@admin_router.message(Text, AddVerb.write_verb)
async def get_verb(m: Message, state: FSMContext):
    verb = m.text
    await state.update_data(verb_ger_inf=verb)
    await m.answer("Great! Please, write this verb in past")
    await state.set_state(AddVerb.verb_ger_past)


@admin_router.message(Text, AddVerb.verb_ger_past)
async def get_verb_in_past(m: Message, state: FSMContext):
    past = m.text
    await state.update_data(verb_ger_past=past)
    await m.answer("Good! Now, write this verb in perfect")
    await state.set_state(AddVerb.verb_ger_perfect)


@admin_router.message(Text, AddVerb.verb_ger_perfect)
async def get_verb_in_perf(m: Message, state: FSMContext):
    perf = m.text
    await state.update_data(verb_ger_perf=perf)
    await m.answer("Ok. Write english translation for this verb")
    await state.set_state(AddVerb.verb_eng)


@admin_router.message(Text, AddVerb.verb_eng)
async def get_eng_trans_for_verb(m: Message, state: FSMContext):
    eng = m.text
    await state.update_data(eng=eng)
    await m.answer("Good. Now, write ukrainian translation for this verb")
    await state.set_state(AddVerb.verb_ukr)


@admin_router.message(Text, AddVerb.verb_ukr)
async def get_ukr_trans_for_verb(m: Message, state: FSMContext):
    ukr = m.text
    await state.update_data(ukr=ukr)
    await m.answer("And finally, write russian translation fr this verb")
    await state.set_state(AddVerb.verb_rus)


@admin_router.message(Text, AddVerb.verb_rus)
async def get_rus_trans_for_verb(m: Message, state: FSMContext):
    rus = m.text
    await state.update_data(rus=rus)
    data = await state.get_data()
    await m.answer(f"Perfect! Check if everything is written correctly:\n\n"
                   f"verb_ger_inf: {data['verb_ger_inf']}\n"
                   f"verb_ger_past: {data['verb_ger_past']}\n"
                   f"verb_ger_perf: {data['verb_ger_perf']}\n"
                   f"english: {data['eng']}\n"
                   f"ukrainian: {data['ukr']}\n"
                   f"russian: {data['rus']}",
                   reply_markup=verb_correct_kb().as_markup(resize_keyboard=True))


@admin_router.callback_query(lambda c: c.data == "verb_correct")
async def verb_correct(c: types.CallbackQuery, state: FSMContext):
    user_id = c.from_user.id
    await c.message.delete()
    data = await state.get_data()
    await sql_with_args('INSERT INTO "verbs" (verb_ger_inf,'
                        ' verb_ger_past,'
                        ' verb_ger_perfect,'
                        ' verb_eng,'
                        ' verb_ukr,'
                        ' verb_rus) VALUES (%s, %s,  %s, %s, %s,  %s)', (data['verb_ger_inf'],
                                                                         data['verb_ger_past'],
                                                                         data['verb_ger_perf'],
                                                                         data['eng'],
                                                                         data['ukr'],
                                                                         data['rus']))
    await state.clear()
    await bot.send_message(user_id, "Congratulations! New verb has been added",
                           reply_markup=admin_action_keyboard().as_markup(resize_keyboard=True))


@admin_router.callback_query(lambda c: c.data == "verb_incorrect")
async def verb_incorrect(c: types.CallbackQuery, state: FSMContext):
    user_id = c.from_user.id
    await c.message.delete()
    await state.clear()
    await bot.send_message(user_id, "You have reached the main menu")
    await bot.send_message(user_id,
                           "Okay. Please, choose action",
                           reply_markup=admin_action_keyboard().as_markup(resize_keyboard=True))
