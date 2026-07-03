"""
Password Generator Bot — entry point.

Wires every flow into a PTB v20+ ``Application`` and starts long-polling.

Run with::

    python bot.py
"""

from __future__ import annotations

import logging
import sys

from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN, PARSE_MODE
from handlers import register_all
from keyboards.main_menu import main_menu_keyboard
from languages import get_text
from utils import user_manager

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s | %(name)-20s | %(levelname)-7s | %(message)s",
    level=logging.INFO,
)
# Silence chatty HTTP libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram.ext._updater").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Fallback handlers
# ---------------------------------------------------------------------------
async def on_unknown_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Catch any callback that no other handler claimed.

    Falls back to the user's main menu so a stale button never strands them.
    """
    query = update.callback_query
    if query is None:
        return
    await query.answer()

    user = query.from_user
    language = "en" if user is None else user_manager.get_language(user.id)

    await query.edit_message_text(
        text=get_text(language, "error_invalid_callback"),
        reply_markup=main_menu_keyboard(language),
    )


async def on_unknown_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Reply to stray text with the main menu so users always have a way back."""
    if update.message is None or update.effective_user is None:
        return

    language = user_manager.get_language(update.effective_user.id)
    await update.message.reply_text(
        text=get_text(language, "main_menu_title"),
        reply_markup=main_menu_keyboard(language),
        parse_mode=PARSE_MODE,
    )


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Top-level error handler — log without crashing the polling loop."""
    logger.exception("Unhandled error while processing update: %s", context.error)


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------
def build_application() -> Application:
    """Construct and configure the PTB Application."""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
        sys.exit(
            "❌ BOT_TOKEN is not configured.\n"
            "Set it in a .env file or as an environment variable and try again.\n"
            "Get a token from @BotFather on Telegram."
        )

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Domain handlers (one per flow)
    register_all(application)

    # Catch-all: any callback we didn't claim gets a graceful fallback.
    application.add_handler(CallbackQueryHandler(on_unknown_callback))
    # Catch-all: any plain text message (not a command) gets the main menu.
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, on_unknown_message)
    )
    application.add_handler(
        MessageHandler(filters.COMMAND, lambda u, c: u.message.reply_text(
            "🤖 Use /start to open the menu."
        ))
    )
    application.add_error_handler(on_error)

    logger.info("✅ Bot application built successfully.")
    return application


def main() -> None:
    """Start the bot in long-polling mode."""
    application = build_application()
    logger.info("🚀 Starting polling…")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()