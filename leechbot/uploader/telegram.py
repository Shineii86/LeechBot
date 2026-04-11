# =============================================================================
# Telegram Leech Bot - Telegram Uploader
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
Telegram uploader module.

Handles uploading files to Telegram with progress tracking.
"""

import logging
from PIL import Image
from asyncio import sleep
from os import path as ospath
from datetime import datetime
from pyrogram.errors import FloodWait
from leechbot.utility.variables import BOT, Transfer, BotTimes, Messages, MSG, Paths
from leechbot.utility.helper import sizeUnit, fileType, getTime, status_bar, thumbMaintainer, videoExtFix
from leechbot.utility.style import style_text

logger = logging.getLogger(__name__)


# =============================================================================
# Upload Progress Callback
# =============================================================================
async def progress_bar(current: int, total: int):
    """
    Update upload progress.
    
    Args:
        current: bytes uploaded
        total: total bytes
    """
    elapsed = (datetime.now() - BotTimes.task_start).seconds
    
    if current > 0 and elapsed > 0:
        upload_speed = current / elapsed
    else:
        upload_speed = 4 * 1024 * 1024  # Default 4MB/s
    
    remaining = Transfer.total_down_size - current - sum(Transfer.up_bytes)
    eta = remaining / upload_speed if upload_speed > 0 else 0
    percentage = (current + sum(Transfer.up_bytes)) / Transfer.total_down_size * 100
    
    await status_bar(
        down_msg=Messages.status_head,
        speed=f"{sizeUnit(upload_speed)}/s",
        percentage=percentage,
        eta=getTime(eta),
        done=sizeUnit(current + sum(Transfer.up_bytes)),
        left=sizeUnit(Transfer.total_down_size),
        engine="Telegram 📤"
    )


# =============================================================================
# Main Upload Function
# =============================================================================
async def upload_file(file_path: str, real_name: str):
    """
    Upload file to Telegram.
    
    Args:
        file_path: path to file
        real_name: original filename
    """
    global Transfer, MSG
    
    BotTimes.task_start = datetime.now()
    
    # Build styled caption
    caption = f"<{BOT.Options.caption}>{BOT.Setting.prefix} {real_name} {BOT.Setting.suffix}</{BOT.Options.caption}>"
    
    # Determine file type
    type_ = fileType(file_path)
    f_type = type_ if BOT.Options.stream_upload else "document"
    
    try:
        if f_type == "video":
            # Video upload
            if not BOT.Options.stream_upload:
                file_path = videoExtFix(file_path)
            
            thmb_path, seconds = thumbMaintainer(file_path)
            
            with Image.open(thmb_path) as img:
                width, height = img.size
            
            MSG.sent_msg = await MSG.sent_msg.reply_video(
                video=file_path,
                supports_streaming=True,
                width=width,
                height=height,
                caption=caption,
                thumb=thmb_path,
                duration=int(seconds),
                progress=progress_bar,
                reply_to_message_id=MSG.sent_msg.id
            )
        
        elif f_type == "audio":
            # Audio upload
            thmb_path = Paths.THMB_PATH if ospath.exists(Paths.THMB_PATH) else None
            
            MSG.sent_msg = await MSG.sent_msg.reply_audio(
                audio=file_path,
                caption=caption,
                thumb=thmb_path,
                progress=progress_bar,
                reply_to_message_id=MSG.sent_msg.id
            )
        
        elif f_type == "photo":
            # Photo upload
            MSG.sent_msg = await MSG.sent_msg.reply_photo(
                photo=file_path,
                caption=caption,
                progress=progress_bar,
                reply_to_message_id=MSG.sent_msg.id
            )
        
        else:
            # Document upload
            if ospath.exists(Paths.THMB_PATH):
                thmb_path = Paths.THMB_PATH
            elif type_ == "video":
                thmb_path, _ = thumbMaintainer(file_path)
            else:
                thmb_path = None
            
            MSG.sent_msg = await MSG.sent_msg.reply_document(
                document=file_path,
                caption=caption,
                thumb=thmb_path,
                progress=progress_bar,
                reply_to_message_id=MSG.sent_msg.id
            )
        
        # Track sent files
        Transfer.sent_file.append(MSG.sent_msg)
        Transfer.sent_file_names.append(real_name)
    
    except FloodWait as e:
        logger.warning(f"Flood wait: waiting {e.value} seconds")
        await sleep(e.value)
        await upload_file(file_path, real_name)
    
    except Exception as e:
        logger.error(f"Upload error: {e}")
