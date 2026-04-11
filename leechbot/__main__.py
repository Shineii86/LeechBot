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
from asyncio import sleep, get_event_loop
from leechbot import leechbot, OWNER
from leechbot.utility.handler import cancelTask
from leechbot.utility.variables import BOT, MSG, BotTimes, Paths
from leechbot.utility.task_manager import taskScheduler, task_starter
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from leechbot.utility.helper import (
    isLink, setThumbnail, message_deleter, send_settings,
    sysINFO, sysINFO_full, status_keyboard  # <-- Import new functions
)
from leechbot.utility.style import style_text, style_button

logger = logging.getLogger(__name__)

# =============================================================================
# Global Variables
# =============================================================================
src_request_msg = None

# =============================================================================
# Welcome Message (Styled & Professional)
# =============================================================================
WELCOME_TEXT = style_text("""
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

───────────────────────────

**📋 Quick Commands**
`/tupload` — Upload To Telegram
`/gdupload` — Mirror To Google Drive
`/ytupload` — Download With Yt‑Dlp
`/settings` — Configure Bot Preferences

───────────────────────────

**🧑‍💻 Developer:** [Shinei Nouzen](https://t.me/Shineii86)

""")

# =============================================================================
# Bot Commands
# =============================================================================
@leechbot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    """
    Handle the /start command.
    Sends welcome message with repository and support links.
    """
    await message.delete()
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(style_button("📂 GitHub Repository ✨"), url="https://github.com/Shineii86/LeechBot")
            ],
            [
                InlineKeyboardButton(style_button("🔔 Updates"), url="https://t.me/MaximXBots"),
                InlineKeyboardButton(style_button("Support 💬"), url="https://t.me/MaximXGroup"),
            ],
            [
                InlineKeyboardButton(style_button("🤖 Bot Settings ⚙️"), callback_data="settings_menu"),
            ]
        ]
    )
    
    await message.reply_text(WELCOME_TEXT, reply_markup=keyboard)


@leechbot.on_message(filters.command("tupload") & filters.private)
async def telegram_upload_command(client, message):
    """
    Handle the /tupload command.
    Sets up leech mode for uploading files to Telegram.
    """
    global BOT, src_request_msg
    
    BOT.Mode.mode = "leech"
    BOT.Mode.ytdl = False
    
    text = style_text("""**⚡ Send Download Link(s)** 🔗

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
• Use () For Extract Password""")
    
    src_request_msg = await task_starter(message, text)


@leechbot.on_message(filters.command("gdupload") & filters.private)
async def gdrive_upload_command(client, message):
    """
    Handle the /gdupload command.
    Sets up mirror mode for uploading files to Google Drive.
    """
    global BOT, src_request_msg
    
    BOT.Mode.mode = "mirror"
    BOT.Mode.ytdl = False
    
    text = style_text("""**⚡ Send Download Link(s)** 🔗

📋 **Follow The Pattern Below:**

<code>https://example.com/file1.mp4
https://example.com/file2.mp4
[Custom Name.mp4]
{Zip Password}
(Unzip Password)</code>

**💡 Tips:**
• Multiple Links Supported
• Files Will Be Mirrored To Your Gdrive
• Make Sure Gdrive Is Mounted""")
    
    src_request_msg = await task_starter(message, text)


@leechbot.on_message(filters.command("drupload") & filters.private)
async def directory_upload_command(client, message):
    """
    Handle the /drupload command.
    Sets up directory leech mode for uploading local folders.
    """
    global BOT, src_request_msg
    
    BOT.Mode.mode = "dir-leech"
    BOT.Mode.ytdl = False
    
    text = style_text("""**⚡ Send Folder Path** 📁

📋 **Example:**

<code>/home/user/Downloads/myfolder</code>

**💡 Note:**
• Provide Absolute Path To The Folder
• Ensure The Bot Has Read Permissions""")
    
    src_request_msg = await task_starter(message, text)


