"""/start command handler — entry point of the bot."""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from config import PARSE_MODE
from keyboards.main_menu import main_menu_keyboard
from languages import get_text
from utils import user_manager

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle ``/start`` by greeting the user and showing the main menu."""
    user = update.effective_user
    if user is None:
        # Defensive: should never happen with a real Telegram update.
        return

    language = user_manager.get_language(user.id)
    first_name = user.first_name or "there"

    text = get_text(language, "welcome", name=first_name)
    keyboard = main_menu_keyboard(language)

    logger.info("/start by user=%s lang=%s", user.id, language)

    await update.message.reply_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=PARSE_MODE,
    )


def register(application) -> None:
    """Wire the handler into the given Application."""
    application.add_handler(CommandHandler("start", start_command))


__all__ = ["start_command", "register"]