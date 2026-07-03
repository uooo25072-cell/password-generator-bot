"""English language strings for the bot UI."""

TEXTS: dict[str, str] = {
    # -----------------------------------------------------------------------
    # General
    # -----------------------------------------------------------------------
    "welcome": (
        "👋 <b>Welcome to the Password Generator Bot, {name}!</b>\n\n"
        "Generate strong and secure passwords in seconds.\n"
        "Pick an option from the menu below to get started."
    ),
    "main_menu_title": (
        "🏠 <b>Main Menu</b>\n\n"
        "What would you like to do?"
    ),
    "back_to_menu": "↩️ Back to Main Menu",
    "btn_back": "🏠 Back",

    # -----------------------------------------------------------------------
    # Main menu buttons
    # -----------------------------------------------------------------------
    "btn_generate": "🔐 Generate Password",
    "btn_settings": "⚙️ Settings",

    # -----------------------------------------------------------------------
    # Password generation
    # -----------------------------------------------------------------------
    "choose_length": (
        "📏 <b>Choose a password length</b>\n\n"
        "Pick how long you want your password to be:"
    ),
    "btn_length_8": "8 chars",
    "btn_length_12": "12 chars",
    "btn_length_16": "16 chars",
    "btn_length_20": "20 chars",
    "btn_length_24": "24 chars",
    "btn_length_32": "32 chars",

    "your_password_title": "🔐 <b>Your Password</b>",
    "strong_secure": "✅ <i>Strong &amp; Secure</i>",
    "password_caption": (
        "Generated with <b>{length}</b> characters.\n"
        "Contains uppercase, lowercase, numbers and symbols."
    ),
    "btn_generate_another": "🔄 Generate Another",
    "btn_copy_password": "📋 Copy Password",

    # -----------------------------------------------------------------------
    # Settings page
    # -----------------------------------------------------------------------
    "settings_title": "⚙️ <b>Settings</b>\n\nHere is your account information:",
    "name_label": "👤 Name",
    "user_id_label": "🆔 User ID",
    "username_label": "📎 Username",
    "no_username": "No Username",
    "language_label": "🌐 Current Language",
    "btn_change_language": "🌐 Change Language",
    "btn_copy_user_id": "📋 Copy User ID",
    "btn_refresh_info": "🔄 Refresh Information",
    "info_refreshed": "🔄 <i>Information refreshed!</i>",

    # -----------------------------------------------------------------------
    # Language page
    # -----------------------------------------------------------------------
    "language_title": (
        "🌐 <b>Choose Your Language</b>\n\n"
        "Select your preferred language:"
    ),
    "btn_lang_en": "🇺🇸 English",
    "btn_lang_ar": "🇪🇬 العربية",
    "language_changed": (
        "✅ <b>Language updated successfully!</b>\n\n"
        "Your interface is now in <b>{language}</b>."
    ),

    # -----------------------------------------------------------------------
    # Copy-to-clipboard helpers
    # -----------------------------------------------------------------------
    "copy_password_msg": (
        "📋 <b>Your password</b>\n"
        "<i>Tap and hold the text below to copy it.</i>"
    ),
    "copy_user_id_msg": (
        "🆔 <b>Your User ID</b>\n"
        "<i>Tap and hold the text below to copy it.</i>"
    ),

    # -----------------------------------------------------------------------
    # Errors
    # -----------------------------------------------------------------------
    "error_generic": (
        "❌ <b>Something went wrong.</b>\n"
        "Please try again or return to the main menu."
    ),
    "error_invalid_callback": (
        "⚠️ That action is no longer valid. Returning to the main menu."
    ),
}