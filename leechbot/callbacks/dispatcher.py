# =============================================================================
# Telegram Leech Bot - Callback Query Handlers
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================
# License   : MIT License
# =============================================================================

"""
All inline keyboard callback query handlers.

Each callback category is handled by a dedicated async function
for clarity, testability, and maintainability.
"""

import logging

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from leechbot import app
from leechbot.utility.variables import BOT, MSG, BotTimes, Paths
from leechbot.utility.handler import cancelTask
from leechbot.utility.helper import send_settings, sysINFO, sysINFO_full, status_keyboard
import config

logger = logging.getLogger(__name__)



from .common import safe_answer
from .navigation import _handle_about, _handle_start_back
from .upload import _handle_upload_type, _handle_ytdl_confirm
from .settings import (
    _handle_video_settings,
    _handle_caption_settings,
    _handle_thumb_settings,
    _handle_delete_thumb,
    _handle_autodelete_menu,
    _handle_photo_mode_menu,
    _handle_screenshot_menu,
)
from .system import _handle_sys_refresh, _handle_sys_stats
from .update import _handle_do_update
from ..commands.start_help import (
    _handle_help_all,
    _handle_help_cat,
    _handle_help_mod,
)


# =============================================================================
# Main Dispatcher
# =============================================================================
@app.on_callback_query()
async def handle_callback(client, callback_query):
    """Route callback queries to the appropriate handler."""
    data = callback_query.data
    logger.debug("Callback: %s", data)

    try:
        # --- Help system ---
        if data.startswith("help_all_"):
            page = int(data.split("_")[-1])
            await _handle_help_all(client, callback_query, page)
        elif data.startswith("help_cat_"):
            cat_id = data[len("help_cat_"):]
            await _handle_help_cat(client, callback_query, cat_id)
        elif data.startswith("help_mod_"):
            mod_id = data[len("help_mod_"):]
            await _handle_help_mod(client, callback_query, mod_id)
        elif data == "noop":
            await safe_answer(callback_query)

        # --- About + Start navigation (3.1.35) ---
        elif data == "about":
            await _handle_about(client, callback_query)
        elif data == "start_back":
            await _handle_start_back(client, callback_query)

        # --- Upload type selection ---
        elif data in ("normal", "zip", "unzip", "undzip"):
            await _handle_upload_type(client, callback_query, data)

        # --- Settings navigation ---
        elif data == "settings_menu":
            await send_settings(client, callback_query.message, callback_query.message.id, False)
            await safe_answer(callback_query)

        # --- Video settings ---
        elif data == "video":
            await _handle_video_settings(client, callback_query)

        # --- Caption settings ---
        elif data == "caption":
            await _handle_caption_settings(client, callback_query)

        # --- Thumbnail settings ---
        elif data == "thumb":
            await _handle_thumb_settings(client, callback_query)

        elif data == "del-thumb":
            await _handle_delete_thumb(client, callback_query)

        # --- Prefix / Suffix ---
        elif data == "set-prefix":
            await callback_query.message.edit_text(
                "<b>⌨️ Set Prefix</b>\n\n"
                "Send your prefix text now.\n"
                "Reply to this message with it.\n\n"
                "<b>💡 Tip:</b> Prefix is prepended to file names."
            )
            BOT.State.prefix = True
            await safe_answer(callback_query, "Send your prefix now")

        elif data == "set-suffix":
            await callback_query.message.edit_text(
                "<b>⌨️ Set Suffix</b>\n\n"
                "Send your suffix text now.\n"
                "Reply to this message with it.\n\n"
                "<b>💡 Tip:</b> Suffix is appended to file names."
            )
            BOT.State.suffix = True
            await safe_answer(callback_query, "Send your suffix now")

        # --- Caption style ---
        elif data in ("code-Monospace", "p-Regular", "b-Bold", "i-Italic", "u-Underlined"):
            res = data.split("-")
            BOT.Options.caption = res[0]
            BOT.Setting.caption = res[1]
            await send_settings(client, callback_query.message, callback_query.message.id, False)
            await safe_answer(callback_query, f"Caption style: {res[1]}")

        # --- Video split ---
        elif data in ("split-true", "split-false"):
            BOT.Options.is_split = data == "split-true"
            BOT.Setting.split_video = "Split" if data == "split-true" else "Zip"
            await send_settings(client, callback_query.message, callback_query.message.id, False)
            await safe_answer(callback_query)

        # --- Video convert ---
        elif data in ("convert-true", "convert-false"):
            BOT.Options.convert_video = data == "convert-true"
            BOT.Setting.convert_video = "Yes" if data == "convert-true" else "No"
            await send_settings(client, callback_query.message, callback_query.message.id, False)
            await safe_answer(callback_query)

        # --- Video format ---
        elif data in ("mp4", "mkv"):
            BOT.Options.video_out = data
            await send_settings(client, callback_query.message, callback_query.message.id, False)
            await safe_answer(callback_query, f"Format: {data.upper()}")

        # --- Quality ---
        elif data in ("q-High", "q-Low"):
            quality = data.split("-")[-1]
            BOT.Setting.convert_quality = quality
            BOT.Options.convert_quality = quality == "High"
            await send_settings(client, callback_query.message, callback_query.message.id, False)
            await safe_answer(callback_query, f"Quality: {quality}")

        # --- Upload mode ---
        elif data in ("media", "document"):
            BOT.Options.stream_upload = data == "media"
            BOT.Setting.stream_upload = "Media" if data == "media" else "Document"
            await send_settings(client, callback_query.message, callback_query.message.id, False)
            await safe_answer(callback_query, f"Upload as: {BOT.Setting.stream_upload}")

        # --- Auto-delete ---
        elif data == "autodelete":
            await _handle_autodelete_menu(client, callback_query)

        elif data == "toggle_autodelete":
            BOT.Setting.auto_delete = not BOT.Setting.auto_delete
            await _handle_autodelete_menu(client, callback_query)
            await safe_answer(callback_query, f"Auto-delete: {'ON' if BOT.Setting.auto_delete else 'OFF'}")

        elif data == "set_autodelete_delay":
            from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
            await callback_query.message.edit_text(
                "<b>⏱️ Set Auto-Delete Delay</b>\n\n"
                "Send a number between 5 and 300.\n"
                "This is the delay in <b>seconds</b>.\n\n"
                "<b>💡 Tip:</b> 30s is a good default.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("❰ Back", callback_data="autodelete")]]
                ),
            )
            BOT.State.setting_autodelete_delay = True
            await safe_answer(callback_query)

        # --- Photo mode ---
        elif data == "photo_mode":
            await _handle_photo_mode_menu(client, callback_query)

        elif data in ("photo-group", "photo-single"):
            BOT.Setting.photo_mode = "Group" if data == "photo-group" else "Single"
            await send_settings(client, callback_query.message, callback_query.message.id, False)
            await safe_answer(callback_query, f"Photo mode: {BOT.Setting.photo_mode}")

        # --- Auto update ---
        elif data == "do_update":
            await _handle_do_update(client, callback_query)

        # --- Close / Back ---
        elif data == "close":
            await callback_query.message.delete()
            await safe_answer(callback_query, "Closed")

        elif data == "back":
            await send_settings(client, callback_query.message, callback_query.message.id, False)
            await safe_answer(callback_query)

        # --- YTDL confirmation ---
        elif data in ("ytdl-true", "ytdl-false"):
            await _handle_ytdl_confirm(client, callback_query, data)

        # --- Cancel ---
        elif data == "cancel":
            await safe_answer(callback_query, "Cancelling...")
            await cancelTask("User cancelled the task")

        # --- Format selection ---
        elif data.startswith("fmt-"):
            fmt = data[4:]
            BOT.Setting.ytdl_format = fmt
            await callback_query.message.edit_text(
                f"<b>✅ Format Updated</b>\n\n"
                f"<b>Selected:</b> <code>{fmt}</code>"
            )
            await safe_answer(callback_query, "Format saved ✓")

        # --- Speed limit ---
        elif data.startswith("spd-"):
            speed_val = data[4:]
            config.BANDWIDTH_LIMIT = speed_val
            display_val = speed_val if speed_val else "Unlimited"
            await callback_query.message.edit_text(
                f"<b>✅ Bandwidth Limit Updated</b>\n\n"
                f"<b>Limit:</b> <code>{display_val}</code>"
            )
            await safe_answer(callback_query, "Speed limit saved ✓")

        # --- System info ---
        elif data == "sys_refresh":
            await _handle_sys_refresh(client, callback_query)

        elif data == "sys_stats":
            await _handle_sys_stats(client, callback_query)

        elif data == "sys_close":
            await callback_query.message.delete()
            await safe_answer(callback_query, "Closed")

        # --- Screenshot settings ---
        elif data == "screenshot":
            await _handle_screenshot_menu(client, callback_query)

        elif data == "toggle_autoss":
            BOT.Setting.auto_screenshot = not BOT.Setting.auto_screenshot
            await _handle_screenshot_menu(client, callback_query)
            await safe_answer(callback_query, f"Auto-SS: {'ON' if BOT.Setting.auto_screenshot else 'OFF'}")

        elif data == "ss-count-plus":
            if BOT.Setting.screenshot_count < 20:
                BOT.Setting.screenshot_count += 1
            await _handle_screenshot_menu(client, callback_query)
            await safe_answer(callback_query)

        elif data == "ss-count-minus":
            if BOT.Setting.screenshot_count > 1:
                BOT.Setting.screenshot_count -= 1
            await _handle_screenshot_menu(client, callback_query)
            await safe_answer(callback_query)

        elif data == "set_ss_watermark":
            from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
            await callback_query.message.edit_text(
                "<b>💬 Set Watermark Text</b>\n\n"
                "Send your watermark text now.\n"
                "This will be overlaid on each screenshot.\n\n"
                "<b>💡 Send /cancel to clear watermark.</b>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("❰ Back", callback_data="screenshot")]]
                ),
            )
            BOT.State.set_ss_watermark = True
            await safe_answer(callback_query)

        else:
            await safe_answer(callback_query, "⚠️ Unknown action", show_alert=True)

    except Exception as e:
        logger.error("Callback error [%s]: %s", data, e, exc_info=True)
        try:
            await safe_answer(callback_query, "❌ Something went wrong", show_alert=True)
        except Exception:
            pass

