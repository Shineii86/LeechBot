# =============================================================================
# Telegram Leech Bot - Telegram Downloader
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
Telegram downloader module.

Handles downloads from Telegram messages.
"""

import logging
from datetime import datetime
from os import path as ospath
from leechbot import leechbot
from leechbot.utility.handler import cancelTask
from leechbot.utility.variables import Transfer, Paths, Messages, BotTimes
from leechbot.utility.helper import speedETA, getTime, sizeUnit, status_bar
from leechbot.utility.style import style_text

logger = logging.getLogger(__name__)


# =============================================================================
# Media Identification
# =============================================================================
async def media_Identifier(link: str):
    """
    Identify media from Telegram link.
    
    Args:
        link: Telegram message link
    
    Returns:
        tuple: (media, message)
    """
    parts = link.split("/")
    message_id = int(parts[-1])
    msg_chat_id = int("-100" + parts[4])
    
    try:
        message = await leechbot.get_messages(msg_chat_id, message_id)
    except Exception as e:
        logger.error(f"Telegram message error: {e}")
        return None, None
    
    if message is None:
        logger.error("Message not found")
        return None, None
    
    # Get media from message
    media = (
        message.document
        or message.photo
        or message.video
        or message.audio
        or message.voice
        or message.video_note
        or message.sticker
        or message.animation
    )
    
    return media, message


# =============================================================================
# Download Progress Callback
# =============================================================================
async def download_progress(current: int, total: int):
    """
    Update download progress.
    
    Args:
        current: bytes downloaded
        total: total bytes
    """
    speed_string, eta, percentage = speedETA(start_time, current, total)
    
    await status_bar(
        down_msg=Messages.status_head,
        speed=speed_string,
        percentage=percentage,
        eta=getTime(eta),
        done=sizeUnit(sum(Transfer.down_bytes) + current),
        left=sizeUnit(Transfer.total_down_size),
        engine="Telegram 💬"
    )


# =============================================================================
# Main Download Function
# =============================================================================
async def TelegramDownload(link: str, num: int):
    """
    Download file from Telegram.
    
    Args:
        link: Telegram message link
        num: link number for display
    """
    global start_time
    
    media, message = await media_Identifier(link)
    
    if media is None:
        logger.error("Could not identify Telegram media")
        await cancelTask(style_text("Could Not Identify Telegram Media"))
        return
    
    name = media.file_name if hasattr(media, "file_name") else "Unknown"
    Messages.status_head = style_text(f"**📥 Downloading** `Link {str(num).zfill(2)}`\n\n") + f"`{name}`\n"
    
    start_time = datetime.now()
    file_path = ospath.join(Paths.down_path, name)
    
    await message.download(
        progress=download_progress,
        in_memory=False,
        file_name=file_path
    )
    
    Transfer.down_bytes.append(media.file_size)