@leechbot.on_message(filters.command("ytupload") & filters.private)
async def ytdl_upload_command(client, message):
    """
    Handle the /ytupload command.
    Sets up YT-DLP mode for downloading from YouTube and other sites.
    """
    global BOT, src_request_msg
    
    BOT.Mode.mode = "leech"
    BOT.Mode.ytdl = True
    
    text = style_text("""**⚡ Send Yt-Dlp Link(s)** 🔗

📋 **Follow The Pattern Below:**

<code>https://youtube.com/watch?v=xxxxx
https://youtu.be/xxxxx
[Custom Name.mp4]
{Zip Password}</code>

**💡 Supported Sites:**
• Youtube, Facebook, Instagram
• Twitter, Tiktok, And More...""")
    
    src_request_msg = await task_starter(message, text)


@leechbot.on_message(filters.command("settings") & filters.private)
async def settings_command(client, message):
    """
    Handle the /settings command.
    Opens the bot settings menu (owner only).
    """
    if message.chat.id == OWNER:
        await message.delete()
        await send_settings(client, message, message.id, True)


@leechbot.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    """
    Handle the /help command.
    Displays help information and available commands.
    """
    help_text = style_text("""**📖 Leechbot Help Menu**

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
/help - Show This Help Message

**🖼️ Thumbnail:**
Send Any Image To Set It As Thumbnail""")
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(style_button("📂 GitHub Repository ✨"), url="https://github.com/Shineii86/LeechBot")
            ],
            [
                InlineKeyboardButton(style_button("🔔 Updates"), url="https://t.me/MaximXBots"),
                InlineKeyboardButton(style_button("Support 💬"), url="https://t.me/MaximXGroup"),
            ],
            [
                InlineKeyboardButton(style_button("🧑‍💻 Developer ✨"), url="https://t.me/Shineii86")
            ]
        ]
    )
    
    msg = await message.reply_text(help_text, reply_markup=keyboard)
    await sleep(30)
    await message_deleter(message, msg)


@leechbot.on_message(filters.command("setname") & filters.private)
async def setname_command(client, message):
    """
    Handle the /setname command.
    Sets a custom filename for downloads.
    """
    global BOT
    
    if len(message.command) < 2:
        msg = await message.reply_text(
            style_text("**⚠️ Usage:**\n`/setname <filename.extension>`\n\n**Example:**\n`/setname myvideo.mp4`"),
            quote=True
        )
    else:
        BOT.Options.custom_name = " ".join(message.command[1:])
        msg = await message.reply_text(
            style_text(f"**✅ Custom Name Set:**\n`{BOT.Options.custom_name}`"),
            quote=True
        )
    
    await sleep(15)
    await message_deleter(message, msg)


@leechbot.on_message(filters.command("zipaswd") & filters.private)
async def zipaswd_command(client, message):
    """
    Handle the /zipaswd command.
    Sets a password for zip compression.
    """
    global BOT
    
    if len(message.command) != 2:
        msg = await message.reply_text(
            style_text("**⚠️ Usage:**\n`/zipaswd <password>`\n\n**Example:**\n`/zipaswd mypassword123`"),
            quote=True
        )
    else:
        BOT.Options.zip_pswd = message.command[1]
        msg = await message.reply_text(
            style_text("**🔐 Zip Password Set Successfully**"),
            quote=True
        )
    
    await sleep(15)
    await message_deleter(message, msg)


@leechbot.on_message(filters.command("unzipaswd") & filters.private)
async def unzipaswd_command(client, message):
    """
    Handle the /unzipaswd command.
    Sets a password for extracting archives.
    """
    global BOT
    
    if len(message.command) != 2:
        msg = await message.reply_text(
            style_text("**⚠️ Usage:**\n`/unzipaswd <password>`\n\n**Example:**\n`/unzipaswd mypassword123`"),
            quote=True
        )
    else:
        BOT.Options.unzip_pswd = message.command[1]
        msg = await message.reply_text(
            style_text("**🔓 Unzip Password Set Successfully**"),
            quote=True
        )
    
    await sleep(15)
    await message_deleter(message, msg)


