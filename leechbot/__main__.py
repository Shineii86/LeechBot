# =============================================================================
# Telegram Leech Bot - Command Handlers and Entry Point
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================
# License   : MIT License
# You may use, modify, and distribute this code under the MIT License.
# Please retain this header when using or modifying the code.
# =============================================================================

"""
LeechBot command handlers and entry point

This module contains all Telegram bot command handlers, callback queries,
and the main bot execution loop. It handles user interactions
and orchestrates the download and upload processes.
"""

import logging
import os
from pyrogram import filters
from datetime import datetime
from asyncio import sleep, get_event_loop, create_task
from leechbot import leechbot, OWNER
from leechbot.utility.handler import cancelTask
from leechbot.utility.variables import BOT, MSG, BotTimes, Paths
from leechbot.utility.task_manager import taskScheduler, task_starter, process_next_in_queue
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from leechbot.utility.helper import (
    isLink, setThumbnail, message_deleter, send_settings,
    sysINFO, sysINFO_full, status_keyboard, sizeUnit
)

logger = logging.getLogger(__name__)

src_request_msg = None

WELCOME_TEXT = """
**🤖 Leech Bot** — *Advanced Telegram File Transloader*

◈ **💪 Powerful • 🚀 Fast • 🔰 Secure**

───────────────────────────

**📥 Download From Anywhere**
`•` Direct Links, Google Drive, Telegram
`•` YouTube, Facebook, Instagram & 2000+ sites
`•` Terabox, Mega (soon)

**📤 Uploaded To Premium Destination**
`•` Telegram (Unlimited Storage)
`•` Google Drive (Mirror Mode)
`•` Local Directory Leech

**🛠️ Advance Tools**
`•` Video Converter (GPU Accelerated)
`•` Archive Extractor (Zip, Rar, 7z)
`•` Smart Splitting For Large Files
`•` Custom Thumbnails & Captions
`•` Task Queue & Resume Downloads

───────────────────────────

**📋 Quick Commands**
`/tupload` — Upload To Telegram
`/gdupload` — Mirror To Google Drive
`/ytupload` — Download With Yt‑Dlp
`/queue` — View Pending Tasks
`/resume` — Resume Interrupted Downloads
`/settings` — Configure Bot Preferences
`/about` — Bot Information

───────────────────────────

**🧑‍💻 Developer:** [Shinei Nouzen](https://t.me/Shineii86)
"""

# =============================================================================
# Check for Resumable Session on Startup
# =============================================================================
async def check_resume_session():
    if os.path.exists(Paths.ARIA2_SESSION):
        try:
            with open(Paths.ARIA2_SESSION, "r") as f:
                lines = f.readlines()
            if lines:
                await leechbot.send_message(
                    OWNER,
                    "**🔄 Interrupted downloads detected!**\nUse `/resume` to continue or `/clear_resume` to discard."
                )
        except Exception:
            pass

# =============================================================================
# Bot Commands
# =============================================================================
@leechbot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.delete()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📂 GitHub Repository ✨", url="https://github.com/Shineii86/LeechBot")],
        [InlineKeyboardButton("🔔 Updates", url="https://t.me/MaximXBots"),
         InlineKeyboardButton("Support 💬", url="https://t.me/MaximXGroup")],
        [InlineKeyboardButton("🤖 Bot Settings ⚙️", callback_data="settings_menu")]
    ])
    await message.reply_text(WELCOME_TEXT, reply_markup=keyboard, disable_web_page_preview=True)

@leechbot.on_message(filters.command("tupload") & filters.private)
async def telegram_upload_command(client, message):
    global BOT, src_request_msg
    BOT.Mode.mode = "leech"
    BOT.Mode.ytdl = False
    text = """**⚡ Send Download Link(s)** 🔗

📋 **Follow The Pattern Below:**

<code>https://example.com/file1.mp4
https://example.com/file2.mp4
[Custom Name.mp4]
{Zip Password}
(Unzip Password)</code>

**💡 Tips:**
• Multiple Links Supported
• Use [] For Custom Filename
• Use {} For Zip Password
• Use () For Extract Password"""
    src_request_msg = await task_starter(message, text)

