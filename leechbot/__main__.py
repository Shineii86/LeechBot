# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
#  x: https://x.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ʟᴇᴇᴄʜʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅ ʜᴀɴᴅʟᴇʀs ᴀɴᴅ ᴇɴᴛʀʏ ᴘᴏɪɴᴛ

ᴛʜɪs ᴍᴏᴅᴜʟᴇ ᴄᴏɴᴛᴀɪɴs ᴀʟʟ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅ ʜᴀɴᴅʟᴇʀs, ᴄᴀʟʟʙᴀᴄᴋ ǫᴜᴇʀɪᴇs,
ᴀɴᴅ ᴛʜᴇ ᴍᴀɪɴ ʙᴏᴛ ᴇxᴇᴄᴜᴛɪᴏɴ ʟᴏᴏᴘ. ɪᴛ ʜᴀɴᴅʟᴇs ᴜsᴇʀ ɪɴᴛᴇʀᴀᴄᴛɪᴏɴs
ᴀɴᴅ ᴏʀᴄʜᴇsᴛʀᴀᴛᴇs ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴘʀᴏᴄᴇssᴇs.
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
from leechbot.utility.helper import isLink, setThumbnail, message_deleter, send_settings

logger = logging.getLogger(__name__)

# =============================================================================
#  ɢʟᴏʙᴀʟ ᴠᴀʀɪᴀʙʟᴇs
# =============================================================================
src_request_msg = None

# =============================================================================
#  ᴜɴɪᴄᴏᴅᴇ sᴛʏʟɪɴɢ ғᴜɴᴄᴛɪᴏɴs
# =============================================================================
def style_text(text: str) -> str:
    """
    ᴄᴏɴᴠᴇʀᴛ ʀᴇɢᴜʟᴀʀ ᴛᴇxᴛ ᴛᴏ ᴜɴɪᴄᴏᴅᴇ sᴍᴀʟʟ ᴄᴀᴘs sᴛʏʟᴇ.
    
    ᴄᴀᴘɪᴛᴀʟ ʟᴇᴛᴛᴇʀs: ᴀ, ʙ, ᴄ, ᴅ, ᴇ, ғ, ɢ, ʜ, ɪ, ᴊ, ᴋ, ʟ, ᴍ, ɴ, ᴏ, ᴘ, Ҩ, ʀ, s, ᴛ, ᴜ, ᴠ, ᴡ, x, ʏ, ᴢ
    sᴍᴀʟʟ ʟᴇᴛᴛᴇʀs: ᴀ, ʙ, ᴄ, ᴅ, ᴇ, ғ, ɢ, ʜ, ɪ, ᴊ, ᴋ, ʟ, ᴍ, ɴ, ᴏ, ᴘ, ҩ, ʀ, s, ᴛ, ᴜ, ᴠ, ᴡ, x, ʏ, ᴢ
    """
    normal_caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    normal_small = "abcdefghijklmnopqrstuvwxyz"
    unicode_caps = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘҨʀsᴛᴜᴠᴡxʏᴢ"
    unicode_small = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘҩʀsᴛᴜᴠᴡxʏᴢ"
    
    result = ""
    for char in text:
        if char in normal_caps:
            result += unicode_caps[normal_caps.index(char)]
        elif char in normal_small:
            result += unicode_small[normal_small.index(char)]
        else:
            result += char
    return result

# =============================================================================
#  ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ
# =============================================================================
WELCOME_TEXT = """**ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʟᴇᴇᴄʜʙᴏᴛ** 🚀

◈ **ᴘᴏᴡᴇʀғᴜʟ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ ʙᴏᴛ**
◈ **ᴅᴏᴡɴʟᴏᴀᴅ ғʀᴏᴍ ᴍᴜʟᴛɪᴘʟᴇ sᴏᴜʀᴄᴇs**
◈ **ᴜᴘʟᴏᴀᴅ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ᴏʀ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ**

**ᴅᴇᴠᴇʟᴏᴘᴇʀ:** @sʜɪɴᴇɪɪ86
**ɢɪᴛʜᴜʙ:** sʜɪɴᴇɪɪ86/ʟᴇᴇᴄʜʙᴏᴛ"""