@leechbot.on_message(filters.command("stats") & filters.private)
async def stats_command(client, message):
    """
    Handle the /stats command.
    Displays bot statistics and system information.
    """
    stats_text = style_text(f"**📊 Bot Statistics**{sysINFO()}")
    
    msg = await message.reply_text(stats_text, quote=True)
    await sleep(15)
    await message_deleter(message, msg)


@leechbot.on_message(filters.command("cancel") & filters.private)
async def cancel_command(client, message):
    """
    Handle the /cancel command.
    Cancels the current running task.
    """
    if BOT.State.task_going:
        await cancelTask("User cancelled the task")
        msg = await message.reply_text(style_text("**🚫 Task Cancelled**"), quote=True)
    else:
        msg = await message.reply_text(style_text("**⚠️ No Active Task To Cancel**"), quote=True)
    
    await sleep(10)
    await message_deleter(message, msg)


# =============================================================================
# Reply Handlers
# =============================================================================
@leechbot.on_message(filters.reply)
async def handle_reply(client, message):
    """
    Handle reply messages for setting prefix/suffix.
    """
    global BOT
    
    if BOT.State.prefix:
        BOT.Setting.prefix = message.text
        BOT.State.prefix = False
        await send_settings(client, message, message.reply_to_message_id, False)
        await message.delete()
    elif BOT.State.suffix:
        BOT.Setting.suffix = message.text
        BOT.State.suffix = False
        await send_settings(client, message, message.reply_to_message_id, False)
        await message.delete()


# =============================================================================
# Link Handler
# =============================================================================
@leechbot.on_message(filters.create(isLink) & ~filters.photo)
async def handle_url(client, message):
    """
    Handle URL messages for download processing.
    Parses options like custom name, zip password, and unzip password.
    """
    global BOT, src_request_msg
    
    # Reset options
    BOT.Options.custom_name = ""
    BOT.Options.zip_pswd = ""
    BOT.Options.unzip_pswd = ""
    
    if src_request_msg:
        await src_request_msg.delete()
    
    if not BOT.State.task_going and BOT.State.started:
        temp_source = message.text.splitlines()
        
        # Parse options from message
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
        
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(style_button("📄 Regular ✨"), callback_data="normal")
                ],
                [
                    InlineKeyboardButton(style_button("🗜️ Compress"), callback_data="zip"),
                    InlineKeyboardButton(style_button("Extract 📂"), callback_data="unzip"),
                ],
                [
                    InlineKeyboardButton(style_button("🔄 Unzip+Zip ✨"), callback_data="undzip")
                ],
            ]
        )
        
        mode_text = BOT.Mode.mode.capitalize()
        options_text = style_text(f"""**🎯 Select Upload Type For {mode_text}**

📄 **Regular** - Normal File Upload
🗜️ **Compress** - Zip File Upload
📂 **Extract** - Extract Archive Before Upload
🔄 **Unzip+Zip** - Extract Then Compress""")
        
        await message.reply_text(
            text=options_text,
            reply_markup=keyboard,
            quote=True
        )
    elif BOT.State.started:
        await message.delete()
        msg = await message.reply_text(style_text("**⏳ I'm Already Working! Please Wait...**"))
        await sleep(10)
        await msg.delete()


