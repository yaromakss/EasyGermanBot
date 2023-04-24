from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def choose_lang_keyboard():
    choose_lang_bts = InlineKeyboardBuilder()
    choose_lang_bts.add(InlineKeyboardButton(
        text='🇷🇺 Русский',
        callback_data='ru'
    ))
    choose_lang_bts.add(InlineKeyboardButton(
        text='🇺🇦 Українська',
        callback_data='ua'
    ))
    choose_lang_bts.add(InlineKeyboardButton(
        text='🇺🇸 English',
        callback_data='en'
    ))
    choose_lang_bts.adjust(1)
    return choose_lang_bts


def achievements_category():
    achievements_bts = InlineKeyboardBuilder()
    achievements_bts.add(
        InlineKeyboardButton(
            text="Participle II (Perfect)",
            callback_data='perfect'
        ))
    achievements_bts.add(
        InlineKeyboardButton(
            text="Articles",
            callback_data='articles'
        ))
    achievements_bts.add(
        InlineKeyboardButton(
            text="Plural",
            callback_data='plural'
        ))
    achievements_bts.adjust(1)
    return achievements_bts