# =============================================================================
#  ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs
# =============================================================================
@leechbot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴛʜᴇ /sᴛᴀʀᴛ ᴄᴏᴍᴍᴀɴᴅ.
    sᴇɴᴅs ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ ʀᴇᴘᴏsɪᴛᴏʀʏ ᴀɴᴅ sᴜᴘᴘᴏʀᴛ ʟɪɴᴋs.
    """
    await message.delete()
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📂 ʀᴇᴘᴏsɪᴛᴏʀʏ", url="https://github.com/Shineii86/LeechBot"),
                InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url="https://t.me/Shineii86"),
            ],
            [
                InlineKeyboardButton("⚙️ sᴇᴛᴛɪɴɢs", callback_data="settings_menu"),
            ]
        ]
    )
    
    await message.reply_text(WELCOME_TEXT, reply_markup=keyboard)


@leechbot.on_message(filters.command("tupload") & filters.private)
async def telegram_upload_command(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴛʜᴇ /ᴛᴜᴘʟᴏᴀᴅ ᴄᴏᴍᴍᴀɴᴅ.
    sᴇᴛs ᴜᴘ ʟᴇᴇᴄʜ ᴍᴏᴅᴇ ғᴏʀ ᴜᴘʟᴏᴀᴅɪɴɢ ғɪʟᴇs ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ.
    """
    global BOT, src_request_msg
    
    BOT.Mode.mode = "leech"
    BOT.Mode.ytdl = False
    
    text = """**⚡ sᴇɴᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ(s)** 🔗

📋 **ғᴏʟʟᴏᴡ ᴛʜᴇ ᴘᴀᴛᴛᴇʀɴ ʙᴇʟᴏᴡ:**

<code>https://example.com/file1.mp4
https://example.com/file2.mp4
[ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ.mp4]
{ᴢɪᴘ ᴘᴀssᴡᴏʀᴅ}
(ᴜɴᴢɪᴘ ᴘᴀssᴡᴏʀᴅ)</code>

**💡 ᴛɪᴘs:**
• ᴍᴜʟᴛɪᴘʟᴇ ʟɪɴᴋs sᴜᴘᴘᴏʀᴛᴇᴅ
• ᴜsᴇ [] ғᴏʀ ᴄᴜsᴛᴏᴍ ғɪʟᴇɴᴀᴍᴇ
• ᴜsᴇ {} ғᴏʀ ᴢɪᴘ ᴘᴀssᴡᴏʀᴅ
• ᴜsᴇ () ғᴏʀ ᴇxᴛʀᴀᴄᴛ ᴘᴀssᴡᴏʀᴅ"""
    
    src_request_msg = await task_starter(message, text)


