# =============================================================================
# Telegram Leech Bot - Command Handlers
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================
# License   : MIT License
# =============================================================================

"""
/start and /help command handlers with Shinobu-style photo menu.
"""

import glob
import logging
import os
import random
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from leechbot import app
from leechbot.utility.variables import Paths
from leechbot.utility.helper import message_deleter

logger = logging.getLogger(__name__)


# safe_answer is in callbacks.common — import at call time to avoid circular import
async def _safe_answer(callback_query, text="", show_alert=False):
    try:
        await callback_query.answer(text=text, show_alert=show_alert)
    except Exception:
        pass


# =============================================================================
# Random Photo Helper
# =============================================================================
def _get_random_photo() -> str:
    """Return a random photo path from assets/images/."""
    images = (
        glob.glob(os.path.join(Paths.ASSETS_IMAGES, "*.jpg"))
        + glob.glob(os.path.join(Paths.ASSETS_IMAGES, "*.png"))
        + glob.glob(os.path.join(Paths.ASSETS_IMAGES, "*.webp"))
    )
    if images:
        return random.choice(images)
    return ""


# =============================================================================
# Module Data
# =============================================================================
MODULES = [
    # ── Downloads ──
    {"id": "upload", "name": "Upload", "desc": "Upload files from links to Telegram or Google Drive.", "cat": "Downloads", "cmds": [
        {"cmd": "/tupload", "desc": "Upload files to Telegram"},
        {"cmd": "/gdupload", "desc": "Mirror files to Google Drive"},
        {"cmd": "/drupload", "desc": "Upload a local directory to Telegram"},
    ]},
    {"id": "ytdl", "name": "YT-DLP", "desc": "Download from YouTube, Facebook, and 2000+ sites.", "cat": "Downloads", "cmds": [
        {"cmd": "/ytupload", "desc": "Download via yt-dlp (YouTube, etc.)"},
        {"cmd": "/formats <url>", "desc": "List available formats for a video URL"},
        {"cmd": "/preview <url>", "desc": "Dry-run a gallery URL to see what would be downloaded"},
    ]},
    {"id": "gallery", "name": "Gallery", "desc": "Download image galleries from 100+ sites.", "cat": "Downloads", "cmds": [
        {"cmd": "/glupload", "desc": "Download image galleries via gallery-dl"},
    ]},
    {"id": "options", "name": "Options", "desc": "Quick download option toggles.", "cat": "Downloads", "cmds": [
        {"cmd": "/setname <name>", "desc": "Set custom filename for next download"},
        {"cmd": "/format", "desc": "Choose yt-dlp quality (1080p/720p/480p/audio)"},
        {"cmd": "/speed", "desc": "Set bandwidth limit"},
    ]},
    # ── Files ──
    {"id": "archive", "name": "Archive", "desc": "Create and extract archives with password support.", "cat": "Files", "cmds": [
        {"cmd": "/zipaswd <pass>", "desc": "Set password for zip compression"},
        {"cmd": "/unzipaswd <pass>", "desc": "Set password for extraction"},
    ]},
    {"id": "queue", "name": "Queue", "desc": "Manage the download queue and cancel tasks.", "cat": "Files", "cmds": [
        {"cmd": "/queue", "desc": "View download queue and session stats"},
        {"cmd": "/cancel", "desc": "Cancel the current running task"},
        {"cmd": "/cancel_all", "desc": "Cancel task and clear the queue"},
    ]},
    # ── Files ──
    {"id": "autorename", "name": "Auto-Rename", "desc": "Set custom filename templates with placeholders.", "cat": "Files", "cmds": [
        {"cmd": "/autorename <template>", "desc": "Set auto-rename template"},
        {"cmd": "/autorename clear", "desc": "Clear auto-rename template"},
    ]},
    # ── Settings ──
    {"id": "settings", "name": "Settings", "desc": "Configure bot preferences and options.", "cat": "Settings", "cmds": [
        {"cmd": "/settings", "desc": "Open interactive settings menu"},
    ]},
    {"id": "status", "name": "Status", "desc": "View bot status, stats, and system info.", "cat": "Settings", "cmds": [
        {"cmd": "/status", "desc": "Show active task detail + queue + transfer stats"},
        {"cmd": "/stats", "desc": "Show lifetime task totals + system resources"},
        {"cmd": "/ping", "desc": "Check Telegram round-trip latency + uptime"},
        {"cmd": "/logs [N]", "desc": "Show last N log lines (default 30)"},
    ]},
    {"id": "system", "name": "System", "desc": "Restart, update, and manage the bot.", "cat": "Settings", "cmds": [
        {"cmd": "/restart", "desc": "Gracefully restart the bot"},
        {"cmd": "/update", "desc": "Check for bot updates"},
    ]},
    # ── Auth ──
    {"id": "cookies", "name": "Cookies", "desc": "YouTube authentication via cookies or PO tokens.", "cat": "Auth", "cmds": [
        {"cmd": "/cookies", "desc": "Check YouTube auth status"},
        {"cmd": "/setcookies", "desc": "Upload a cookies.txt file"},
        {"cmd": "/clearcookies", "desc": "Delete stored cookies file"},
    ]},
    # ── Tools ──
    {"id": "screenshot", "name": "Screenshot", "desc": "Auto-screenshot after upload (or manual).", "cat": "Tools", "cmds": [
        {"cmd": "/screenshot [count]", "desc": "Manual screenshot (backup)"},
        {"cmd": "Auto-SS", "desc": "Enable via Settings → 📸 Auto-SS (extracts after upload)"},
    ]},
    # ── Admin ──
    {"id": "admin", "name": "Admin", "desc": "Manage allowed users and broadcast files.", "cat": "Admin", "cmds": [
        {"cmd": "/admin", "desc": "Manage allowed users (add/remove/list)"},
        {"cmd": "/broadcast <ids>", "desc": "Send last file to multiple chats"},
    ]},
    {"id": "rss", "name": "RSS", "desc": "Subscribe to RSS feeds for automatic downloads.", "cat": "Admin", "cmds": [
        {"cmd": "/rss_add <url> <chat_id>", "desc": "Add an RSS subscription"},
        {"cmd": "/rss_list", "desc": "List all RSS subscriptions"},
        {"cmd": "/rss_remove <url>", "desc": "Remove an RSS subscription"},
        {"cmd": "/rss_check", "desc": "Manually check all RSS feeds now"},
    ]},
]

