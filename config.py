"""
Configuration module for the Password Generator Bot.

Centralises all runtime configuration (env vars, constants) so the rest of
the codebase doesn't have to reach into `os.environ` directly.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from a local .env file (if present)
load_dotenv()

# ---------------------------------------------------------------------------
# Bot credentials
# ---------------------------------------------------------------------------
# Get your token from @BotFather on Telegram.
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------
# Local JSON file used to remember each user's language preference.
# In production you would swap this for Redis / a real database.
BASE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR: Path = BASE_DIR / "data"
USERS_FILE: Path = DATA_DIR / "users.json"

# ---------------------------------------------------------------------------
# Supported languages
# ---------------------------------------------------------------------------
DEFAULT_LANGUAGE: str = "en"
SUPPORTED_LANGUAGES: tuple[str, ...] = ("en", "ar")

# Friendly names shown in the Settings page
LANGUAGE_DISPLAY: dict[str, str] = {
    "en": "English 🇺🇸",
    "ar": "العربية 🇪🇬",
}

# ---------------------------------------------------------------------------
# Password generation
# ---------------------------------------------------------------------------
ALLOWED_PASSWORD_LENGTHS: tuple[int, ...] = (8, 12, 16, 20, 24, 32)
SPECIAL_SYMBOLS: str = "!@#$%^&*"

# ---------------------------------------------------------------------------
# Telegram parsing mode
# ---------------------------------------------------------------------------
# HTML is the safest mode here — it doesn't choke on the special characters
# that appear inside generated passwords.
PARSE_MODE: str = "HTML"