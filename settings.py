"""Inline keyboards for the Settings page."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from languages import get_text


def settings_keyboard(language: str) -> InlineKeyboardMarkup:
    """All four actions available from the Settings page."""
    keyboard: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                get_text(language, "btn_change_language"),
                callback_data="change_language",
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(language, "btn_copy_user_id"),
                callback_data="copy_user_id",
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(language, "btn_refresh_info"),
                callback_data="refresh_info",
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(language, "btn_back"),
                callback_data="main_menu",
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


__all__ = ["settings_keyboard"]