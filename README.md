# 🔐 Password Generator Bot

A clean, production-ready Telegram bot that generates strong, random passwords on
demand. Ships with a modern inline-keyboard UI, full bilingual support
(English / Arabic) and per-user language memory.

> Built with [python-telegram-bot](https://docs.python-telegram-bot.org/) v21+.

---

## ✨ Features

- 🔐 **One-tap password generation** — pick a length, get a cryptographically
  strong password containing uppercase, lowercase, digits and special symbols.
- ⚙️ **Settings page** — shows the user's Telegram name, ID, `@username`
  and current language.
- 🌐 **Bilingual UI** — every string is translated; the chosen language is
  remembered per user in a local JSON store.
- 🧱 **Inline keyboards only** — no reply keyboards; the UI is consistent on
  every device.
- 🛡️ **Cryptographic randomness** — passwords use `secrets` (the stdlib
  CSPRNG), not `random`.
- 🧩 **Modular codebase** — handlers, keyboards, languages and utils each
  live in their own folder.
- 📋 **Copy-to-clipboard friendly** — passwords and user IDs are rendered in
  `<code>` blocks inside a separate message so they can be long-press copied
  on any Telegram client.

---

## 📁 Project layout

```
password-generator-bot/
├── bot.py                 # Entry point — wires everything together
├── config.py              # Env vars + runtime constants
├── requirements.txt
├── .env.example
├── handlers/              # One module per flow
│   ├── start.py
│   ├── main_menu.py
│   ├── password.py
│   ├── settings.py
│   └── language.py
├── keyboards/             # InlineKeyboardMarkup builders
│   ├── main_menu.py
│   ├── password.py
│   ├── settings.py
│   └── language.py
├── languages/             # Translation tables
│   ├── en.py
│   └── ar.py
├── utils/                 # Helpers (random, persistence, …)
│   ├── password_gen.py
│   └── user_manager.py
└── data/                  # Created at runtime — stores user preferences
    └── users.json
```

---

## 🚀 Quick start

### 1. Create a bot on Telegram

1. Open [@BotFather](https://t.me/BotFather) on Telegram.
2. Send `/newbot` and follow the prompts.
3. Copy the HTTP API token it gives you.

### 2. Install & run

```bash
# Clone or download this project, then:
cd password-generator-bot

# (recommended) create a virtualenv
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

# install deps
pip install -r requirements.txt

# configure your token
cp .env.example .env
# edit .env and paste your real token

# launch the bot
python bot.py
```

You should see something like:

```
2026-07-03 19:09:01 | bot                   | INFO     | ✅ Bot application built successfully.
2026-07-03 19:09:01 | bot                   | INFO     | 🚀 Starting polling…
```

Now open a chat with your bot in Telegram and tap **Start**.

---

## 🧭 User flows

### Main menu

```
👋 Welcome to the Password Generator Bot, <name>!

[ 🔐 Generate Password ]
[ ⚙️ Settings            ]
```

### Generate password

1. User taps **Generate Password** → sees a 2×3 grid of lengths
   (8 / 12 / 16 / 20 / 24 / 32) plus **Back**.
2. User picks a length → bot replies with:

   ```
   🔐 Your Password

   <code>X7@kP#2Lm!Q9</code>

   ✅ Strong & Secure
   📊 Generated with 12 characters. (Strong)
   ```

3. Three buttons appear: **Generate Another** (same length), **Copy
   Password** (sends a fresh copy-friendly message) and **Back**.

### Settings

```
⚙️ Settings

👤 Name: <first name>
🆔 User ID: <id>
📎 Username: @username  (or "No Username")
🌐 Current Language: English 🇺🇸
```

Buttons: **Change Language** • **Copy User ID** • **Refresh Information** • **Back**.

### Change language

Two buttons (**🇪🇬 العربية** / **🇺🇸 English**) plus **Back**.
Whichever the user picks is persisted and the entire UI flips immediately.

---

## 🌐 Adding a new language

1. Create `languages/<code>.py` and export a `TEXTS` dict using the same
   keys as `languages/en.py`.
2. Add the code to `SUPPORTED_LANGUAGES` in `config.py` and a label in
   `LANGUAGE_DISPLAY`.
3. Register it in `languages/__init__.py`'s `_REGISTRY`.

That's it — the language picker, settings page and all UI text will pick
the new language up automatically.

---

## 🔒 Security notes

- Password generation uses `secrets` (CSPRNG) — never `random`.
- The token never appears in source — it lives in `.env`, which is
  `.gitignore`d.
- User data is stored locally in `data/users.json` (atomic writes via
  `tempfile` + `os.replace`). For production-scale deployments, swap the
  `UserManager` in `utils/user_manager.py` for Redis or a database — the
  public surface area is just three functions.

---

## 🧪 Smoke test (no Telegram needed)

```python
from utils.password_gen import generate_password
print(generate_password(16))
```

You should get something like `Y4&hT8@eZrQ!kP1$` (with one of each
character class guaranteed).

---

## 📜 License

MIT — do whatever you want, no warranty.