CATEGORIES = [
    {"id": "Downloads", "name": "Downloads", "desc": "Upload, mirror, yt-dlp, gallery, options.", "emoji": "📥"},
    {"id": "Files", "name": "Files", "desc": "Archive handling, queue, task control, and auto-rename.", "emoji": "🗂"},
    {"id": "Settings", "name": "Settings", "desc": "Bot configuration, status, and system management.", "emoji": "⚙️"},
    {"id": "Auth", "name": "Auth", "desc": "YouTube authentication via cookies or PO tokens.", "emoji": "🍪"},
    {"id": "Tools", "name": "Tools", "desc": "Screenshot generation and watermarking.", "emoji": "🛠"},
    {"id": "Admin", "name": "Admin", "desc": "User management, broadcast, and RSS feeds.", "emoji": "👤"},
]


# =============================================================================
# /start
# =============================================================================
WELCOME_TEXT = """<b>🤖 LeechBot</b> — Advanced Telegram File Transloader

◈ Powerful · Fast · Secure
◈ Download from 2000+ sources
◈ Upload to Telegram or Google Drive

<b>📥 Send any link to start downloading.</b>

Tap a button below to explore:"""


def _start_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📖 Help", callback_data="help_all_0"),
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
        ],
        [InlineKeyboardButton("⚙️ Bot Settings", callback_data="settings_menu")],
        [
            InlineKeyboardButton("📂 GitHub", url="https://github.com/Shineii86/LeechBot"),
            InlineKeyboardButton("🔔 Updates", url="https://t.me/MaximXBots"),
        ],
        [InlineKeyboardButton("💬 Support", url="https://t.me/MaximXGroup")],
    ])


async def _send_welcome(client, message, edit: bool = False):
    photo = _get_random_photo()
    if edit:
        if photo:
            try:
                await message.edit_media(
                    InputMediaPhoto(photo, caption=WELCOME_TEXT),
                    reply_markup=_start_keyboard(),
                )
                return
            except Exception:
                pass
        try:
            await message.edit_text(
                WELCOME_TEXT,
                reply_markup=_start_keyboard(),
                link_preview_options=types.LinkPreviewOptions(is_disabled=True),
            )
            return
        except Exception:
            pass
    try:
        await message.delete()
    except Exception:
        pass
    if photo:
        try:
            await message.reply_photo(
                photo=photo,
                caption=WELCOME_TEXT,
                reply_markup=_start_keyboard(),
            )
            return
        except Exception:
            pass
    await message.reply_text(
        WELCOME_TEXT,
        reply_markup=_start_keyboard(),
        link_preview_options=types.LinkPreviewOptions(is_disabled=True),
    )


@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await _send_welcome(client, message, edit=False)


# =============================================================================
# /help
# =============================================================================
HELP_TEXT = (
    "<b>📖 LeechBot Help Menu</b>\n\n"
    "<i>Browse every available module.</i>"
)


def _help_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Help Menu", callback_data="help_all_0")],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="settings_menu"),
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
        ],
        [InlineKeyboardButton("💬 Support", url="https://t.me/MaximXGroup")],
    ])


