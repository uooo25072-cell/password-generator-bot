"""Inline keyboards for the main menu."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from languages import get_text


def main_menu_keyboard(language: str) -> InlineKeyboardMarkup:
    """Build the top-level menu shown on /start and after most actions."""
    keyboard = [
        [
            InlineKeyboardButton(
                get_text(language, "btn_generate"),
                callback_data="generate_password",
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(language, "btn_settings"),
                callback_data="settings",
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


__all__ = ["main_menu_keyboard"]