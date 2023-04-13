from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram.types import KeyboardButton


def home_keyboard():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        KeyboardButton(text="Plural")
    )
    home_buttons.add(
        KeyboardButton(text="Articles")
    )
    home_buttons.add(
        KeyboardButton(text="Participle II (Perfect)")
    )
    home_buttons.add(
        KeyboardButton(text="Random word")
    )
    home_buttons.add(
        KeyboardButton(text="Achievements")
    )
    home_buttons.adjust(1)
    return home_buttons


def random_word_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(text="Noun")
    )
    kb.add(
        KeyboardButton(text="Verb")
    )
    kb.add(
        KeyboardButton(text="Adjectives")
    )
    kb.add(
        KeyboardButton(text="Else")
    )
    kb.add(
        KeyboardButton(text="Menu")
    )
    kb.adjust(2)
    return kb


def der_die_das_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(text="der")
    )
    kb.add(
        KeyboardButton(text="die")
    )
    kb.add(
        KeyboardButton(text="das")
    )
    kb.adjust(3)
    return kb


def next_or_menu_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(text="menu")
    )
    kb.add(
        KeyboardButton(text="next")
    )
    kb.adjust(2)
    return kb


def idk_plural_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(text="i don`t know")
    )
    return kb



