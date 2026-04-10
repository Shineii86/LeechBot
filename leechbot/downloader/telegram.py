# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ᴛᴇʟᴇɢʀᴀᴍ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ᴍᴏᴅᴜʟᴇ

ᴛʜɪs ᴍᴏᴅᴜʟᴇ ʜᴀɴᴅʟᴇs ᴅᴏᴡɴʟᴏᴀᴅs ғʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇs.
"""

import logging
from datetime import datetime
from os import path as ospath
from leechbot import leechbot
from leechbot.utility.handler import cancelTask
from leechbot.utility.variables import Transfer, Paths, Messages, BotTimes
from leechbot.utility.helper import speedETA, getTime, sizeUnit, status_bar

logger = logging.getLogger(__name__)


# =============================================================================
#  ᴍᴇᴅɪᴀ ɪᴅᴇɴᴛɪғɪᴄᴀᴛɪᴏɴ
# =============================================================================
async def media_Identifier(link: str):
    """
    ɪᴅᴇɴᴛɪғʏ ᴍᴇᴅɪᴀ ғʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ ʟɪɴᴋ.
    
    ᴀʀɢs:
        ʟɪɴᴋ: ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇ ʟɪɴᴋ
    
    ʀᴇᴛᴜʀɴs:
        ᴛᴜᴘʟᴇ: (ᴍᴇᴅɪᴀ, ᴍᴇssᴀɢᴇ)
    """
    parts = link.split("/")
    message_id = int(parts[-1])
    msg_chat_id = int("-100" + parts[4])
    
    try:
        message = await leechbot.get_messages(msg_chat_id, message_id)
    except Exception as e:
        logger.error(f"ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇ ᴇʀʀᴏʀ: {e}")
        return None, None
    
    if message is None:
        logger.error("ᴍᴇssᴀɢᴇ ɴᴏᴛ ғᴏᴜɴᴅ")
        return None, None
    
    # ɢᴇᴛ ᴍᴇᴅɪᴀ ғʀᴏᴍ ᴍᴇssᴀɢᴇ
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
#  ᴅᴏᴡɴʟᴏᴀᴅ ᴘʀᴏɢʀᴇss ᴄᴀʟʟʙᴀᴄᴋ
# =============================================================================
async def download_progress(current: int, total: int):
    """
    ᴜᴘᴅᴀᴛᴇ ᴅᴏᴡɴʟᴏᴀᴅ ᴘʀᴏɢʀᴇss.
    
    ᴀʀɢs:
        ᴄᴜʀʀᴇɴᴛ: ʙʏᴛᴇs ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ
        ᴛᴏᴛᴀʟ: ᴛᴏᴛᴀʟ ʙʏᴛᴇs
    """
    speed_string, eta, percentage = speedETA(start_time, current, total)
    
    await status_bar(
        down_msg=Messages.status_head,
        speed=speed_string,
        percentage=percentage,
        eta=getTime(eta),
        done=sizeUnit(sum(Transfer.down_bytes) + current),
        left=sizeUnit(Transfer.total_down_size),
        engine="ᴛᴇʟᴇɢʀᴀᴍ 💬"
    )


# =============================================================================
#  ᴍᴀɪɴ ᴅᴏᴡɴʟᴏᴀᴅ ғᴜɴᴄᴛɪᴏɴ
# =============================================================================
async def TelegramDownload(link: str, num: int):
    """
    ᴅᴏᴡɴʟᴏᴀᴅ ғɪʟᴇ ғʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ.
    
    ᴀʀɢs:
        ʟɪɴᴋ: ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇ ʟɪɴᴋ
        ɴᴜᴍ: ʟɪɴᴋ ɴᴜᴍʙᴇʀ ғᴏʀ ᴅɪsᴘʟᴀʏ
    """
    global start_time
    
    media, message = await media_Identifier(link)
    
    if media is None:
        logger.error("ᴄᴏᴜʟᴅ ɴᴏᴛ ɪᴅᴇɴᴛɪғʏ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇᴅɪᴀ")
        await cancelTask("ᴄᴏᴜʟᴅ ɴᴏᴛ ɪᴅᴇɴᴛɪғʏ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇᴅɪᴀ")
        return
    
    name = media.file_name if hasattr(media, "file_name") else "ᴜɴᴋɴᴏᴡɴ"
    Messages.status_head = f"**📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ** `ʟɪɴᴋ {str(num).zfill(2)}`\n\n`{name}`\n"
    
    start_time = datetime.now()
    file_path = ospath.join(Paths.down_path, name)
    
    await message.download(
        progress=download_progress,
        in_memory=False,
        file_name=file_path
    )
    
    Transfer.down_bytes.append(media.file_size)
