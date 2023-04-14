from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from aiogram import Bot, types
from aiogram.filters.callback_data import CallbackData
from typing import Optional


class CastomCallback(CallbackData, prefix="fabnum"):
    # castom class for callback_data
    action: str
    order_id: Optional[int]


def noun_correct_kb():
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(
        text="✅ Yes",
        callback_data="noun_correct"
    ))
    kb.add(types.InlineKeyboardButton(
        text="❌ No",
        callback_data="noun_incorrect"
    ))
    kb.adjust(2)
    return kb


def adj_correct_kb():
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(
        text="✅ Yes",
        callback_data="adj_correct"
    ))
    kb.add(types.InlineKeyboardButton(
        text="❌ No",
        callback_data="adj_incorrect"
    ))
    kb.adjust(2)
    return kb