@leechbot.on_message(filters.command("gdupload") & filters.private)
async def gdrive_upload_command(client, message):
    global BOT, src_request_msg
    BOT.Mode.mode = "mirror"
    BOT.Mode.ytdl = False
    text = """**⚡ Send Download Link(s)** 🔗

📋 **Follow The Pattern Below:**

<code>https://example.com/file1.mp4
https://example.com/file2.mp4
[Custom Name.mp4]
{Zip Password}
(Unzip Password)</code>

**💡 Tips:**
• Multiple Links Supported
• Files Will Be Mirrored To Your Gdrive
• Make Sure Gdrive Is Mounted"""
    src_request_msg = await task_starter(message, text)

@leechbot.on_message(filters.command("drupload") & filters.private)
async def directory_upload_command(client, message):
    global BOT, src_request_msg
    BOT.Mode.mode = "dir-leech"
    BOT.Mode.ytdl = False
    text = """**⚡ Send Folder Path** 📁

📋 **Example:**

<code>/home/user/Downloads/myfolder</code>

**💡 Note:**
• Provide Absolute Path To The Folder
• Ensure The Bot Has Read Permissions"""
    src_request_msg = await task_starter(message, text)

@leechbot.on_message(filters.command("ytupload") & filters.private)
async def ytdl_upload_command(client, message):
    global BOT, src_request_msg
    BOT.Mode.mode = "leech"
    BOT.Mode.ytdl = True
    text = """**⚡ Send Yt-Dlp Link(s)** 🔗

📋 **Follow The Pattern Below:**

<code>https://youtube.com/watch?v=xxxxx
https://youtu.be/xxxxx
[Custom Name.mp4]
{Zip Password}</code>

**💡 Supported Sites:**
• Youtube, Facebook, Instagram
• Twitter, Tiktok, And More..."""
    src_request_msg = await task_starter(message, text)

@leechbot.on_message(filters.command("settings") & filters.private)
async def settings_command(client, message):
    if message.chat.id == OWNER:
        await message.delete()
        await send_settings(client, message, message.id, True)

@leechbot.on_message(filters.command("queue") & filters.private)
async def queue_command(client, message):
    if not BOT.TASK_QUEUE:
        await message.reply_text("**📋 Task queue is empty.**")
    else:
        text = "**📋 Pending Tasks:**\n"
        for i, (_, _, sources, mode, ytdl, _) in enumerate(BOT.TASK_QUEUE, 1):
            text += f"\n{i}. `{mode.upper()}` ({'YT-DLP' if ytdl else 'Direct'}) - {len(sources)} link(s)"
        await message.reply_text(text)

@leechbot.on_message(filters.command("resume") & filters.private)
async def resume_command(client, message):
    if not os.path.exists(Paths.ARIA2_SESSION):
        await message.reply_text("**ℹ️ No interrupted downloads found.**")
        return
    with open(Paths.ARIA2_SESSION, "r") as f:
        lines = f.readlines()
    if not lines:
        await message.reply_text("**ℹ️ No interrupted downloads found.**")
        return
    BOT.Mode.mode = "leech"
    BOT.Mode.type = "normal"
    BOT.Mode.ytdl = False
    BOT.SOURCE = ["resume_session"]
    BOT.State.started = True
    MSG.status_msg = await leechbot.send_message(
        OWNER, "**🔄 Resuming interrupted downloads...**",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="cancel")]])
    )
    BOT.State.task_going = True
    BotTimes.start_time = datetime.now()
    event_loop = get_event_loop()
    BOT.TASK = event_loop.create_task(taskScheduler(resume=True))
    try:
        await BOT.TASK
    finally:
        BOT.State.task_going = False

@leechbot.on_message(filters.command("clear_resume") & filters.private)
async def clear_resume_command(client, message):
    if os.path.exists(Paths.ARIA2_SESSION):
        os.remove(Paths.ARIA2_SESSION)
        await message.reply_text("**✅ Resume session cleared.**")
    else:
        await message.reply_text("**ℹ️ No resume session found.**")

