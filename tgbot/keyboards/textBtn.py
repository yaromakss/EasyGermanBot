from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram import Bot, types


def home_keyboard():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Plural")
    )
    home_buttons.add(
        types.KeyboardButton(text="Articles")
    )
    home_buttons.add(
        types.KeyboardButton(text="Participle II (Perfect)")
    )
    home_buttons.add(
        types.KeyboardButton(text="Random word")
    )
    home_buttons.add(
        types.KeyboardButton(text="Achievements")
    )
    home_buttons.adjust(1)
    return home_buttons


def choose_lang_keyboard():
    choose_lang_bts = ReplyKeyboardBuilder()
    choose_lang_bts.add(
        types.KeyboardButton(text="")
    )







