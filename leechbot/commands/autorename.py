# =============================================================================
# Telegram Leech Bot - Auto-Rename Command
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================
# License   : MIT License
# =============================================================================

"""
Auto-rename template command.

Set a template for automatic file renaming using placeholders.
"""

import logging

from pyrogram import filters

from leechbot import app
from leechbot.utility.variables import BOT
from leechbot.utility.helper import message_deleter

logger = logging.getLogger(__name__)


@app.on_message(filters.command("autorename") & filters.private)
async def autorename_command(client, message):
    """Set auto-rename template for files."""
    if len(message.command) < 2:
        current_template = BOT.Setting.autorename_template
        status = f"<b>📝 Current Template:</b> <code>{current_template}</code>" if current_template else "<b>📝 No template set</b>"

        msg = await message.reply_text(
            f"<b>🏷️ Auto-Rename Template</b>\n\n"
            f"{status}\n\n"
            f"<b>⚠️ Usage:</b> <code>/autorename &lt;template&gt;</code>\n\n"
            f"<b>📝 Examples:</b>\n"
            f"• Manga: <code>/autorename [WF] [C{{chapter}}] One Piece @Webtoon_Flix</code>\n"
            f"• Video: <code>/autorename [S{{season}} E{{episode}}] One Piece [{{quality}}] [{{audio}}]</code>\n\n"
            f"<b>💡 Note:</b> Don't put .mkv or .mp4 at the end.\n"
            f"The bot will use this template to rename your files automatically.\n\n"
            f"<b>🗑️ To clear:</b> <code>/autorename clear</code>",
            quote=True,
        )
    elif message.command[1].lower() == "clear":
        BOT.Setting.autorename_template = ""
        msg = await message.reply_text("<b>✅ Auto-rename template cleared.</b>", quote=True)
    else:
        BOT.Setting.autorename_template = " ".join(message.command[1:])
        msg = await message.reply_text(
            f"<b>🏷️ Auto-Rename Template Set</b>\n\n"
            f"<b>📝 Template:</b> <code>{BOT.Setting.autorename_template}</code>\n\n"
            f"<b>💡 The bot will use this pattern to rename files.</b>",
            quote=True,
        )
    await message_deleter(message, msg)
