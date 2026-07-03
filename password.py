"""Inline keyboards for the password-generation flow."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import ALLOWED_PASSWORD_LENGTHS
from languages import get_text

# Map: callback suffix -> translation key for that length's button label.
_LENGTH_LABEL_KEYS: dict[int, str] = {
    8: "btn_length_8",
    12: "btn_length_12",
    16: "btn_length_16",
    20: "btn_length_20",
    24: "btn_length_24",
    32: "btn_length_32",
}


def _length_buttons(language: str, lengths: list[int]) -> list[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            get_text(language, _LENGTH_LABEL_KEYS[length]),
            callback_data=f"pw_{length}",
        )
        for length in lengths
    ]


def password_length_keyboard(language: str) -> InlineKeyboardMarkup:
    """Three-column grid of all allowed password lengths + Back."""
    # Split the six options into two rows of three for a tidy grid
    rows: list[list[InlineKeyboardButton]] = []
    allowed = list(ALLOWED_PASSWORD_LENGTHS)

    for start in range(0, len(allowed), 3):
        rows.append(_length_buttons(language, allowed[start : start + 3]))

    rows.append(
        [
            InlineKeyboardButton(
                get_text(language, "btn_back"),
                callback_data="main_menu",
            ),
        ]
    )

    return InlineKeyboardMarkup(rows)


def password_result_keyboard(language: str, length: int) -> InlineKeyboardMarkup:
    """Buttons shown beneath a freshly generated password."""
    keyboard: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                get_text(language, "btn_generate_another"),
                callback_data=f"pw_{length}",
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(language, "btn_copy_password"),
                callback_data="copy_password",
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


__all__ = ["password_length_keyboard", "password_result_keyboard"]