@leechbot.on_message(filters.command("gdupload") & filters.private)
async def gdrive_upload_command(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴛʜᴇ /ɢᴅᴜᴘʟᴏᴀᴅ ᴄᴏᴍᴍᴀɴᴅ.
    sᴇᴛs ᴜᴘ ᴍɪʀʀᴏʀ ᴍᴏᴅᴇ ғᴏʀ ᴜᴘʟᴏᴀᴅɪɴɢ ғɪʟᴇs ᴛᴏ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ.
    """
    global BOT, src_request_msg
    
    BOT.Mode.mode = "mirror"
    BOT.Mode.ytdl = False
    
    text = """**⚡ sᴇɴᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ(s)** 🔗

📋 **ғᴏʟʟᴏᴡ ᴛʜᴇ ᴘᴀᴛᴛᴇʀɴ ʙᴇʟᴏᴡ:**

<code>https://example.com/file1.mp4
https://example.com/file2.mp4
[ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ.mp4]
{ᴢɪᴘ ᴘᴀssᴡᴏʀᴅ}
(ᴜɴᴢɪᴘ ᴘᴀssᴡᴏʀᴅ)</code>

**💡 ᴛɪᴘs:**
• ᴍᴜʟᴛɪᴘʟᴇ ʟɪɴᴋs sᴜᴘᴘᴏʀᴛᴇᴅ
• ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴍɪʀʀᴏʀᴇᴅ ᴛᴏ ʏᴏᴜʀ ɢᴅʀɪᴠᴇ
• ᴍᴀᴋᴇ sᴜʀᴇ ɢᴅʀɪᴠᴇ ɪs ᴍᴏᴜɴᴛᴇᴅ"""
    
    src_request_msg = await task_starter(message, text)


@leechbot.on_message(filters.command("drupload") & filters.private)
async def directory_upload_command(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴛʜᴇ /ᴅʀᴜᴘʟᴏᴀᴅ ᴄᴏᴍᴍᴀɴᴅ.
    sᴇᴛs ᴜᴘ ᴅɪʀᴇᴄᴛᴏʀʏ ʟᴇᴇᴄʜ ᴍᴏᴅᴇ ғᴏʀ ᴜᴘʟᴏᴀᴅɪɴɢ ʟᴏᴄᴀʟ ғᴏʟᴅᴇʀs.
    """
    global BOT, src_request_msg
    
    BOT.Mode.mode = "dir-leech"
    BOT.Mode.ytdl = False
    
    text = """**⚡ sᴇɴᴅ ғᴏʟᴅᴇʀ ᴘᴀᴛʜ** 📁

📋 **ᴇxᴀᴍᴘʟᴇ:**

<code>/home/user/Downloads/myfolder</code>

**💡 ɴᴏᴛᴇ:**
• ᴘʀᴏᴠɪᴅᴇ ᴀʙsᴏʟᴜᴛᴇ ᴘᴀᴛʜ ᴛᴏ ᴛʜᴇ ғᴏʟᴅᴇʀ
• ᴇɴsᴜʀᴇ ᴛʜᴇ ʙᴏᴛ ʜᴀs ʀᴇᴀᴅ ᴘᴇʀᴍɪssɪᴏɴs"""
    
    src_request_msg = await task_starter(message, text)


@leechbot.on_message(filters.command("ytupload") & filters.private)
async def ytdl_upload_command(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴛʜᴇ /ʏᴛᴜᴘʟᴏᴀᴅ ᴄᴏᴍᴍᴀɴᴅ.
    sᴇᴛs ᴜᴘ ʏᴛ-ᴅʟᴘ ᴍᴏᴅᴇ ғᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ᴀɴᴅ ᴏᴛʜᴇʀ sɪᴛᴇs.
    """
    global BOT, src_request_msg
    
    BOT.Mode.mode = "leech"
    BOT.Mode.ytdl = True
    
    text = """**⚡ sᴇɴᴅ ʏᴛ-ᴅʟᴘ ʟɪɴᴋ(s)** 🔗

📋 **ғᴏʟʟᴏᴡ ᴛʜᴇ ᴘᴀᴛᴛᴇʀɴ ʙᴇʟᴏᴡ:**

<code>https://youtube.com/watch?v=xxxxx
https://youtu.be/xxxxx
[ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ.mp4]
{ᴢɪᴘ ᴘᴀssᴡᴏʀᴅ}</code>

**💡 sᴜᴘᴘᴏʀᴛᴇᴅ sɪᴛᴇs:**
• ʏᴏᴜᴛᴜʙᴇ, ғᴀᴄᴇʙᴏᴏᴋ, ɪɴsᴛᴀɢʀᴀᴍ
• ᴛᴡɪᴛᴛᴇʀ, ᴛɪᴋᴛᴏᴋ, ᴀɴᴅ ᴍᴏʀᴇ..."""
    
    src_request_msg = await task_starter(message, text)


@leechbot.on_message(filters.command("settings") & filters.private)
async def settings_command(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴛʜᴇ /sᴇᴛᴛɪɴɢs ᴄᴏᴍᴍᴀɴᴅ.
    ᴏᴘᴇɴs ᴛʜᴇ ʙᴏᴛ sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ (ᴏᴡɴᴇʀ ᴏɴʟʏ).
    """
    if message.chat.id == OWNER:
        await message.delete()
        await send_settings(client, message, message.id, True)


@leechbot.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴛʜᴇ /ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅ.
    ᴅɪsᴘʟᴀʏs ʜᴇʟᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀɴᴅ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs.
    """
    help_text = """**📖 ʟᴇᴇᴄʜʙᴏᴛ ʜᴇʟᴘ ᴍᴇɴᴜ**

**ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs:**

/start - sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
/tupload - ᴜᴘʟᴏᴀᴅ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ
/gdupload - ᴍɪʀʀᴏʀ ᴛᴏ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ
/drupload - ᴜᴘʟᴏᴀᴅ ʟᴏᴄᴀʟ ᴅɪʀᴇᴄᴛᴏʀʏ
/ytupload - ᴅᴏᴡɴʟᴏᴀᴅ ᴡɪᴛʜ ʏᴛ-ᴅʟᴘ
/settings - ʙᴏᴛ sᴇᴛᴛɪɴɢs
/setname - sᴇᴛ ᴄᴜsᴛᴏᴍ ғɪʟᴇɴᴀᴍᴇ
/zipaswd - sᴇᴛ ᴢɪᴘ ᴘᴀssᴡᴏʀᴅ
/unzipaswd - sᴇᴛ ᴜɴᴢɪᴘ ᴘᴀssᴡᴏʀᴅ
/help - sʜᴏᴡ ᴛʜɪs ʜᴇʟᴘ ᴍᴇssᴀɢᴇ

**🖼️ ᴛʜᴜᴍʙɴᴀɪʟ:**
sᴇɴᴅ ᴀɴʏ ɪᴍᴀɢᴇ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ᴛʜᴜᴍʙɴᴀɪʟ"""
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📂 ʀᴇᴘᴏsɪᴛᴏʀʏ", url="https://github.com/Shineii86/LeechBot"),
                InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url="https://t.me/Shineii86"),
            ]
        ]
    )
    
    msg = await message.reply_text(help_text, reply_markup=keyboard)
    await sleep(30)
    await message_deleter(message, msg)


@leechbot.on_message(filters.command("setname") & filters.private)
async def setname_command(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴛʜᴇ /sᴇᴛɴᴀᴍᴇ ᴄᴏᴍᴍᴀɴᴅ.
    sᴇᴛs ᴀ ᴄᴜsᴛᴏᴍ ғɪʟᴇɴᴀᴍᴇ ғᴏʀ ᴅᴏᴡɴʟᴏᴀᴅs.
    """
    global BOT
    
    if len(message.command) < 2:
        msg = await message.reply_text(
            "**⚠️ ᴜsᴀɢᴇ:**\n`/setname <filename.extension>`\n\n**ᴇxᴀᴍᴘʟᴇ:**\n`/setname myvideo.mp4`",
            quote=True
        )
    else:
        BOT.Options.custom_name = " ".join(message.command[1:])
        msg = await message.reply_text(
            f"**✅ ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ sᴇᴛ:**\n`{BOT.Options.custom_name}`",
            quote=True
        )
    
    await sleep(15)
    await message_deleter(message, msg)


@leechbot.on_message(filters.command("zipaswd") & filters.private)
async def zipaswd_command(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴛʜᴇ /ᴢɪᴘᴀsᴡᴅ ᴄᴏᴍᴍᴀɴᴅ.
    sᴇᴛs ᴀ ᴘᴀssᴡᴏʀᴅ ғᴏʀ ᴢɪᴘ ᴄᴏᴍᴘʀᴇssɪᴏɴ.
    """
    global BOT
    
    if len(message.command) != 2:
        msg = await message.reply_text(
            "**⚠️ ᴜsᴀɢᴇ:**\n`/zipaswd <password>`\n\n**ᴇxᴀᴍᴘʟᴇ:**\n`/zipaswd mypassword123`",
            quote=True
        )
    else:
        BOT.Options.zip_pswd = message.command[1]
        msg = await message.reply_text(
            "**🔐 ᴢɪᴘ ᴘᴀssᴡᴏʀᴅ sᴇᴛ sᴜᴄᴄᴇssғᴜʟʟʏ**",
            quote=True
        )
    
    await sleep(15)
    await message_deleter(message, msg)


@leechbot.on_message(filters.command("unzipaswd") & filters.private)
async def unzipaswd_command(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴛʜᴇ /ᴜɴᴢɪᴘᴀsᴡᴅ ᴄᴏᴍᴍᴀɴᴅ.
    sᴇᴛs ᴀ ᴘᴀssᴡᴏʀᴅ ғᴏʀ ᴇxᴛʀᴀᴄᴛɪɴɢ ᴀʀᴄʜɪᴠᴇs.
    """
    global BOT
    
    if len(message.command) != 2:
        msg = await message.reply_text(
            "**⚠️ ᴜsᴀɢᴇ:**\n`/unzipaswd <password>`\n\n**ᴇxᴀᴍᴘʟᴇ:**\n`/unzipaswd mypassword123`",
            quote=True
        )
    else:
        BOT.Options.unzip_pswd = message.command[1]
        msg = await message.reply_text(
            "**🔓 ᴜɴᴢɪᴘ ᴘᴀssᴡᴏʀᴅ sᴇᴛ sᴜᴄᴄᴇssғᴜʟʟʏ**",
            quote=True
        )
    
    await sleep(15)
    await message_deleter(message, msg)


@leechbot.on_message(filters.command("stats") & filters.private)
async def stats_command(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴛʜᴇ /sᴛᴀᴛs ᴄᴏᴍᴍᴀɴᴅ.
    ᴅɪsᴘʟᴀʏs ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs ᴀɴᴅ sʏsᴛᴇᴍ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.
    """
    from leechbot.utility.helper import sysINFO
    
    stats_text = f"**📊 ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs**{sysINFO()}"
    
    msg = await message.reply_text(stats_text, quote=True)
    await sleep(15)
    await message_deleter(message, msg)


@leechbot.on_message(filters.command("cancel") & filters.private)
async def cancel_command(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴛʜᴇ /ᴄᴀɴᴄᴇʟ ᴄᴏᴍᴍᴀɴᴅ.
    ᴄᴀɴᴄᴇʟs ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ʀᴜɴɴɪɴɢ ᴛᴀsᴋ.
    """
    if BOT.State.task_going:
        await cancelTask("ᴜsᴇʀ ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ᴛᴀsᴋ")
        msg = await message.reply_text("**❌ ᴛᴀsᴋ ᴄᴀɴᴄᴇʟʟᴇᴅ**", quote=True)
    else:
        msg = await message.reply_text("**⚠️ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴛᴀsᴋ ᴛᴏ ᴄᴀɴᴄᴇʟ**", quote=True)
    
    await sleep(10)
    await message_deleter(message, msg)


# =============================================================================
#  ʀᴇᴘʟʏ ʜᴀɴᴅʟᴇʀs
# =============================================================================
@leechbot.on_message(filters.reply)
async def handle_reply(client, message):
    """
    ʜᴀɴᴅʟᴇ ʀᴇᴘʟʏ ᴍᴇssᴀɢᴇs ғᴏʀ sᴇᴛᴛɪɴɢ ᴘʀᴇғɪx/sᴜғғɪx.
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
#  ʟɪɴᴋ ʜᴀɴᴅʟᴇʀ
# =============================================================================
@leechbot.on_message(filters.create(isLink) & ~filters.photo)
async def handle_url(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴜʀʟ ᴍᴇssᴀɢᴇs ғᴏʀ ᴅᴏᴡɴʟᴏᴀᴅ ᴘʀᴏᴄᴇssɪɴɢ.
    ᴘᴀʀsᴇs ᴏᴘᴛɪᴏɴs ʟɪᴋᴇ ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ, ᴢɪᴘ ᴘᴀssᴡᴏʀᴅ, ᴀɴᴅ ᴜɴᴢɪᴘ ᴘᴀssᴡᴏʀᴅ.
    """
    global BOT, src_request_msg
    
    # ʀᴇsᴇᴛ ᴏᴘᴛɪᴏɴs
    BOT.Options.custom_name = ""
    BOT.Options.zip_pswd = ""
    BOT.Options.unzip_pswd = ""
    
    if src_request_msg:
        await src_request_msg.delete()
    
    if not BOT.State.task_going and BOT.State.started:
        temp_source = message.text.splitlines()
        
        # ᴘᴀʀsᴇ ᴏᴘᴛɪᴏɴs ғʀᴏᴍ ᴍᴇssᴀɢᴇ
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
                [InlineKeyboardButton("📄 ʀᴇɢᴜʟᴀʀ", callback_data="normal")],
                [
                    InlineKeyboardButton("🗜️ ᴄᴏᴍᴘʀᴇss", callback_data="zip"),
                    InlineKeyboardButton("📂 ᴇxᴛʀᴀᴄᴛ", callback_data="unzip"),
                ],
                [InlineKeyboardButton("🔄 ᴜɴᴢɪᴘ+ᴢɪᴘ", callback_data="undzip")],
            ]
        )
        
        mode_text = BOT.Mode.mode.capitalize()
        options_text = f"""**🎯 sᴇʟᴇᴄᴛ ᴜᴘʟᴏᴀᴅ ᴛʏᴘᴇ ғᴏʀ {mode_text}**

📄 **ʀᴇɢᴜʟᴀʀ** - ɴᴏʀᴍᴀʟ ғɪʟᴇ ᴜᴘʟᴏᴀᴅ
🗜️ **ᴄᴏᴍᴘʀᴇss** - ᴢɪᴘ ғɪʟᴇ ᴜᴘʟᴏᴀᴅ
📂 **ᴇxᴛʀᴀᴄᴛ** - ᴇxᴛʀᴀᴄᴛ ᴀʀᴄʜɪᴠᴇ ʙᴇғᴏʀᴇ ᴜᴘʟᴏᴀᴅ
🔄 **ᴜɴᴢɪᴘ+ᴢɪᴘ** - ᴇxᴛʀᴀᴄᴛ ᴛʜᴇɴ ᴄᴏᴍᴘʀᴇss"""
        
        await message.reply_text(
            text=options_text,
            reply_markup=keyboard,
            quote=True
        )
    elif BOT.State.started:
        await message.delete()
        msg = await message.reply_text("**⏳ ɪ'ᴍ ᴀʟʀᴇᴀᴅʏ ᴡᴏʀᴋɪɴɢ! ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**")
        await sleep(10)
        await msg.delete()


# =============================================================================
#  ᴄᴀʟʟʙᴀᴄᴋ ǫᴜᴇʀʏ ʜᴀɴᴅʟᴇʀ
# =============================================================================
@leechbot.on_callback_query()
async def handle_callback(client, callback_query):
    """
    ʜᴀɴᴅʟᴇ ᴀʟʟ ɪɴʟɪɴᴇ ᴋᴇʏʙᴏᴀʀᴅ ᴄᴀʟʟʙᴀᴄᴋs.
    """
    global BOT, MSG
    
    data = callback_query.data
    
    # ᴜᴘʟᴏᴀᴅ ᴛʏᴘᴇ sᴇʟᴇᴄᴛɪᴏɴ
    if data in ["normal", "zip", "unzip", "undzip"]:
        BOT.Mode.type = data
        await callback_query.message.delete()
        await leechbot.delete_messages(
            chat_id=callback_query.message.chat.id,
            message_ids=callback_query.message.reply_to_message_id
        )
        
        MSG.status_msg = await leechbot.send_message(
            chat_id=OWNER,
            text="**🚀 ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴛᴀsᴋ...**\n\nᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴡʜɪʟᴇ ɪ ᴘʀᴇᴘᴀʀᴇ ʏᴏᴜʀ ᴅᴏᴡɴʟᴏᴀᴅ",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="cancel")]]
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
    
    # sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ
    elif data == "settings_menu":
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # ᴠɪᴅᴇᴏ sᴇᴛᴛɪɴɢs
    elif data == "video":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✂️ sᴘʟɪᴛ", callback_data="split-true"),
                    InlineKeyboardButton("🗜️ ᴢɪᴘ", callback_data="split-false"),
                ],
                [
                    InlineKeyboardButton("🔄 ᴄᴏɴᴠᴇʀᴛ", callback_data="convert-true"),
                    InlineKeyboardButton("⏭️ sᴋɪᴘ", callback_data="convert-false"),
                ],
                [
                    InlineKeyboardButton("🎬 ᴍᴘ4", callback_data="mp4"),
                    InlineKeyboardButton("📼 ᴍᴋᴠ", callback_data="mkv"),
                ],
                [
                    InlineKeyboardButton("🔴 ʜɪɢʜ ǫᴜᴀʟɪᴛʏ", callback_data="q-High"),
                    InlineKeyboardButton("🔵 ʟᴏᴡ ǫᴜᴀʟɪᴛʏ", callback_data="q-Low"),
                ],
                [InlineKeyboardButton("⏎ ʙᴀᴄᴋ", callback_data="back")],
            ]
        )
        
        await callback_query.message.edit_text(
            f"**⚙️ ᴠɪᴅᴇᴏ sᴇᴛᴛɪɴɢs**\n\n"
            f"╭🔄 **ᴄᴏɴᴠᴇʀᴛ:** `{BOT.Setting.convert_video}`\n"
            f"├✂️ **sᴘʟɪᴛ:** `{BOT.Setting.split_video}`\n"
            f"├🎬 **ғᴏʀᴍᴀᴛ:** `{BOT.Options.video_out}`\n"
            f"╰🔴 **ǫᴜᴀʟɪᴛʏ:** `{BOT.Setting.convert_quality}`",
            reply_markup=keyboard
        )
    
    # ᴄᴀᴘᴛɪᴏɴ sᴇᴛᴛɪɴɢs
    elif data == "caption":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("<code>ᴍᴏɴᴏsᴘᴀᴄᴇ</code>", callback_data="code-Monospace"),
                    InlineKeyboardButton("**ʙᴏʟᴅ**", callback_data="b-Bold"),
                ],
                [
                    InlineKeyboardButton("__ɪᴛᴀʟɪᴄ__", callback_data="i-Italic"),
                    InlineKeyboardButton("__ᴜɴᴅᴇʀʟɪɴᴇ__", callback_data="u-Underlined"),
                ],
                [InlineKeyboardButton("ʀᴇɢᴜʟᴀʀ", callback_data="p-Regular")],
                [InlineKeyboardButton("⏎ ʙᴀᴄᴋ", callback_data="back")],
            ]
        )
        
        await callback_query.message.edit_text(
            "**📝 ᴄᴀᴘᴛɪᴏɴ ғᴏɴᴛ sᴛʏʟᴇ**\n\n"
            "<code>ᴍᴏɴᴏsᴘᴀᴄᴇ</code>\n"
            "ʀᴇɢᴜʟᴀʀ\n"
            "**ʙᴏʟᴅ**\n"
            "__ɪᴛᴀʟɪᴄ__\n"
            "__ᴜɴᴅᴇʀʟɪɴᴇ__",
            reply_markup=keyboard
        )
    
    # ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛᴛɪɴɢs
    elif data == "thumb":
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🗑️ ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="del-thumb")],
                [InlineKeyboardButton("⏎ ʙᴀᴄᴋ", callback_data="back")],
            ]
        )
        
        thmb_status = "✅ sᴇᴛ" if BOT.Setting.thumbnail else "❌ ɴᴏɴᴇ"
        
        await callback_query.message.edit_text(
            f"**🖼️ ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛᴛɪɴɢs**\n\n"
            f"**sᴛᴀᴛᴜs:** {thmb_status}\n\n"
            f"💡 sᴇɴᴅ ᴀɴ ɪᴍᴀɢᴇ ᴛᴏ sᴇᴛ ᴀs ᴛʜᴜᴍʙɴᴀɪʟ",
            reply_markup=keyboard
        )
    
    # ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ
    elif data == "del-thumb":
        if BOT.Setting.thumbnail and os.path.exists(Paths.THMB_PATH):
            os.remove(Paths.THMB_PATH)
        BOT.Setting.thumbnail = False
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # sᴇᴛ ᴘʀᴇғɪx/sᴜғғɪx
    elif data == "set-prefix":
        await callback_query.message.edit_text(
            "**⌨️ sᴇɴᴅ ᴛᴇxᴛ ᴛᴏ sᴇᴛ ᴀs ᴘʀᴇғɪx**\n\nʀᴇᴘʟʏ ᴛᴏ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪᴛʜ ʏᴏᴜʀ ᴘʀᴇғɪx"
        )
        BOT.State.prefix = True
    
    elif data == "set-suffix":
        await callback_query.message.edit_text(
            "**⌨️ sᴇɴᴅ ᴛᴇxᴛ ᴛᴏ sᴇᴛ ᴀs sᴜғғɪx**\n\nʀᴇᴘʟʏ ᴛᴏ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪᴛʜ ʏᴏᴜʀ sᴜғғɪx"
        )
        BOT.State.suffix = True
    
    # ᴄᴀᴘᴛɪᴏɴ sᴛʏʟᴇ sᴇʟᴇᴄᴛɪᴏɴ
    elif data in ["code-Monospace", "p-Regular", "b-Bold", "i-Italic", "u-Underlined"]:
        res = data.split("-")
        BOT.Options.caption = res[0]
        BOT.Setting.caption = res[1]
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # ᴠɪᴅᴇᴏ sᴘʟɪᴛ sᴇʟᴇᴄᴛɪᴏɴ
    elif data in ["split-true", "split-false"]:
        BOT.Options.is_split = data == "split-true"
        BOT.Setting.split_video = "sᴘʟɪᴛ" if data == "split-true" else "ᴢɪᴘ"
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # ᴠɪᴅᴇᴏ ᴄᴏɴᴠᴇʀᴛ sᴇʟᴇᴄᴛɪᴏɴ
    elif data in ["convert-true", "convert-false"]:
        BOT.Options.convert_video = data == "convert-true"
        BOT.Setting.convert_video = "ʏᴇs" if data == "convert-true" else "ɴᴏ"
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # ᴠɪᴅᴇᴏ ғᴏʀᴍᴀᴛ sᴇʟᴇᴄᴛɪᴏɴ
    elif data in ["mp4", "mkv"]:
        BOT.Options.video_out = data
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # ǫᴜᴀʟɪᴛʏ sᴇʟᴇᴄᴛɪᴏɴ
    elif data in ["q-High", "q-Low"]:
        BOT.Setting.convert_quality = data.split("-")[-1]
        BOT.Options.convert_quality = BOT.Setting.convert_quality == "High"
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # ᴜᴘʟᴏᴀᴅ ᴍᴏᴅᴇ sᴇʟᴇᴄᴛɪᴏɴ
    elif data in ["media", "document"]:
        BOT.Options.stream_upload = data == "media"
        BOT.Setting.stream_upload = "ᴍᴇᴅɪᴀ" if data == "media" else "ᴅᴏᴄᴜᴍᴇɴᴛ"
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # ᴄʟᴏsᴇ ᴍᴇɴᴜ
    elif data == "close":
        await callback_query.message.delete()
    
    # ɢᴏ ʙᴀᴄᴋ
    elif data == "back":
        await send_settings(client, callback_query.message, callback_query.message.id, False)
    
    # ʏᴛᴅʟ ᴄᴏɴғɪʀᴍᴀᴛɪᴏɴ
    elif data in ["ytdl-true", "ytdl-false"]:
        BOT.Mode.ytdl = data == "ytdl-true"
        await callback_query.message.delete()
        await leechbot.delete_messages(
            chat_id=callback_query.message.chat.id,
            message_ids=callback_query.message.reply_to_message_id
        )
        
        MSG.status_msg = await leechbot.send_message(
            chat_id=OWNER,
            text="**🚀 ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴛᴀsᴋ...**\n\nᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴡʜɪʟᴇ ɪ ᴘʀᴇᴘᴀʀᴇ ʏᴏᴜʀ ᴅᴏᴡɴʟᴏᴀᴅ",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="cancel")]]
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
    
    # ᴄᴀɴᴄᴇʟ ᴛᴀsᴋ
    elif data == "cancel":
        await cancelTask("ᴜsᴇʀ ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ᴛᴀsᴋ")