@leechbot.on_message(filters.command("about") & filters.private)
async def about_command(client, message):
    about_text = """
**🤖 About LeechBot**

**Version:** `0.3`
**Build Date:** `2026-04-11`
**License:** `MIT`

───────────────────────────

**🧑‍💻 Developer**
[Shinei Nouzen](https://t.me/Shineii86)
GitHub: [Shineii86](https://github.com/Shineii86)

───────────────────────────

**📣 Updates & Support**
• **Updates Channel:** [@MaximXBots](https://t.me/MaximXBots)
• **Support Group:** [@MaximXGroup](https://t.me/MaximXGroup)
• **Source Code:** [GitHub Repository](https://github.com/Shineii86/LeechBot)

───────────────────────────

**💡 Acknowledgements**
Based on the original work by [XronTrix10](https://github.com/XronTrix10/Telegram-Leecher) and enhanced with features like Task Queue, Resume Downloads, Duplicate Detection, and Speed Limiter.

**⚠️ Disclaimer**
This bot is intended for educational purposes. Do not use it to download copyrighted content without permission. The developer assumes no liability for misuse.
"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📂 GitHub Repository", url="https://github.com/Shineii86/LeechBot")],
        [InlineKeyboardButton("🔔 Updates Channel", url="https://t.me/MaximXBots"),
         InlineKeyboardButton("Support Group 💬", url="https://t.me/MaximXGroup")],
        [InlineKeyboardButton("🧑‍💻 Developer", url="https://t.me/Shineii86")]
    ])
    msg = await message.reply_text(about_text, reply_markup=keyboard, disable_web_page_preview=True)
    await message_deleter(message, msg)

@leechbot.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    help_text = """**📖 Leechbot Help Menu**

**Available Commands:**

/start - Start The Bot
/tupload - Upload To Telegram
/gdupload - Mirror To Google Drive
/drupload - Upload Local Directory
/ytupload - Download With Yt-Dlp
/settings - Bot Settings
/setname - Set Custom Filename
/zipaswd - Set Zip Password
/unzipaswd - Set Unzip Password
/queue - View Task Queue
/resume - Resume Interrupted Downloads
/clear_resume - Clear Resume Session
/about - About This Bot
/help - Show This Help Message

**🖼️ Thumbnail:**
Send Any Image To Set It As Thumbnail"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📂 GitHub Repository ✨", url="https://github.com/Shineii86/LeechBot")],
        [InlineKeyboardButton("🔔 Updates", url="https://t.me/MaximXBots"),
         InlineKeyboardButton("Support 💬", url="https://t.me/MaximXGroup")],
        [InlineKeyboardButton("🧑‍💻 Developer ✨", url="https://t.me/Shineii86")]
    ])
    msg = await message.reply_text(help_text, reply_markup=keyboard)
    await message_deleter(message, msg)

@leechbot.on_message(filters.command("setname") & filters.private)
async def setname_command(client, message):
    global BOT
    if len(message.command) < 2:
        msg = await message.reply_text("**⚠️ Usage:**\n`/setname <filename.extension>`\n\n**Example:**\n`/setname myvideo.mp4`", quote=True)
    else:
        BOT.Options.custom_name = " ".join(message.command[1:])
        msg = await message.reply_text(f"**✅ Custom Name Set:**\n`{BOT.Options.custom_name}`", quote=True)
    await message_deleter(message, msg)

@leechbot.on_message(filters.command("zipaswd") & filters.private)
async def zipaswd_command(client, message):
    global BOT
    if len(message.command) != 2:
        msg = await message.reply_text("**⚠️ Usage:**\n`/zipaswd <password>`\n\n**Example:**\n`/zipaswd mypassword123`", quote=True)
    else:
        BOT.Options.zip_pswd = message.command[1]
        msg = await message.reply_text("**🔐 Zip Password Set Successfully**", quote=True)
    await message_deleter(message, msg)

@leechbot.on_message(filters.command("unzipaswd") & filters.private)
async def unzipaswd_command(client, message):
    global BOT
    if len(message.command) != 2:
        msg = await message.reply_text("**⚠️ Usage:**\n`/unzipaswd <password>`\n\n**Example:**\n`/unzipaswd mypassword123`", quote=True)
    else:
        BOT.Options.unzip_pswd = message.command[1]
        msg = await message.reply_text("**🔓 Unzip Password Set Successfully**", quote=True)
    await message_deleter(message, msg)

@leechbot.on_message(filters.command("stats") & filters.private)
async def stats_command(client, message):
    stats_text = f"**📊 Bot Statistics**{sysINFO()}"
    msg = await message.reply_text(stats_text, quote=True)
    await message_deleter(message, msg)

