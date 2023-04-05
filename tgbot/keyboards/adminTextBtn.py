from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardBuilder, KeyboardButton
from aiogram import Bot, types


def admin_action_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(text="Add noun")
    )
    kb.add(
        KeyboardButton(text="Add verb")
    )
    kb.add(
        KeyboardButton(text="Add adjective")
    )
    kb.add(
        KeyboardButton(text="Users")
    )
    kb.adjust(2)
    return kb


def admin_menu():
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(text="menu")
    )
    return kb


def admin_der_die_das():
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
