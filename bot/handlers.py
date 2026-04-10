# =============================================================================
# LeechBot Pro - Command Handlers
# =============================================================================
# Project   : Telegram Leech Bot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

import os
import logging
from pyrogram import filters
from datetime import datetime
from asyncio import sleep, get_event_loop

from colab_leecher import colab_bot, OWNER
from colab_leecher.utility.handler import cancel_task
from colab_leecher.utility.variables import BOT, MSG, BotTimes, Paths, Transfer
from colab_leecher.utility.task_manager import task_starter, task_scheduler
from colab_leecher.utility.helper import (
    is_valid_link, set_thumbnail, delete_messages, 
    send_settings_menu, format_size
)

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# =============================================================================
# START COMMAND
# =============================================================================
@colab_bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    """Handle /start command."""
    await message.delete()
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🌐 GitHub", url="https://github.com/Shineii86/LeechBot"),
            InlineKeyboardButton("📣 Channel", url="https://t.me/Shineii86"),
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="back"),
            InlineKeyboardButton("❓ Help", callback_data="help"),
        ],
    ])
    
    welcome_text = f"""<b>🚀 Welcome to LeechBot Pro v3.0!</b>

<i>Your ultimate file transfer companion</i>

<b>✨ What I can do:</b>
• 📥 Download from multiple sources
• 📤 Upload to Telegram or Google Drive
• 🎬 Convert and process videos
• 📂 Extract and create archives
• ✂️ Split large files automatically

<b>📚 Quick Start:</b>
• /tupload - Leech to Telegram
• /gdupload - Mirror to Google Drive
• /ytupload - Download from YouTube
• /settings - Configure preferences

<b>👨‍💻 Developer:</b> <a href='https://github.com/Shineii86'>Shinei Nouzen</a>
"""
    
    await message.reply_text(welcome_text, reply_markup=keyboard)


# =============================================================================
# UPLOAD COMMANDS
# =============================================================================
@colab_bot.on_message(filters.command("tupload") & filters.private)
async def telegram_upload_handler(client, message):
    """Handle /tupload command - Leech to Telegram."""
    global BOT
    
    BOT.Mode.mode = "leech"
    BOT.Mode.ytdl = False
    
    text = """<b>📤 TELEGRAM UPLOAD MODE</b>

<b>Send me download link(s):</b>

<code>https://example.com/file1.zip
https://example.com/file2.mp4</code>

<b>📝 Optional parameters:</b>
• <code>[Custom Name.mp4]</code> - Set custom filename
• <code>{zip_password}</code> - Password for zip
• <code>(unzip_password)</code> - Password for extraction

<i>Waiting for your links...</i>"""
    
    MSG.src_request_msg = await task_starter(message, text)


@colab_bot.on_message(filters.command("gdupload") & filters.private)
async def drive_upload_handler(client, message):
    """Handle /gdupload command - Mirror to Google Drive."""
    global BOT
    
    BOT.Mode.mode = "mirror"
    BOT.Mode.ytdl = False
    
    text = """<b>☁️ GOOGLE DRIVE MIRROR MODE</b>

<b>Send me download link(s):</b>

<code>https://example.com/file1.zip
https://drive.google.com/file/d/xxxxx</code>

<b>📝 Optional parameters:</b>
• <code>[Custom Name.mp4]</code> - Set custom filename
• <code>{zip_password}</code> - Password for zip
• <code>(unzip_password)</code> - Password for extraction

<i>Waiting for your links...</i>"""
    
    MSG.src_request_msg = await task_starter(message, text)


@colab_bot.on_message(filters.command("drupload") & filters.private)
async def directory_upload_handler(client, message):
    """Handle /drupload command - Upload local directory."""
    global BOT
    
    BOT.Mode.mode = "dir-leech"
    BOT.Mode.ytdl = False
    
    text = """<b>📂 DIRECTORY UPLOAD MODE</b>

<b>Send me the folder path:</b>

<code>/home/user/Downloads/my_folder</code>
<code>/content/downloads/files</code>

<i>Waiting for path...</i>"""
    
    MSG.src_request_msg = await task_starter(message, text)


@colab_bot.on_message(filters.command("ytupload") & filters.private)
async def youtube_upload_handler(client, message):
    """Handle /ytupload command - Download from YouTube."""
    global BOT
    
    BOT.Mode.mode = "leech"
    BOT.Mode.ytdl = True
    
    text = """<b>🎬 YOUTUBE/YT-DLP MODE</b>

<b>Send me video link(s):</b>

<code>https://youtube.com/watch?v=xxxxx
https://youtu.be/xxxxx</code>

<b>✨ Supported sites:</b>
• YouTube, Facebook, Instagram
• Twitter/X, TikTok, Vimeo
• And 1000+ more sites!

<b>📝 Optional:</b>
• <code>[Custom Name.mp4]</code> - Set custom filename
• <code>{zip_password}</code> - Password for zip

<i>Waiting for your links...</i>"""
    
    MSG.src_request_msg = await task_starter(message, text)