# =============================================================================
#  ᴘʜᴏᴛᴏ ʜᴀɴᴅʟᴇʀ (ᴛʜᴜᴍʙɴᴀɪʟ)
# =============================================================================
@leechbot.on_message(filters.photo & filters.private)
async def handle_photo(client, message):
    """
    ʜᴀɴᴅʟᴇ ᴘʜᴏᴛᴏ ᴍᴇssᴀɢᴇs ᴛᴏ sᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ.
    """
    msg = await message.reply_text("**🖼️ ᴘʀᴏᴄᴇssɪɴɢ ᴛʜᴜᴍʙɴᴀɪʟ...**")
    
    success = await setThumbnail(message)
    
    if success:
        await msg.edit_text("**✅ ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛ sᴜᴄᴄᴇssғᴜʟʟʏ**")
        await message.delete()
    else:
        await msg.edit_text("**❌ ғᴀɪʟᴇᴅ ᴛᴏ sᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ**")
    
    await sleep(15)
    await message_deleter(message, msg)


# =============================================================================
#  ʙᴏᴛ sᴛᴀʀᴛᴜᴘ
# =============================================================================
logger.info("=" * 60)
logger.info("ʟᴇᴇᴄʜʙᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ")
logger.info("ᴅᴇᴠᴇʟᴏᴘᴇʀ: sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ (@sʜɪɴᴇɪɪ86)")
logger.info("ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86/ʟᴇᴇᴄʜʙᴏᴛ")
logger.info("=" * 60)

leechbot.run()
