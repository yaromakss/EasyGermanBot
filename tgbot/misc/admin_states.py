from aiogram.fsm.context import FSMContext
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