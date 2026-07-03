"""Lightweight JSON-backed user-preference store.

Stores per-user data (currently: language preference) in a local JSON file.
The implementation is intentionally tiny so it's trivial to swap for Redis
or a real database later — the public surface area is just
``get_language`` and ``set_language``.

Reads and writes are guarded by a module-level ``threading.Lock`` because
Telegram bots can receive updates concurrently, and we don't want a
half-written JSON file corrupting user data.
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
import threading
from typing import Any

from config import DATA_DIR, DEFAULT_LANGUAGE, USERS_FILE

logger = logging.getLogger(__name__)

# A single lock is enough: writes are infrequent and short-lived.
_lock = threading.Lock()


def _ensure_storage() -> None:
    """Create the data dir + file if they don't exist yet."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text("{}", encoding="utf-8")


def _read() -> dict[str, Any]:
    """Read the entire users dict from disk. Returns ``{}`` on any failure."""
    _ensure_storage()
    try:
        with USERS_FILE.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read users file (%s) — starting empty.", exc)
        return {}


def _write(data: dict[str, Any]) -> None:
    """Atomically replace the users file with *data*.

    Writing to a sibling temp file then renaming avoids partial writes if
    the process is killed mid-flush.
    """
    _ensure_storage()
    fd, tmp_path = tempfile.mkstemp(
        prefix=".users_", suffix=".json", dir=str(DATA_DIR)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        os.replace(tmp_path, USERS_FILE)
    except Exception:
        # Best-effort cleanup if the rename never happened
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def get_language(user_id: int) -> str:
    """Return the user's saved language code, or the default."""
    with _lock:
        data = _read()
    record = data.get(str(user_id), {})
    return record.get("language", DEFAULT_LANGUAGE)


def set_language(user_id: int, language: str) -> None:
    """Persist the user's language preference."""
    with _lock:
        data = _read()
        data[str(user_id)] = {**data.get(str(user_id), {}), "language": language}
        _write(data)
        logger.info("Saved language=%s for user %s", language, user_id)


def get_user(user_id: int) -> dict[str, Any]:
    """Return the full record for a user (empty dict if unknown)."""
    with _lock:
        data = _read()
    return data.get(str(user_id), {})


__all__ = ["get_language", "set_language", "get_user"]