@leechbot.on_message(filters.command("cancel") & filters.private)
async def cancel_command(client, message):
    if BOT.State.task_going:
        await cancelTask("User cancelled the task")
        msg = await message.reply_text("**🚫 Task Cancelled**", quote=True)
    else:
        msg = await message.reply_text("**⚠️ No Active Task To Cancel**", quote=True)
    await message_deleter(message, msg)

# =============================================================================
# Reply Handlers
# =============================================================================
@leechbot.on_message(filters.reply)
async def handle_reply(client, message):
    global BOT
    if BOT.State.prefix:
        BOT.Setting.prefix = message.text
        BOT.State.prefix = False
        BOT.Setting.save()
        await send_settings(client, message, message.reply_to_message_id, False)
        await message.delete()
    elif BOT.State.suffix:
        BOT.Setting.suffix = message.text
        BOT.State.suffix = False
        BOT.Setting.save()
        await send_settings(client, message, message.reply_to_message_id, False)
        await message.delete()
    elif BOT.State.setting_autodelete_delay:
        try:
            delay = int(message.text.strip())
            if 5 <= delay <= 300:
                BOT.Setting.auto_delete_delay = delay
                BOT.State.setting_autodelete_delay = False
                BOT.Setting.save()
                await message.reply_text(f"**✅ Auto-delete delay set to {delay} seconds.**")
                fake_cb = type('obj', (object,), {'message': message, 'data': 'autodelete'})
                await handle_callback(client, fake_cb)
            else:
                await message.reply_text("**⚠️ Please enter a number between 5 and 300.**")
        except ValueError:
            await message.reply_text("**⚠️ Invalid number. Please try again.**")
        await message.delete()
    elif BOT.State.setting_download_limit:
        try:
            val = message.text.strip().upper()
            if val in ("0", "UNLIMITED"):
                BOT.Setting.download_speed_limit = 0
            else:
                num = float(''.join(filter(str.isdigit, val)) or 0)
                if 'G' in val:
                    num *= 1024**3
                elif 'M' in val:
                    num *= 1024**2
                elif 'K' in val:
                    num *= 1024
                BOT.Setting.download_speed_limit = int(num)
            BOT.State.setting_download_limit = False
            BOT.Setting.save()
            await message.reply_text("**✅ Download speed limit set.**")
            fake_cb = type('obj', (object,), {'message': message, 'data': 'speed_limit'})
            await handle_callback(client, fake_cb)
        except Exception:
            await message.reply_text("**⚠️ Invalid format. Use e.g., 10M, 500K, or 0 for unlimited.**")
        await message.delete()
    elif BOT.State.setting_upload_limit:
        try:
            val = message.text.strip().upper()
            if val in ("0", "UNLIMITED"):
                BOT.Setting.upload_speed_limit = 0
            else:
                num = float(''.join(filter(str.isdigit, val)) or 0)
                if 'G' in val:
                    num *= 1024**3
                elif 'M' in val:
                    num *= 1024**2
                elif 'K' in val:
                    num *= 1024
                BOT.Setting.upload_speed_limit = int(num)
            BOT.State.setting_upload_limit = False
            BOT.Setting.save()
            await message.reply_text("**✅ Upload speed limit set.**")
            fake_cb = type('obj', (object,), {'message': message, 'data': 'speed_limit'})
            await handle_callback(client, fake_cb)
        except Exception:
            await message.reply_text("**⚠️ Invalid format. Use e.g., 10M, 500K, or 0 for unlimited.**")
        await message.delete()

