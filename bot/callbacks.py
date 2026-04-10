# =============================================================================
# LeechBot Pro - Callback Query Handlers
# =============================================================================
# Project   : LeechBot Pro v3.0
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://t.me/Shineii86
# =============================================================================

import os
import logging
from datetime import datetime
from asyncio import get_event_loop
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from colab_leecher import colab_bot, OWNER
from colab_leecher.utility.handler import cancel_task
from colab_leecher.utility.variables import BOT, MSG, BotTimes
from colab_leecher.utility.task_manager import task_scheduler
from colab_leecher.utility.helper import send_settings_menu, create_cancel_keyboard


# =============================================================================
# MAIN CALLBACK HANDLER
# =============================================================================
@colab_bot.on_callback_query()
async def callback_handler(client, callback_query):
    """Handle all callback queries."""
    data = callback_query.data
    
    # Mode selection callbacks
    if data in ["normal", "zip", "unzip", "undzip"]:
        await handle_mode_selection(callback_query, data)
    
    # Settings callbacks
    elif data == "video":
        await show_video_settings(callback_query)
    elif data == "caption":
        await show_caption_settings(callback_query)
    elif data == "thumb":
        await show_thumbnail_settings(callback_query)
    elif data == "back":
        await back_to_main_settings(callback_query)
    elif data == "close":
        await close_settings(callback_query)
    
    # Video settings
    elif data.startswith("split-"):
        await handle_split_setting(callback_query, data)
    elif data.startswith("convert-"):
        await handle_convert_setting(callback_query, data)
    elif data in ["mp4", "mkv"]:
        await handle_format_setting(callback_query, data)
    elif data.startswith("q-"):
        await handle_quality_setting(callback_query, data)
    
    # Caption settings
    elif data.startswith(("code-", "b-", "i-", "u-", "p-")):
        await handle_caption_style(callback_query, data)
    
    # Thumbnail settings
    elif data == "del-thumb":
        await delete_thumbnail(callback_query)
    
    # Upload mode
    elif data in ["media", "document"]:
        await handle_upload_mode(callback_query, data)
    
    # Prefix/Suffix
    elif data == "set-prefix":
        await set_prefix(callback_query)
    elif data == "set-suffix":
        await set_suffix(callback_query)
    elif data == "speed-limit":
        await set_speed_limit(callback_query)
    
    # Cancel task
    elif data == "cancel":
        await cancel_task("Cancelled by user")
    
    # Help
    elif data == "help":
        await show_help(callback_query)


# =============================================================================
# MODE SELECTION
# =============================================================================
async def handle_mode_selection(callback_query, mode):
    """Handle mode selection (normal/zip/unzip/undzip)."""
    BOT.Mode.type = mode
    
    await callback_query.message.delete()
    await colab_bot.delete_messages(
        chat_id=callback_query.message.chat.id,
        message_ids=callback_query.message.reply_to_message_id,
    )
    
    MSG.status_msg = await colab_bot.send_message(
        chat_id=OWNER,
        text="<b>🚀 STARTING TASK</b>\n\n<i>Initializing download process...</i>",
        reply_markup=create_cancel_keyboard(),
    )
    
    BOT.State.task_going = True
    BOT.State.started = False
    BotTimes.start_time = datetime.now()
    
    event_loop = get_event_loop()
    BOT.TASK = event_loop.create_task(task_scheduler())
    
    try:
        await BOT.TASK
    finally:
        BOT.State.task_going = False


# =============================================================================
# SETTINGS MENUS
# =============================================================================
async def show_video_settings(callback_query):
    """Show video conversion settings."""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"✂️ Split: {BOT.Setting.split_video}", 
                callback_data=f"split-{'false' if BOT.Options.is_split else 'true'}"
            ),
        ],
        [
            InlineKeyboardButton(
                f"🔄 Convert: {BOT.Setting.convert_video}",
                callback_data=f"convert-{'false' if BOT.Options.convert_video else 'true'}"
            ),
        ],
        [
            InlineKeyboardButton(f"📹 Format: {BOT.Options.video_out.upper()}", callback_data="format"),
        ],
        [
            InlineKeyboardButton("🎬 MP4", callback_data="mp4"),
            InlineKeyboardButton("🎬 MKV", callback_data="mkv"),
        ],
        [
            InlineKeyboardButton(
                f"🔥 Quality: {BOT.Setting.convert_quality}",
                callback_data=f"q-{'Low' if BOT.Setting.convert_quality == 'High' else 'High'}"
            ),
        ],
        [InlineKeyboardButton("⬅️ Back", callback_data="back")],
    ])
    
    text = f"""<b>🎥 VIDEO SETTINGS</b>

<b>Current Configuration:</b>
• ✂️ <b>Split Videos:</b> <code>{BOT.Setting.split_video}</code>
• 🔄 <b>Convert:</b> <code>{BOT.Setting.convert_video}</code>
• 📹 <b>Format:</b> <code>{BOT.Options.video_out.upper()}</code>
• 🔥 <b>Quality:</b> <code>{BOT.Setting.convert_quality}</code>

<i>Tap options to change settings</i>"""
    
    await callback_query.message.edit_text(text=text, reply_markup=keyboard)


async def show_caption_settings(callback_query):
    """Show caption style settings."""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📟 Monospace", callback_data="code-Monospace"),
            InlineKeyboardButton("🔲 Regular", callback_data="p-Regular"),
        ],
        [
            InlineKeyboardButton("🔵 Bold", callback_data="b-Bold"),
            InlineKeyboardButton("🟣 Italic", callback_data="i-Italic"),
        ],
        [
            InlineKeyboardButton("🟡 Underlined", callback_data="u-Underlined"),
        ],
        [InlineKeyboardButton("⬅️ Back", callback_data="back")],
    ])
    
    text = f"""<b>📝 CAPTION STYLE</b>

<b>Current:</b> <code>{BOT.Setting.caption_style}</code>

<b>Preview:</b>
• <code>Monospace</code>
• Regular
• <b>Bold</b>
• <i>Italic</i>
• <u>Underlined</u>

<i>Select your preferred style</i>"""
    
    await callback_query.message.edit_text(text=text, reply_markup=keyboard)