@app.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    photo = _get_random_photo()
    if photo:
        try:
            await message.reply_photo(
                photo=photo,
                caption=HELP_TEXT,
                reply_markup=_help_keyboard(),
            )
        except Exception:
            await message.reply_text(
                HELP_TEXT,
                reply_markup=_help_keyboard(),
                link_preview_options=types.LinkPreviewOptions(is_disabled=True),
            )
    else:
        await message.reply_text(
            HELP_TEXT,
            reply_markup=_help_keyboard(),
            link_preview_options=types.LinkPreviewOptions(is_disabled=True),
        )
    try:
        await message.delete()
    except Exception:
        pass


# =============================================================================
# Help Navigation Builders
# =============================================================================

def _build_all_page(page: int):
    per_page = 15
    total = len(MODULES)
    total_pages = max((total + per_page - 1) // per_page, 1)
    page = max(0, min(page, total_pages - 1))

    start = page * per_page
    end = start + per_page
    page_modules = MODULES[start:end]

    text = "<b>All modules:</b>\n<i>Browse every available module.</i>"

    rows = []
    row = []
    for m in page_modules:
        row.append(InlineKeyboardButton(m["name"], callback_data=f"help_mod_{m['id']}"))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        while len(row) < 3:
            row.append(InlineKeyboardButton(" ", callback_data="noop"))
        rows.append(row)

    nav_row = []
    nav_row.append(
        InlineKeyboardButton("⬅️", callback_data=f"help_all_{page - 1}")
        if page > 0
        else InlineKeyboardButton(" ", callback_data="noop")
    )
    nav_row.append(InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="noop"))
    nav_row.append(
        InlineKeyboardButton("➡️", callback_data=f"help_all_{page + 1}")
        if page < total_pages - 1
        else InlineKeyboardButton(" ", callback_data="noop")
    )
    rows.append(nav_row)
    rows.append([InlineKeyboardButton("⟵ Back", callback_data="start_back")])

    return text, InlineKeyboardMarkup(rows)


def _build_cat_view(cat_id: str):
    cat = next((c for c in CATEGORIES if c["id"] == cat_id), None)
    if not cat:
        return "⚠️ Category not found.", InlineKeyboardMarkup(
            [[InlineKeyboardButton("⟵ Back", callback_data="help_all_0")]]
        )

    modules = [m for m in MODULES if m["cat"] == cat_id]
    text = f"<b>{cat['emoji']} {cat['name']} modules:</b>\n<i>{cat['desc']}</i>"

    rows = []
    row = []
    for m in modules:
        row.append(InlineKeyboardButton(m["name"], callback_data=f"help_mod_{m['id']}"))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        while len(row) < 3:
            row.append(InlineKeyboardButton(" ", callback_data="noop"))
        rows.append(row)

    rows.append([InlineKeyboardButton("⟵ Back", callback_data="start_back")])

    return text, InlineKeyboardMarkup(rows)


def _build_mod_view(mod_id: str):
    mod = next((m for m in MODULES if m["id"] == mod_id), None)
    if not mod:
        return "⚠️ Module not found.", InlineKeyboardMarkup(
            [[InlineKeyboardButton("⟵ Back", callback_data="help_all_0")]]
        )

    text = f"<b>Here is the help for the {mod['name']} module:</b>\n\n"
    for c in mod["cmds"]:
        text += f"❖ <b>{c['cmd']}</b> — {c['desc']}\n"

    cat = next((c for c in CATEGORIES if c["id"] == mod["cat"]), None)
    back_data = f"help_cat_{mod['cat']}" if cat else "help_all_0"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⟵ Back", callback_data=back_data)],
    ])

    return text, keyboard


# =============================================================================
# Help Callback Handlers (imported by dispatcher)
# =============================================================================

async def _edit_media_with_photo(message, text, keyboard):
    """Edit a message with a random photo + text + keyboard."""
    photo = _get_random_photo()
    if photo:
        try:
            await message.edit_media(
                InputMediaPhoto(photo, caption=text),
                reply_markup=keyboard,
            )
            return
        except Exception:
            pass
    try:
        await message.edit_text(
            text=text,
            reply_markup=keyboard,
            link_preview_options=types.LinkPreviewOptions(is_disabled=True),
        )
    except Exception:
        pass


async def _handle_help_all(client, callback_query, page: int):
    text, keyboard = _build_all_page(page)
    await _edit_media_with_photo(callback_query.message, text, keyboard)
    await _safe_answer(callback_query)


async def _handle_help_cat(client, callback_query, cat_id: str):
    text, keyboard = _build_cat_view(cat_id)
    await _edit_media_with_photo(callback_query.message, text, keyboard)
    await _safe_answer(callback_query)


async def _handle_help_mod(client, callback_query, mod_id: str):
    text, keyboard = _build_mod_view(mod_id)
    await _edit_media_with_photo(callback_query.message, text, keyboard)
    await _safe_answer(callback_query)