# =============================================================================
# Callback Query Handler
# =============================================================================
@leechbot.on_callback_query()
async def handle_callback(client, callback_query):
    """
    Handle all inline keyboard callbacks.
    """
    global BOT, MSG
    
    data = callback_query.data
    
    # Upload type selection
    if data in ["normal", "zip", "unzip", "undzip"]:
        BOT.Mode.type = data
        await callback_query.message.delete()
        await leechbot.delete_messages(
            chat_id=callback_query.message.chat.id,
            message_ids=callback_query.message.reply_to_message_id
        )
        
        MSG.status_msg = await leechbot.send_message(
            chat_id=OWNER,
            text=style_text("**🚀 Initializing Task...**\n\nPlease Wait While I Prepare Your Download"),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(style_button("🚫 Cancel"), callback_data="cancel")]]
            )
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
    
    # Settings menu
    elif data == "settings_menu":
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # Video settings
    elif data == "video":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(style_button("✂️ Split"), callback_data="split-true"),
                    InlineKeyboardButton(style_button("Zip 🗜️"), callback_data="split-false"),
                ],
                [
                    InlineKeyboardButton(style_button("🔄 Convert"), callback_data="convert-true"),
                    InlineKeyboardButton(style_button("Skip ⏭️"), callback_data="convert-false"),
                ],
                [
                    InlineKeyboardButton("🎬 Mp4", callback_data="mp4"),
                    InlineKeyboardButton("Mkv 📼", callback_data="mkv"),
                ],
                [
                    InlineKeyboardButton(style_button("👍 High Quality"), callback_data="q-High"),
                    InlineKeyboardButton(style_button("Low Quality 👎"), callback_data="q-Low"),
                ],
                [
                    InlineKeyboardButton(style_button("❰ Back"), callback_data="back")
                ],
            ]
        )
        
        await callback_query.message.edit_text(
            style_text(f"**⚙️ Video Settings**\n\n"
                      f"┏🔄 **Convert:** `{BOT.Setting.convert_video}`\n"
                      f"┣✂️ **Split:** `{BOT.Setting.split_video}`\n"
                      f"┣🎬 **Format:** `{BOT.Options.video_out}`\n"
                      f"┗🔴 **Quality:** `{BOT.Setting.convert_quality}`"),
            reply_markup=keyboard
        )
    
    # Caption settings
    elif data == "caption":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("<code>Monospace</code>", callback_data="code-Monospace"),
                    InlineKeyboardButton("**Bold**", callback_data="b-Bold"),
                ],
                [
                    InlineKeyboardButton("__Italic__", callback_data="i-Italic"),
                    InlineKeyboardButton("__Underline__", callback_data="u-Underlined"),
                ],
                [
                    InlineKeyboardButton("Regular", callback_data="p-Regular")
                ],
                [
                    InlineKeyboardButton(style_button("❰ Back"), callback_data="back")
                ],
            ]
        )
        
        await callback_query.message.edit_text(
            style_text("**📝 Caption Font Style**\n\n"
                      "<code>Monospace</code>\n"
                      "Regular\n"
                      "**Bold**\n"
                      "__Italic__\n"
                      "__Underline__"),
            reply_markup=keyboard
        )
    
    # Thumbnail settings
    elif data == "thumb":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(style_button("🗑️ Delete Thumbnail"), callback_data="del-thumb")
                ],
                [
                    InlineKeyboardButton(style_button("❰ Back"), callback_data="back")
                ],
            ]
        )
        
        thmb_status = style_text("✅ Set") if BOT.Setting.thumbnail else style_text("🚫 None")
        
        await callback_query.message.edit_text(
            style_text(f"**🖼️ Thumbnail Settings**\n\n"
                      f"**Status:** {thmb_status}\n\n"
                      f"💡 Send An Image To Set As Thumbnail"),
            reply_markup=keyboard
        )
    
    # Delete thumbnail
    elif data == "del-thumb":
        if BOT.Setting.thumbnail and os.path.exists(Paths.THMB_PATH):
            os.remove(Paths.THMB_PATH)
        BOT.Setting.thumbnail = False
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # Set prefix/suffix
    elif data == "set-prefix":
        await callback_query.message.edit_text(
            style_text("**⌨️ Send Text To Set As Prefix**\n\nReply To This Message With Your Prefix")
        )
        BOT.State.prefix = True
    
    elif data == "set-suffix":
        await callback_query.message.edit_text(
            style_text("**⌨️ Send Text To Set As Suffix**\n\nReply To This Message With Your Suffix")
        )
        BOT.State.suffix = True
    
    # Caption style selection
    elif data in ["code-Monospace", "p-Regular", "b-Bold", "i-Italic", "u-Underlined"]:
        res = data.split("-")
        BOT.Options.caption = res[0]
        BOT.Setting.caption = res[1]
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # Video split selection
    elif data in ["split-true", "split-false"]:
        BOT.Options.is_split = data == "split-true"
        BOT.Setting.split_video = "Split" if data == "split-true" else "Zip"
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # Video convert selection
    elif data in ["convert-true", "convert-false"]:
        BOT.Options.convert_video = data == "convert-true"
        BOT.Setting.convert_video = "Yes" if data == "convert-true" else "No"
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # Video format selection
    elif data in ["mp4", "mkv"]:
        BOT.Options.video_out = data
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # Quality selection
    elif data in ["q-High", "q-Low"]:
        BOT.Setting.convert_quality = data.split("-")[-1]
        BOT.Options.convert_quality = BOT.Setting.convert_quality == "High"
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # Upload mode selection
    elif data in ["media", "document"]:
        BOT.Options.stream_upload = data == "media"
        BOT.Setting.stream_upload = "Media" if data == "media" else "Document"
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # Close menu
    elif data == "close":
        await callback_query.message.delete()
    
    # Go back
    elif data == "back":
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # YTDL confirmation
    elif data in ["ytdl-true", "ytdl-false"]:
        BOT.Mode.ytdl = data == "ytdl-true"
        await callback_query.message.delete()
        await leechbot.delete_messages(
            chat_id=callback_query.message.chat.id,
            message_ids=callback_query.message.reply_to_message_id
        )
        
        MSG.status_msg = await leechbot.send_message(
            chat_id=OWNER,
            text=style_text("**🚀 Initializing Task...**\n\nPlease Wait While I Prepare Your Download"),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(style_button("Cancel"), callback_data="cancel")
                    ]
                ]
            )
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
    
    # Cancel task
    elif data == "cancel":
        await cancelTask("User cancelled the task")
    
    # =========================================================================
    # System Info Callbacks (NEW)
    # =========================================================================
    # System Info Refresh
    elif data == "sys_refresh":
        original_text = callback_query.message.text
        parts = original_text.split("⌬─────")
        if len(parts) >= 2:
            new_text = parts[0] + sysINFO()
            await callback_query.message.edit_text(
                text=new_text,
                disable_web_page_preview=True,
                reply_markup=status_keyboard()
            )
        else:
            await callback_query.message.edit_text(
                text=original_text + "\n" + sysINFO(),
                disable_web_page_preview=True,
                reply_markup=status_keyboard()
            )
        await callback_query.answer("System info refreshed")
    
    # Detailed System Stats
    elif data == "sys_stats":
        original_text = callback_query.message.text
        parts = original_text.split("⌬─────")
        if len(parts) >= 2:
            new_text = parts[0] + sysINFO_full()
        else:
            new_text = original_text + "\n" + sysINFO_full()
        await callback_query.message.edit_text(
            text=new_text,
            disable_web_page_preview=True,
            reply_markup=status_keyboard()
        )
        await callback_query.answer("Showing detailed stats")
    
    # Close system panel (optional)
    elif data == "sys_close":
        await callback_query.message.delete()
        await callback_query.answer("Closed")


# =============================================================================
# Photo Handler (Thumbnail)
# =============================================================================
@leechbot.on_message(filters.photo & filters.private)
async def handle_photo(client, message):
    """
    Handle photo messages to set thumbnail.
    """
    msg = await message.reply_text(style_text("**🖼️ Processing Thumbnail...**"))
    
    success = await setThumbnail(message)
    
    if success:
        await msg.edit_text(style_text("**✅ Thumbnail Set Successfully**"))
        await message.delete()
    else:
        await msg.edit_text(style_text("**❎ Failed To Set Thumbnail**"))
    
    await sleep(15)
    await message_deleter(message, msg)


# =============================================================================
# Bot Startup
# =============================================================================
logger.info("=" * 60)
logger.info("LeechBot started successfully")
logger.info("Developer: Shinei Nouzen")
logger.info("GitHub: https://github.com/Shineii86/LeechBot")
logger.info("=" * 60)

leechbot.run()
