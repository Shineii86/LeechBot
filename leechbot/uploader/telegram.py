# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ᴛᴇʟᴇɢʀᴀᴍ ᴜᴘʟᴏᴀᴅᴇʀ ᴍᴏᴅᴜʟᴇ

ᴛʜɪs ᴍᴏᴅᴜʟᴇ ʜᴀɴᴅʟᴇs ᴜᴘʟᴏᴀᴅɪɴɢ ғɪʟᴇs ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ᴡɪᴛʜ ᴘʀᴏɢʀᴇss ᴛʀᴀᴄᴋɪɴɢ.
"""

import logging
from PIL import Image
from asyncio import sleep
from os import path as ospath
from datetime import datetime
from pyrogram.errors import FloodWait
from leechbot.utility.variables import BOT, Transfer, BotTimes, Messages, MSG, Paths
from leechbot.utility.helper import sizeUnit, fileType, getTime, status_bar, thumbMaintainer, videoExtFix

logger = logging.getLogger(__name__)


# =============================================================================
#  ᴜᴘʟᴏᴀᴅ ᴘʀᴏɢʀᴇss ᴄᴀʟʟʙᴀᴄᴋ
# =============================================================================
async def progress_bar(current: int, total: int):
    """
    ᴜᴘᴅᴀᴛᴇ ᴜᴘʟᴏᴀᴅ ᴘʀᴏɢʀᴇss.
    
    ᴀʀɢs:
        ᴄᴜʀʀᴇɴᴛ: ʙʏᴛᴇs ᴜᴘʟᴏᴀᴅᴇᴅ
        ᴛᴏᴛᴀʟ: ᴛᴏᴛᴀʟ ʙʏᴛᴇs
    """
    elapsed = (datetime.now() - BotTimes.task_start).seconds
    
    if current > 0 and elapsed > 0:
        upload_speed = current / elapsed
    else:
        upload_speed = 4 * 1024 * 1024  # ᴅᴇғᴀᴜʟᴛ 4ᴍʙ/s
    
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
        engine="ᴛᴇʟᴇɢʀᴀᴍ 📤"
    )


# =============================================================================
#  ᴍᴀɪɴ ᴜᴘʟᴏᴀᴅ ғᴜɴᴄᴛɪᴏɴ
# =============================================================================
async def upload_file(file_path: str, real_name: str):
    """
    ᴜᴘʟᴏᴀᴅ ғɪʟᴇ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ.
    
    ᴀʀɢs:
        ғɪʟᴇ_ᴘᴀᴛʜ: ᴘᴀᴛʜ ᴛᴏ ғɪʟᴇ
        ʀᴇᴀʟ_ɴᴀᴍᴇ: ᴏʀɪɢɪɴᴀʟ ғɪʟᴇɴᴀᴍᴇ
    """
    global Transfer, MSG
    
    BotTimes.task_start = datetime.now()
    
    # ʙᴜɪʟᴅ ᴄᴀᴘᴛɪᴏɴ
    caption = f"<{BOT.Options.caption}>{BOT.Setting.prefix} {real_name} {BOT.Setting.suffix}</{BOT.Options.caption}>"
    
    # ᴅᴇᴛᴇʀᴍɪɴᴇ ғɪʟᴇ ᴛʏᴘᴇ
    type_ = fileType(file_path)
    f_type = type_ if BOT.Options.stream_upload else "document"
    
    try:
        if f_type == "video":
            # ᴠɪᴅᴇᴏ ᴜᴘʟᴏᴀᴅ
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
            # ᴀᴜᴅɪᴏ ᴜᴘʟᴏᴀᴅ
            thmb_path = Paths.THMB_PATH if ospath.exists(Paths.THMB_PATH) else None
            
            MSG.sent_msg = await MSG.sent_msg.reply_audio(
                audio=file_path,
                caption=caption,
                thumb=thmb_path,
                progress=progress_bar,
                reply_to_message_id=MSG.sent_msg.id
            )
        
        elif f_type == "photo":
            # ᴘʜᴏᴛᴏ ᴜᴘʟᴏᴀᴅ
            MSG.sent_msg = await MSG.sent_msg.reply_photo(
                photo=file_path,
                caption=caption,
                progress=progress_bar,
                reply_to_message_id=MSG.sent_msg.id
            )
        
        else:
            # ᴅᴏᴄᴜᴍᴇɴᴛ ᴜᴘʟᴏᴀᴅ
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
        
        # ᴛʀᴀᴄᴋ sᴇɴᴛ ғɪʟᴇs
        Transfer.sent_file.append(MSG.sent_msg)
        Transfer.sent_file_names.append(real_name)
    
    except FloodWait as e:
        logger.warning(f"ғʟᴏᴏᴅᴡᴀɪᴛ: ᴡᴀɪᴛɪɴɢ {e.value} sᴇᴄᴏɴᴅs")
        await sleep(e.value)
        await upload_file(file_path, real_name)
    
    except Exception as e:
        logger.error(f"ᴜᴘʟᴏᴀᴅ ᴇʀʀᴏʀ: {e}")