async def show_thumbnail_settings(callback_query):
    """Show thumbnail settings."""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🗑️ Delete Thumbnail", callback_data="del-thumb"),
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="back"),
        ],
    ])
    
    thumb_status = "✅ Set" if BOT.Setting.thumbnail else "❌ None"
    
    text = f"""<b>🖼️ THUMBNAIL SETTINGS</b>

<b>Status:</b> <code>{thumb_status}</code>

<b>How to set:</b>
Send any image to the bot and it will be used as thumbnail for video uploads.

<i>Recommended size: 320x240 pixels</i>"""
    
    await callback_query.message.edit_text(text=text, reply_markup=keyboard)


async def back_to_main_settings(callback_query):
    """Return to main settings menu."""
    await send_settings_menu(client, callback_query.message, callback_query.message.id, False)


async def close_settings(callback_query):
    """Close settings menu."""
    await callback_query.message.delete()


# =============================================================================
# VIDEO SETTINGS HANDLERS
# =============================================================================
async def handle_split_setting(callback_query, data):
    """Handle split video setting."""
    value = data.split("-")[1] == "true"
    BOT.Options.is_split = value
    BOT.Setting.split_video = "Split Videos" if value else "Zip Videos"
    await show_video_settings(callback_query)


async def handle_convert_setting(callback_query, data):
    """Handle video conversion setting."""
    value = data.split("-")[1] == "true"
    BOT.Options.convert_video = value
    BOT.Setting.convert_video = "Yes" if value else "No"
    await show_video_settings(callback_query)


async def handle_format_setting(callback_query, format):
    """Handle video format setting."""
    BOT.Options.video_out = format
    await show_video_settings(callback_query)


async def handle_quality_setting(callback_query, data):
    """Handle conversion quality setting."""
    quality = data.split("-")[1]
    BOT.Setting.convert_quality = quality
    BOT.Options.convert_quality = quality == "High"
    await show_video_settings(callback_query)


# =============================================================================
# CAPTION STYLE HANDLER
# =============================================================================
async def handle_caption_style(callback_query, data):
    """Handle caption style selection."""
    parts = data.split("-")
    tag = parts[0]
    style_name = parts[1]
    
    BOT.Options.caption = tag
    BOT.Setting.caption_style = style_name
    
    await send_settings_menu(client, callback_query.message, callback_query.message.id, False)


# =============================================================================
# THUMBNAIL HANDLERS
# =============================================================================
async def delete_thumbnail(callback_query):
    """Delete custom thumbnail."""
    if BOT.Setting.thumbnail and os.path.exists(Paths.THMB_PATH):
        os.remove(Paths.THMB_PATH)
    
    BOT.Setting.thumbnail = False
    await send_settings_menu(client, callback_query.message, callback_query.message.id, False)


# =============================================================================
# UPLOAD MODE HANDLER
# =============================================================================
async def handle_upload_mode(callback_query, mode):
    """Handle upload mode selection."""
    BOT.Options.stream_upload = mode == "media"
    BOT.Setting.stream_upload = "Media" if mode == "media" else "Document"
    await send_settings_menu(client, callback_query.message, callback_query.message.id, False)


# =============================================================================
# PREFIX/SUFFIX/SPEED HANDLERS
# =============================================================================
async def set_prefix(callback_query):
    """Set filename prefix."""
    BOT.State.prefix = True
    await callback_query.message.edit_text(
        "<b>➕ SET PREFIX</b>\n\n<i>Send the text you want to add as prefix to filenames</i>\n\n<code>Example: [NEW]</code>\n\n<i>Reply to this message with your prefix</i>"
    )


async def set_suffix(callback_query):
    """Set filename suffix."""
    BOT.State.suffix = True
    await callback_query.message.edit_text(
        "<b>➖ SET SUFFIX</b>\n\n<i>Send the text you want to add as suffix to filenames</i>\n\n<code>Example: [1080p]</code>\n\n<i>Reply to this message with your suffix</i>"
    )


async def set_speed_limit(callback_query):
    """Set download speed limit."""
    BOT.State.speed_limit = True
    await callback_query.message.edit_text(
        "<b>⚡ SPEED LIMIT</b>\n\n<i>Enter speed limit in KB/s</i>\n\n<code>0 = Unlimited</code>\n<code>1024 = 1 MB/s</code>\n<code>5120 = 5 MB/s</code>\n\n<i>Reply with a number</i>"
    )


# =============================================================================
# HELP HANDLER
# =============================================================================
async def show_help(callback_query):
    """Show help message."""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬅️ Back", callback_data="back"),
        ],
    ])
    
    help_text = """<b>📖 LeechBot Pro - Help</b>

<b>🚀 Upload Commands:</b>
• /tupload - Leech to Telegram
• /gdupload - Mirror to Google Drive
• /drupload - Upload local directory
• /ytupload - Download from YouTube

<b>⚙️ Configuration:</b>
• /settings - Open settings
• /setname - Custom filename
• /zipaswd - Zip password
• /unzipaswd - Unzip password

<b>📝 Input Format:</b>
<code>link1
link2
[Custom Name]
{Zip Pass}
(Unzip Pass)</code>

<b>👨‍💻 Developer:</b> @Shineii86"""
    
    await callback_query.message.edit_text(text=help_text, reply_markup=keyboard)