# =============================================================================
# Link Handler (now supports queue)
# =============================================================================
@leechbot.on_message(filters.create(isLink) & ~filters.photo)
async def handle_url(client, message):
    global BOT, src_request_msg
    BOT.Options.custom_name = ""
    BOT.Options.zip_pswd = ""
    BOT.Options.unzip_pswd = ""
    if src_request_msg:
        await src_request_msg.delete()
    if not BOT.State.task_going and BOT.State.started:
        temp_source = message.text.splitlines()
        for _ in range(3):
            if not temp_source:
                break
            if temp_source[-1][0] == "[":
                BOT.Options.custom_name = temp_source[-1][1:-1]
                temp_source.pop()
            elif temp_source[-1][0] == "{":
                BOT.Options.zip_pswd = temp_source[-1][1:-1]
                temp_source.pop()
            elif temp_source[-1][0] == "(":
                BOT.Options.unzip_pswd = temp_source[-1][1:-1]
                temp_source.pop()
            else:
                break
        BOT.SOURCE = temp_source
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📄 Regular ✨", callback_data="normal")],
            [InlineKeyboardButton("🗜️ Compress", callback_data="zip"),
             InlineKeyboardButton("Extract 📂", callback_data="unzip")],
            [InlineKeyboardButton("🔄 Unzip+Zip ✨", callback_data="undzip")]
        ])
        mode_text = BOT.Mode.mode.capitalize()
        options_text = f"""**🎯 Select Upload Type For {mode_text}**

📄 **Regular** - Normal File Upload
🗜️ **Compress** - Zip File Upload
📂 **Extract** - Extract Archive Before Upload
🔄 **Unzip+Zip** - Extract Then Compress"""
        await message.reply_text(text=options_text, reply_markup=keyboard, quote=True)
    elif BOT.State.started:
        BOT.TASK_QUEUE.append((
            message.chat.id, message, BOT.SOURCE.copy() if BOT.SOURCE else temp_source,
            BOT.Mode.mode, BOT.Mode.ytdl, BOT.Mode.type
        ))
        await message.reply_text(f"**📋 Added to queue. Position: {len(BOT.TASK_QUEUE)}**")
        if not BOT.State.task_going:
            await process_next_in_queue(client)

