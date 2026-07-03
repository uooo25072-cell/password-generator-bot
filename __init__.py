"""Language registry + lookup helper."""

from config import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES
from languages import ar, en

# Map: language code -> module containing the TEXTS dict
_REGISTRY: dict[str, dict[str, str]] = {
    "en": en.TEXTS,
    "ar": ar.TEXTS,
}


def get_text(language: str, key: str, /, **fmt) -> str:
    """Return the translated string for *key* in *language*.

    Falls back to the default language if the requested language is unknown,
    and to an empty string if even the key is missing — so a missing
    translation can never crash the bot.

    Any additional ``**fmt`` kwargs are passed to ``str.format`` so callers
    can do ``get_text("en", "welcome", name="Alice")``.
    """
    lang_table = _REGISTRY.get(language) or _REGISTRY[DEFAULT_LANGUAGE]
    template = lang_table.get(key)

    # Fallback to default language if the key is missing in the chosen one
    if template is None:
        template = _REGISTRY[DEFAULT_LANGUAGE].get(key, "")

    if not fmt:
        return template
    try:
        return template.format(**fmt)
    except (KeyError, IndexError):
        # Bad placeholder usage — return raw template rather than crashing.
        return template


def language_name(language: str) -> str:
    """Human-readable language label, e.g. for the Settings page."""
    from config import LANGUAGE_DISPLAY
    return LANGUAGE_DISPLAY.get(language, language)


def is_supported(language: str) -> bool:
    """Check if *language* is a supported language code."""
    return language in SUPPORTED_LANGUAGES


__all__ = ["get_text", "language_name", "is_supported"]