from aiogram.fsm.state import State, StatesGroup


class AddNoun(StatesGroup):
    write_noun = State()
    choose_article = State()
    plural = State()
    sing_eng = State()
    plural_eng = State()
    sing_ukr = State()
    plural_ukr = State()
    sing_rus = State()
    plural_rus = State()


class AddAdjectives(StatesGroup):
    write_adj = State()
    adj_eng = State()
    adj_ukr = State()
    adj_rus = State()


class AddVerb(StatesGroup):
    write_verb = State()
    verb_ger_past = State()
    verb_ger_perfect = State()
    verb_eng = State()
    verb_ukr = State()
    verb_rus = State()
