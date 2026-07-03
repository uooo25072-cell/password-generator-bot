"""
Smoke test — verifies password generation, language lookups and keyboard
construction without needing a real Telegram bot token.

Run with:  python smoke_test.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Make sibling packages importable when running this file directly
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import ALLOWED_PASSWORD_LENGTHS, SPECIAL_SYMBOLS
from keyboards.language import language_keyboard
from keyboards.main_menu import main_menu_keyboard
from keyboards.password import password_length_keyboard, password_result_keyboard
from keyboards.settings import settings_keyboard
from languages import get_text, is_supported, language_name
from utils.password_gen import generate_password, password_strength


def _assert(condition: bool, message: str) -> None:
    if not condition:
        print(f"❌ {message}")
        sys.exit(1)
    print(f"✅ {message}")


def test_password_generation() -> None:
    print("\n=== Password generation ===")
    _assert(len(SPECIAL_SYMBOLS) >= 4, "Special-symbol pool has ≥4 chars")

    for length in ALLOWED_PASSWORD_LENGTHS:
        pwd = generate_password(length)
        has_upper = bool(re.search(r"[A-Z]", pwd))
        has_lower = bool(re.search(r"[a-z]", pwd))
        has_digit = bool(re.search(r"[0-9]", pwd))
        has_symbol = bool(re.search(rf"[{re.escape(SPECIAL_SYMBOLS)}]", pwd))
        _assert(
            len(pwd) == length,
            f"Length {length}: produced exactly {length} chars (got {len(pwd)})",
        )
        _assert(has_upper, f"Length {length}: contains uppercase")
        _assert(has_lower, f"Length {length}: contains lowercase")
        _assert(has_digit, f"Length {length}: contains digit")
        _assert(has_symbol, f"Length {length}: contains symbol")
        print(f"   sample: {pwd}  ({password_strength(length)})")


def test_languages() -> None:
    print("\n=== Language lookups ===")
    _assert(is_supported("en"), "English is supported")
    _assert(is_supported("ar"), "Arabic is supported")
    _assert(not is_supported("klingon"), "Unknown language is rejected")

    welcome_en = get_text("en", "welcome", name="Alice")
    welcome_ar = get_text("ar", "welcome", name="علي")
    _assert("Alice" in welcome_en, "English welcome formats the name")
    _assert("علي" in welcome_ar, "Arabic welcome formats the name (RTL text)")

    # Fallback to default when key is missing in chosen language
    fallback = get_text("ar", "welcome", name="Bob")
    _assert("Bob" in fallback, "Fallback still formats the name")

    print(f"   EN name: {language_name('en')}")
    print(f"   AR name: {language_name('ar')}")


def test_keyboards() -> None:
    print("\n=== Keyboards ===")
    for label, km in [
        ("main menu", main_menu_keyboard("en")),
        ("main menu (ar)", main_menu_keyboard("ar")),
        ("length picker", password_length_keyboard("en")),
        ("length picker (ar)", password_length_keyboard("ar")),
        ("result (len=16)", password_result_keyboard("en", 16)),
        ("settings", settings_keyboard("en")),
        ("settings (ar)", settings_keyboard("ar")),
        ("language", language_keyboard("en")),
    ]:
        _assert(km.inline_keyboard, f"{label}: has at least one row")
        for row in km.inline_keyboard:
            for btn in row:
                _assert(
                    btn.text, f"{label}: button '{btn.callback_data}' has text"
                )
                _assert(
                    len(btn.callback_data or "") <= 64,
                    f"{label}: callback '{btn.callback_data}' ≤ 64 bytes",
                )


def main() -> None:
    print("🔐 Password Generator Bot — smoke test\n")
    test_password_generation()
    test_languages()
    test_keyboards()
    print("\n🎉 All smoke tests passed. The bot is ready to launch.")


if __name__ == "__main__":
    main()