# =============================================================================
# Callback Query Handler (expanded)
# =============================================================================
@leechbot.on_callback_query()
async def handle_callback(client, callback_query):
    global BOT, MSG
    data = callback_query.data
    if data in ["normal", "zip", "unzip", "undzip"]:
        BOT.Mode.type = data
        await callback_query.message.delete()
        await leechbot.delete_messages(
            chat_id=callback_query.message.chat.id,
            message_ids=callback_query.message.reply_to_message_id
        )
        MSG.status_msg = await leechbot.send_message(
            chat_id=OWNER,
            text="**🚀 Initializing Task...**\n\nPlease Wait While I Prepare Your Download",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚫 Cancel", callback_data="cancel")]])
        )
        BOT.State.task_going = True
        BOT.State.started = False
        BotTimes.start_time = datetime.now()
        event_loop = get_event_loop()
        BOT.TASK = event_loop.create_task(taskScheduler())
        try:
            await BOT.TASK
        finally:
            BOT.State.task_going = False
            if BOT.TASK_QUEUE:
                await process_next_in_queue(client)
    elif data == "settings_menu":
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    elif data == "video":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✂️ Split", callback_data="split-true"),
             InlineKeyboardButton("Zip 🗜️", callback_data="split-false")],
            [InlineKeyboardButton("🔄 Convert", callback_data="convert-true"),
             InlineKeyboardButton("Skip ⏭️", callback_data="convert-false")],
            [InlineKeyboardButton("🎬 Mp4", callback_data="mp4"),
             InlineKeyboardButton("Mkv 📼", callback_data="mkv")],
            [InlineKeyboardButton("👍 High Quality", callback_data="q-High"),
             InlineKeyboardButton("Low Quality 👎", callback_data="q-Low")],
            [InlineKeyboardButton("❰ Back", callback_data="back")]
        ])
        await callback_query.message.edit_text(
            f"**⚙️ Video Settings**\n\n┏🔄 **Convert:** `{BOT.Setting.convert_video}`\n┣✂️ **Split:** `{BOT.Setting.split_video}`\n┣🎬 **Format:** `{BOT.Options.video_out}`\n┗🔴 **Quality:** `{BOT.Setting.convert_quality}`",
            reply_markup=keyboard
        )
    elif data == "caption":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("<code>Monospace</code>", callback_data="code-Monospace"),
             InlineKeyboardButton("**Bold**", callback_data="b-Bold")],
            [InlineKeyboardButton("__Italic__", callback_data="i-Italic"),
             InlineKeyboardButton("__Underline__", callback_data="u-Underlined")],
            [InlineKeyboardButton("Regular", callback_data="p-Regular")],
            [InlineKeyboardButton("❰ Back", callback_data="back")]
        ])
        await callback_query.message.edit_text(
            "**📝 Caption Font Style**\n\n<code>Monospace</code>\nRegular\n**Bold**\n__Italic__\n__Underline__",
            reply_markup=keyboard
        )
    elif data == "thumb":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🗑️ Delete Thumbnail", callback_data="del-thumb")],
            [InlineKeyboardButton("❰ Back", callback_data="back")]
        ])
        thmb_status = "✅ Set" if BOT.Setting.thumbnail else "🚫 None"
        await callback_query.message.edit_text(
            f"**🖼️ Thumbnail Settings**\n\n**Status:** {thmb_status}\n\n💡 Send An Image To Set As Thumbnail",
            reply_markup=keyboard
        )
    elif data == "del-thumb":
        if BOT.Setting.thumbnail and os.path.exists(Paths.THMB_PATH):
            os.remove(Paths.THMB_PATH)
        BOT.Setting.thumbnail = False
        BOT.Setting.save()
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    elif data == "set-prefix":
        await callback_query.message.edit_text("**⌨️ Send Text To Set As Prefix**\n\nReply To This Message With Your Prefix")
        BOT.State.prefix = True
    elif data == "set-suffix":
        await callback_query.message.edit_text("**⌨️ Send Text To Set As Suffix**\n\nReply To This Message With Your Suffix")
        BOT.State.suffix = True
    elif data in ["code-Monospace", "p-Regular", "b-Bold", "i-Italic", "u-Underlined"]:
        res = data.split("-")
        BOT.Options.caption = res[0]
        BOT.Setting.caption = res[1]
        BOT.Setting.save()
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    elif data in ["split-true", "split-false"]:
        BOT.Options.is_split = data == "split-true"
        BOT.Setting.split_video = "Split" if data == "split-true" else "Zip"
        BOT.Setting.save()
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    elif data in ["convert-true", "convert-false"]:
        BOT.Options.convert_video = data == "convert-true"
        BOT.Setting.convert_video = "Yes" if data == "convert-true" else "No"
        BOT.Setting.save()
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    elif data in ["mp4", "mkv"]:
        BOT.Options.video_out = data
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    elif data in ["q-High", "q-Low"]:
        BOT.Setting.convert_quality = data.split("-")[-1]
        BOT.Options.convert_quality = BOT.Setting.convert_quality == "High"
        BOT.Setting.save()
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    elif data in ["media", "document"]:
        BOT.Options.stream_upload = data == "media"
        BOT.Setting.stream_upload = "Media" if data == "media" else "Document"
        BOT.Setting.save()
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    elif data == "autodelete":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"✅ Auto-Delete: {'ON' if BOT.Setting.auto_delete else 'OFF'}", callback_data="toggle_autodelete")],
            [InlineKeyboardButton("⏱️ Set Delay", callback_data="set_autodelete_delay")],
            [InlineKeyboardButton("❰ Back", callback_data="back")]
        ])
        await callback_query.message.edit_text(
            f"**⏳ Auto-Delete Messages**\n\n**Status:** {'Enabled' if BOT.Setting.auto_delete else 'Disabled'}\n**Delay:** {BOT.Setting.auto_delete_delay} seconds",
            reply_markup=keyboard
        )
    elif data == "toggle_autodelete":
        BOT.Setting.auto_delete = not BOT.Setting.auto_delete
        BOT.Setting.save()
        await handle_callback(client, callback_query)
    elif data == "set_autodelete_delay":
        await callback_query.message.edit_text(
            "**⏱️ Send the delay in seconds**\n\nReply to this message with a number between 5 and 300.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❰ Back", callback_data="autodelete")]])
        )
        BOT.State.setting_autodelete_delay = True
    elif data == "speed_limit":
        down_limit = f"{sizeUnit(BOT.Setting.download_speed_limit)}/s" if BOT.Setting.download_speed_limit else "Unlimited"
        up_limit = f"{sizeUnit(BOT.Setting.upload_speed_limit)}/s" if BOT.Setting.upload_speed_limit else "Unlimited"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"⬇️ DL Limit: {down_limit}", callback_data="set_download_limit")],
            [InlineKeyboardButton(f"⬆️ UL Limit: {up_limit}", callback_data="set_upload_limit")],
            [InlineKeyboardButton("❰ Back", callback_data="back")]
        ])
        await callback_query.message.edit_text(
            "**⚡ Speed Limit Settings**\n\nSet limits in format like `10M` or `500K`. Use `0` or `unlimited` to disable.",
            reply_markup=keyboard
        )
    elif data == "set_download_limit":
        await callback_query.message.edit_text(
            "**⬇️ Send download speed limit**\n\nExamples: `10M`, `500K`, `0` (unlimited)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❰ Back", callback_data="speed_limit")]])
        )
        BOT.State.setting_download_limit = True
    elif data == "set_upload_limit":
        await callback_query.message.edit_text(
            "**⬆️ Send upload speed limit**\n\nExamples: `10M`, `500K`, `0` (unlimited)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❰ Back", callback_data="speed_limit")]])
        )
        BOT.State.setting_upload_limit = True
    elif data == "close":
        await callback_query.message.delete()
    elif data == "back":
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    elif data in ["ytdl-true", "ytdl-false"]:
        BOT.Mode.ytdl = data == "ytdl-true"
        await callback_query.message.delete()
        await leechbot.delete_messages(
            chat_id=callback_query.message.chat.id,
            message_ids=callback_query.message.reply_to_message_id
        )
        MSG.status_msg = await leechbot.send_message(
            chat_id=OWNER,
            text="**🚀 Initializing Task...**\n\nPlease Wait While I Prepare Your Download",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="cancel")]])
        )
        BOT.State.task_going = True
        BOT.State.started = False
        BotTimes.start_time = datetime.now()
        event_loop = get_event_loop()
        BOT.TASK = event_loop.create_task(taskScheduler())
        try:
            await BOT.TASK
        finally:
            BOT.State.task_going = False
            if BOT.TASK_QUEUE:
                await process_next_in_queue(client)
    elif data == "cancel":
        await cancelTask("User cancelled the task")
    elif data == "sys_refresh":
        original_text = callback_query.message.text
        parts = original_text.split("⌬─────")
        if len(parts) >= 2:
            new_text = parts[0] + sysINFO()
            await callback_query.message.edit_text(text=new_text, disable_web_page_preview=True, reply_markup=status_keyboard())
        else:
            await callback_query.message.edit_text(text=original_text + "\n" + sysINFO(), disable_web_page_preview=True, reply_markup=status_keyboard())
        await callback_query.answer("System info refreshed")
    elif data == "sys_stats":
        original_text = callback_query.message.text
        parts = original_text.split("⌬─────")
        if len(parts) >= 2:
            new_text = parts[0] + sysINFO_full()
        else:
            new_text = original_text + "\n" + sysINFO_full()
        await callback_query.message.edit_text(text=new_text, disable_web_page_preview=True, reply_markup=status_keyboard())
        await callback_query.answer("Showing detailed stats")
    elif data == "sys_close":
        await callback_query.message.delete()
        await callback_query.answer("Closed")

