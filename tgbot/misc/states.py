from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class example_state(StatesGroup):
    name = State()
    age = State()


class RandomWordState(StatesGroup):
    button = State()


class ArticlesState(StatesGroup):
    answer = State()
    next_or_menu = State()


class PluralState(StatesGroup):
    answer = State()
    next_or_menu = State()


class PerfectState(StatesGroup):
    answer = State()
    next_or_menu = State()

