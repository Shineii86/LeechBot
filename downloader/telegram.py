# =============================================================================
# LeechBot Pro - Telegram Downloader
# =============================================================================
# Project   : LeechBot Pro v3.0
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://t.me/Shineii86
# =============================================================================

import logging
from datetime import datetime
from os import path as ospath

from colab_leecher import colab_bot
from colab_leecher.utility.handler import cancel_task
from colab_leecher.utility.variables import Transfer, Paths, Messages, BotTimes
from colab_leecher.utility.helper import (
    calculate_speed_eta, get_time_string, format_size, update_status_bar
)


# =============================================================================
# MEDIA IDENTIFIER
# =============================================================================
async def get_media_info(link: str) -> tuple:
    """
    Extract media from Telegram message link.
    
    Args:
        link: Telegram message URL (t.me/...)
        
    Returns:
        tuple: (media_object, message_object)
    """
    try:
        parts = link.split("/")
        message_id = int(parts[-1])
        
        # Handle private channel links
        if parts[-2].startswith("-100"):
            chat_id = int(parts[-2])
        else:
            chat_id = "-100" + parts[-2]
            chat_id = int(chat_id)
        
        message = await colab_bot.get_messages(chat_id, message_id)
        
        if not message:
            logging.error("Message not found")
            return None, None
        
        # Get media from message
        media = (
            message.document
            or message.video
            or message.audio
            or message.photo
            or message.voice
            or message.video_note
            or message.sticker
            or message.animation
        )
        
        if not media:
            logging.error("No media found in message")
            return None, None
        
        return media, message
        
    except Exception as e:
        logging.error(f"Media info error: {e}")
        return None, None


# =============================================================================
# DOWNLOAD PROGRESS
# =============================================================================
async def download_progress(current: int, total: int):
    """
    Update download progress for Telegram downloads.
    
    Args:
        current: Bytes downloaded
        total: Total bytes
    """
    speed, eta, percentage = calculate_speed_eta(
        BotTimes.task_start,
        sum(Transfer.down_bytes) + current,
        Transfer.total_down_size
    )
    
    await update_status_bar(
        down_msg=Messages.status_head,
        speed=speed,
        percentage=percentage,
        eta=get_time_string(eta),
        done=format_size(sum(Transfer.down_bytes) + current),
        left=format_size(Transfer.total_down_size),
        engine="Telegram",
    )


# =============================================================================
# MAIN DOWNLOAD FUNCTION
# =============================================================================
async def telegram_download(link: str, num: int):
    """
    Download media from Telegram message.
    
    Args:
        link: Telegram message URL
        num: Download number for display
    """
    global start_time
    
    media, message = await get_media_info(link)
    
    if not media:
        await cancel_task("Could not retrieve media from Telegram message")
        return
    
    # Get file name
    if hasattr(media, "file_name"):
        name = media.file_name
    elif hasattr(media, "mime_type"):
        # Generate name from mime type
        ext = media.mime_type.split("/")[-1]
        name = f"telegram_file_{num}.{ext}"
    else:
        name = f"telegram_file_{num}"
    
    Messages.status_head = (
        f"<b>📥 DOWNLOADING</b> <code>Link {num:02d}</code>\n\n"
        f"<code>{name}</code>\n"
    )
    
    # Setup download
    start_time = datetime.now()
    file_path = ospath.join(Paths.down_path, name)
    
    try:
        await message.download(
            progress=download_progress,
            in_memory=False,
            file_name=file_path
        )
        
        # Record downloaded size
        file_size = media.file_size or 0
        Transfer.down_bytes.append(file_size)
        
    except Exception as e:
        logging.error(f"Telegram download error: {e}")
        await cancel_task(f"Download failed: {e}")
