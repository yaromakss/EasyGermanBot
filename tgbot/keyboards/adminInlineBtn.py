from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def noun_correct_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="✅ Yes",
        callback_data="noun_correct"
    ))
    kb.add(InlineKeyboardButton(
        text="❌ No",
        callback_data="noun_incorrect"
    ))
    kb.adjust(2)
    return kb


def adj_correct_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="✅ Yes",
        callback_data="adj_correct"
    ))
    kb.add(InlineKeyboardButton(
        text="❌ No",
        callback_data="adj_incorrect"
    ))
    kb.adjust(2)
    return kb


def verb_correct_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="✅ Yes",
        callback_data="verb_correct"
    ))
    kb.add(InlineKeyboardButton(
        text="❌ No",
        callback_data="verb_incorrect"
    ))
    kb.adjust(2)
    return kb
