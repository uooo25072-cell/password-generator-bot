"""Inline keyboards for the Language selection page."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from languages import get_text


def language_keyboard(language: str) -> InlineKeyboardMarkup:
    """Two buttons (Arabic + English) + Back. Labels stay in their own
    native language regardless of the user's currently selected UI language
    — picking a language should never require translation."""

    keyboard: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                "🇪🇬 العربية",
                callback_data="lang_ar",
            ),
        ],
        [
            InlineKeyboardButton(
                "🇺🇸 English",
                callback_data="lang_en",
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(language, "btn_back"),
                callback_data="settings",
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


__all__ = ["language_keyboard"]