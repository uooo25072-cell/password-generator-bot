"""Strong random password generation."""

from __future__ import annotations

import secrets
import string

from config import SPECIAL_SYMBOLS


def generate_password(length: int = 16) -> str:
    """Generate a cryptographically strong password.

    The returned string always contains **at least one** character from each
    of these four sets:

    * Uppercase letters  ``A-Z``
    * Lowercase letters  ``a-z``
    * Digits             ``0-9``
    * Special symbols    ``!@#$%^&*``

    Any remaining slots are filled with characters drawn uniformly from the
    combined pool, and the final result is shuffled so that the position of
    the mandatory characters is unpredictable.

    ``secrets`` is used instead of ``random`` because it is the
    cryptographically-secure RNG from the Python stdlib — the way it should
    be for anything security-related.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    symbols = SPECIAL_SYMBOLS

    pool = upper + lower + digits + symbols

    # Guarantee one character from every category
    mandatory = [
        secrets.choice(upper),
        secrets.choice(lower),
        secrets.choice(digits),
        secrets.choice(symbols),
    ]

    # Fill the rest from the combined pool
    remaining = [secrets.choice(pool) for _ in range(length - 4)]

    chars = mandatory + remaining
    # SystemRandom.shuffle uses os.urandom under the hood — safe to use.
    secrets.SystemRandom().shuffle(chars)

    return "".join(chars)


def password_strength(length: int) -> str:
    """Return a short strength label based on length (informational only)."""
    if length < 10:
        return "Basic"
    if length < 16:
        return "Good"
    if length < 24:
        return "Strong"
    return "Very Strong"


__all__ = ["generate_password", "password_strength"]