# =============================================================================
# SETTINGS COMMAND
# =============================================================================
@colab_bot.on_message(filters.command("settings") & filters.private)
async def settings_handler(client, message):
    """Handle /settings command."""
    if message.chat.id != OWNER:
        await message.reply_text("<b>⛔️ You are not authorized!</b>")
        return
    
    await message.delete()
    await send_settings_menu(client, message, message.id, True)


# =============================================================================
# CUSTOM COMMANDS
# =============================================================================
@colab_bot.on_message(filters.command("setname") & filters.private)
async def setname_handler(client, message):
    """Handle /setname command."""
    global BOT
    
    if len(message.command) < 2:
        msg = await message.reply_text(
            "<b>❌ Usage:</b>\n<code>/setname custom_filename.ext</code>\n\n<i>Set a custom filename for the next download</i>"
        )
    else:
        BOT.Options.custom_name = message.command[1]
        msg = await message.reply_text(
            f"<b>✅ Custom name set:</b>\n<code>{BOT.Options.custom_name}</code>"
        )
    
    await sleep(15)
    await delete_messages(message, msg)


@colab_bot.on_message(filters.command("zipaswd") & filters.private)
async def zip_password_handler(client, message):
    """Handle /zipaswd command."""
    global BOT
    
    if len(message.command) < 2:
        msg = await message.reply_text(
            "<b>❌ Usage:</b>\n<code>/zipaswd your_password</code>\n\n<i>Set password for output zip file</i>"
        )
    else:
        BOT.Options.zip_password = message.command[1]
        msg = await message.reply_text(
            "<b>✅ Zip password set!</b>\n<i>Next archive will be password protected</i>"
        )
    
    await sleep(15)
    await delete_messages(message, msg)


@colab_bot.on_message(filters.command("unzipaswd") & filters.private)
async def unzip_password_handler(client, message):
    """Handle /unzipaswd command."""
    global BOT
    
    if len(message.command) < 2:
        msg = await message.reply_text(
            "<b>❌ Usage:</b>\n<code>/unzipaswd your_password</code>\n\n<i>Set password for extracting archives</i>"
        )
    else:
        BOT.Options.unzip_password = message.command[1]
        msg = await message.reply_text(
            "<b>✅ Unzip password set!</b>\n<i>Will use this password for extraction</i>"
        )
    
    await sleep(15)
    await delete_messages(message, msg)


# =============================================================================
# STATS COMMAND
# =============================================================================
@colab_bot.on_message(filters.command("stats") & filters.private)
async def stats_handler(client, message):
    """Handle /stats command."""
    if message.chat.id != OWNER:
        return
    
    uptime = datetime.now() - BotTimes.session_start
    
    stats_text = f"""<b>📊 BOT STATISTICS</b>

╔════════════════════════════════════╗
║  <b>Session Stats</b>                 ║
╠════════════════════════════════════╣
║  ⏱️ Uptime: <code>{str(uptime).split('.')[0]}</code>
║  ✅ Success: <code>{Transfer.success_count}</code>
║  ❌ Failed: <code>{Transfer.failed_count}</code>
╠════════════════════════════════════╣
║  <b>Data Transfer</b>                 ║
╠════════════════════════════════════╣
║  ⬇️ Downloaded: <code>{format_size(Transfer.total_down_bytes)}</code>
║  ⬆️ Uploaded: <code>{format_size(Transfer.total_up_bytes)}</code>
╚════════════════════════════════════╝
"""
    
    await message.reply_text(stats_text)


# =============================================================================
# HELP COMMAND
# =============================================================================
@colab_bot.on_message(filters.command("help") & filters.private)
async def help_handler(client, message):
    """Handle /help command."""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🌐 GitHub", url="https://github.com/Shineii86/LeechBot"),
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Shineii86"),
        ],
    ])
    
    help_text = """<b>📖 LeechBot Pro - Command Guide</b>

<b>🚀 Upload Commands:</b>
• /tupload - Leech files to Telegram
• /gdupload - Mirror files to Google Drive
• /drupload - Upload local directory
• /ytupload - Download from YouTube/Supported sites

<b>⚙️ Configuration:</b>
• /settings - Open settings menu
• /setname - Set custom filename
• /zipaswd - Set zip password
• /unzipaswd - Set unzip password

<b>📊 Information:</b>
• /start - Start the bot
• /help - Show this help message
• /stats - View download statistics
• /cancel - Cancel current task

<b>📝 Input Format:</b>
<code>https://link1.com/file.zip
https://link2.com/file.mp4
[Custom Name.mp4]
{Zip Password}
(Unzip Password)</code>

<b>👨‍💻 Developer:</b> <a href='https://t.me/Shineii86'>@Shineii86</a>
"""
    
    await message.reply_text(help_text, reply_markup=keyboard)


