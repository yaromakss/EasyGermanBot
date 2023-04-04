from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram import Bot, types
from aiogram.filters.callback_data import CallbackData
from typing import Optional


class CastomCallback(CallbackData, prefix="fabnum"):
    # castom class for callback_data
    action: str
    order_id: Optional[int]


# def example_button():
#     example = InlineKeyboardBuilder()
#     example.add(types.InlineKeyboardButton(
#         text='confirm',
#         callback_data=CastomCallback(action="end_order")
#     ))
#     example.add(types.InlineKeyboardButton(
#         text='skip',
#         callback_data='skip'
#     ))
#     return example


def choose_lang_keyboard():
    choose_lang_bts = InlineKeyboardBuilder()
    choose_lang_bts.add(types.InlineKeyboardButton(
        text='🇷🇺 Русский',
        callback_data='ru'
    ))
    choose_lang_bts.add(types.InlineKeyboardButton(
        text='🇺🇦 Українська',
        callback_data='ua'
    ))
    choose_lang_bts.add(types.InlineKeyboardButton(
        text='🇺🇸 English',
        callback_data='en'
    ))
    choose_lang_bts.adjust(1)
    return choose_lang_bts


def achievements_category():
    achievements_bts = InlineKeyboardBuilder()
    achievements_bts.add(
        types.InlineKeyboardButton(
            text="Participle II (Perfect)",
            callback_data='participle'
        ))
    achievements_bts.add(
        types.InlineKeyboardButton(
            text="Articles",
            callback_data='articles'
        ))
    achievements_bts.add(
        types.InlineKeyboardButton(
            text="Plural",
            callback_data='plural'
        ))
    achievements_bts.adjust(1)
    return achievements_bts