# =============================================================================
# Photo Handler (Thumbnail)
# =============================================================================
@leechbot.on_message(filters.photo & filters.private)
async def handle_photo(client, message):
    msg = await message.reply_text("**🖼️ Processing Thumbnail...**")
    success = await setThumbnail(message)
    if success:
        await msg.edit_text("**✅ Thumbnail Set Successfully**")
        await message.delete()
    else:
        await msg.edit_text("**❎ Failed To Set Thumbnail**")
    await message_deleter(message, msg)

# =============================================================================
# Queue Processing
# =============================================================================
async def process_next_in_queue(client):
    if not BOT.TASK_QUEUE:
        return
    chat_id, msg, sources, mode, ytdl, up_type = BOT.TASK_QUEUE.pop(0)
    BOT.Mode.mode = mode
    BOT.Mode.ytdl = ytdl
    BOT.Mode.type = up_type
    BOT.SOURCE = sources
    BOT.CURRENT_TASK_OWNER = chat_id
    BOT.State.started = True
    await leechbot.send_message(chat_id, "**▶️ Starting queued task...**")
    fake_cb = type('obj', (object,), {
        'message': msg,
        'data': up_type,
        'reply_to_message_id': msg.id
    })
    await handle_callback(client, fake_cb)

# =============================================================================
# Bot Startup
# =============================================================================
logger.info("=" * 60)
logger.info("LeechBot started successfully")
logger.info("Developer: Shinei Nouzen")
logger.info("GitHub: https://github.com/Shineii86/LeechBot")
logger.info("=" * 60)

# Check for resume session on startup
create_task(check_resume_session())

leechbot.run()