# =============================================================================
# CANCEL COMMAND
# =============================================================================
@colab_bot.on_message(filters.command("cancel") & filters.private)
async def cancel_handler(client, message):
    """Handle /cancel command."""
    if BOT.State.task_going:
        await cancel_task("Cancelled by user")
    else:
        msg = await message.reply_text("<b>ℹ️ No active task to cancel</b>")
        await sleep(5)
        await delete_messages(message, msg)


# =============================================================================
# LINK HANDLER
# =============================================================================
@colab_bot.on_message(filters.create(is_valid_link) & ~filters.photo)
async def link_handler(client, message):
    """Handle incoming download links."""
    global BOT
    
    # Reset options
    BOT.Options.custom_name = ""
    BOT.Options.zip_password = ""
    BOT.Options.unzip_password = ""
    
    # Delete source request message
    if MSG.src_request_msg:
        await MSG.src_request_msg.delete()
    
    # Check if ready to process
    if not BOT.State.task_going and BOT.State.started:
        links = message.text.splitlines()
        
        # Parse options from end of message
        for _ in range(3):
            if not links:
                break
                
            last_line = links[-1].strip()
            
            if last_line.startswith("[") and last_line.endswith("]"):
                BOT.Options.custom_name = last_line[1:-1]
                links.pop()
            elif last_line.startswith("{") and last_line.endswith("}"):
                BOT.Options.zip_password = last_line[1:-1]
                links.pop()
            elif last_line.startswith("(") and last_line.endswith(")"):
                BOT.Options.unzip_password = last_line[1:-1]
                links.pop()
            else:
                break
        
        BOT.SOURCE = links
        
        # Show mode selection
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📄 Normal", callback_data="normal")],
            [
                InlineKeyboardButton("🗜️ Compress", callback_data="zip"),
                InlineKeyboardButton("📂 Extract", callback_data="unzip"),
            ],
            [InlineKeyboardButton("🔄 Unzip & Zip", callback_data="undzip")],
        ])
        
        mode_text = f"""<b>🎯 SELECT PROCESSING MODE</b>

<b>Current task:</b> <code>{BOT.Mode.mode.capitalize()}</code>

<b>Options:</b>
• 📄 <b>Normal</b> - Upload as-is
• 🗜️ <b>Compress</b> - Zip before upload
• 📂 <b>Extract</b> - Unzip archives first
• 🔄 <b>Unzip & Zip</b> - Extract then re-compress

<i>Choose how to process your files...</i>"""
        
        await message.reply_text(mode_text, reply_markup=keyboard, quote=True)
        
    elif BOT.State.started:
        await message.delete()
        msg = await message.reply_text(
            "<b>⏳ Please Wait!</b>\n\n<i>I'm already processing a task. Please wait until it completes.</i>"
        )
        await sleep(10)
        await delete_messages(message, msg)


# =============================================================================
# THUMBNAIL HANDLER
# =============================================================================
@colab_bot.on_message(filters.photo & filters.private)
async def thumbnail_handler(client, message):
    """Handle photo uploads for thumbnail."""
    msg = await message.reply_text("<i>🖼️ Processing thumbnail...</i>")
    
    success = await set_thumbnail(message)
    
    if success:
        await msg.edit_text("<b>✅ Thumbnail updated successfully!</b>")
        await message.delete()
    else:
        await msg.edit_text("<b>❌ Failed to set thumbnail</b>\n<i>Please try again with a different image</i>")
    
    await sleep(10)
    await delete_messages(message, msg)


# =============================================================================
# PREFIX/SUFFIX HANDLER
# =============================================================================
@colab_bot.on_message(filters.reply)
async def reply_handler(client, message):
    """Handle reply messages for settings."""
    global BOT
    
    if BOT.State.prefix:
        BOT.Setting.prefix = message.text
        BOT.State.prefix = False
        await send_settings_menu(client, message, message.reply_to_message_id, False)
        await message.delete()
        
    elif BOT.State.suffix:
        BOT.Setting.suffix = message.text
        BOT.State.suffix = False
        await send_settings_menu(client, message, message.reply_to_message_id, False)
        await message.delete()
        
    elif BOT.State.speed_limit:
        try:
            limit = int(message.text)
            BOT.Setting.speed_limit = max(0, limit)
        except ValueError:
            pass
        BOT.State.speed_limit = False
        await send_settings_menu(client, message, message.reply_to_message_id, False)
        await message.delete()
