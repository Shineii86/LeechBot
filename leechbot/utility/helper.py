# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ʟᴇᴇᴄʜʙᴏᴛ ʜᴇʟᴘᴇʀ ᴜᴛɪʟɪᴛɪᴇs

ᴛʜɪs ᴍᴏᴅᴜʟᴇ ᴄᴏɴᴛᴀɪɴs ᴠᴀʀɪᴏᴜs ʜᴇʟᴘᴇʀ ғᴜɴᴄᴛɪᴏɴs ғᴏʀ ғɪʟᴇ ᴏᴘᴇʀᴀᴛɪᴏɴs,
sʏsᴛᴇᴍ ɪɴғᴏʀᴍᴀᴛɪᴏɴ, ᴍᴇssᴀɢᴇ ʜᴀɴᴅʟɪɴɢ, ᴀɴᴅ ᴜɪ ᴜᴘᴅᴀᴛᴇs.
"""

import os
import math
import psutil
import logging
from time import time
from PIL import Image
from os import path as ospath
from datetime import datetime
from urllib.parse import urlparse
from asyncio import get_event_loop
from leechbot import leechbot
from pyrogram.errors import BadRequest
from moviepy.video.io.VideoFileClip import VideoFileClip
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from leechbot.utility.variables import BOT, MSG, BotTimes, Messages, Paths

logger = logging.getLogger(__name__)


# =============================================================================
#  ʟɪɴᴋ ᴠᴀʟɪᴅᴀᴛɪᴏɴ
# =============================================================================
def isLink(_, __, update):
    """
    ᴠᴀʟɪᴅᴀᴛᴇ ɪғ ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴄᴏɴᴛᴀɪɴs ᴀ ᴠᴀʟɪᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ.
    
    ᴀʀɢs:
        ᴜᴘᴅᴀᴛᴇ: ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴜᴘᴅᴀᴛᴇ ᴏʙᴊᴇᴄᴛ
    
    ʀᴇᴛᴜʀɴs:
        ʙᴏᴏʟ: ᴛʀᴜᴇ ɪғ ᴠᴀʟɪᴅ ʟɪɴᴋ ғᴏᴜɴᴅ
    """
    if update.text:
        # ʟᴏᴄᴀʟ ᴘᴀᴛʜs
        if "/content/" in str(update.text) or "/home" in str(update.text):
            return True
        # ᴍᴀɢɴᴇᴛ ʟɪɴᴋs
        elif update.text.startswith("magnet:?xt=urn:btih:"):
            return True
        
        parsed = urlparse(update.text)
        
        # ʜᴛᴛᴘ/ʜᴛᴛᴘs ᴜʀʟs
        if parsed.scheme in ("http", "https") and parsed.netloc:
            return True
    
    return False


def is_google_drive(link: str) -> bool:
    """ᴄʜᴇᴄᴋ ɪғ ʟɪɴᴋ ɪs ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ"""
    return "drive.google.com" in link


def is_mega(link: str) -> bool:
    """ᴄʜᴇᴄᴋ ɪғ ʟɪɴᴋ ɪs ᴍᴇɢᴀ.ɴᴢ"""
    return "mega.nz" in link


def is_terabox(link: str) -> bool:
    """ᴄʜᴇᴄᴋ ɪғ ʟɪɴᴋ ɪs ᴛᴇʀᴀʙᴏx"""
    return "terabox" in link or "1024tera" in link


def is_ytdl_link(link: str) -> bool:
    """ᴄʜᴇᴄᴋ ɪғ ʟɪɴᴋ ɪs ʏᴏᴜᴛᴜʙᴇ/ʏᴛ-ᴅʟᴘ sᴜᴘᴘᴏʀᴛᴇᴅ"""
    return "youtube.com" in link or "youtu.be" in link


def is_telegram(link: str) -> bool:
    """ᴄʜᴇᴄᴋ ɪғ ʟɪɴᴋ ɪs ᴛᴇʟᴇɢʀᴀᴍ"""
    return "t.me" in link


def is_torrent(link: str) -> bool:
    """ᴄʜᴇᴄᴋ ɪғ ʟɪɴᴋ ɪs ᴛᴏʀʀᴇɴᴛ/ᴍᴀɢɴᴇᴛ"""
    return "magnet" in link or ".torrent" in link


# =============================================================================
#  ᴛɪᴍᴇ ғᴏʀᴍᴀᴛᴛɪɴɢ
# =============================================================================
def getTime(seconds: int) -> str:
    """
    ᴄᴏɴᴠᴇʀᴛ sᴇᴄᴏɴᴅs ᴛᴏ ʜᴜᴍᴀɴ-ʀᴇᴀᴅᴀʙʟᴇ ғᴏʀᴍᴀᴛ.
    
    ᴀʀɢs:
        sᴇᴄᴏɴᴅs: ᴛɪᴍᴇ ɪɴ sᴇᴄᴏɴᴅs
    
    ʀᴇᴛᴜʀɴs:
        sᴛʀ: ғᴏʀᴍᴀᴛᴛᴇᴅ ᴛɪᴍᴇ sᴛʀɪɴɢ
    """
    seconds = int(seconds)
    days = seconds // (24 * 3600)
    seconds = seconds % (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    if days > 0:
        return f"{days}ᴅ {hours}ʜ {minutes}ᴍ {seconds}s"
    elif hours > 0:
        return f"{hours}ʜ {minutes}ᴍ {seconds}s"
    elif minutes > 0:
        return f"{minutes}ᴍ {seconds}s"
    else:
        return f"{seconds}s"


# =============================================================================
#  sɪᴢᴇ ғᴏʀᴍᴀᴛᴛɪɴɢ
# =============================================================================
def sizeUnit(size: float) -> str:
    """
    ᴄᴏɴᴠᴇʀᴛ ʙʏᴛᴇs ᴛᴏ ʜᴜᴍᴀɴ-ʀᴇᴀᴅᴀʙʟᴇ sɪᴢᴇ.
    
    ᴀʀɢs:
        sɪᴢᴇ: sɪᴢᴇ ɪɴ ʙʏᴛᴇs
    
    ʀᴇᴛᴜʀɴs:
        sᴛʀ: ғᴏʀᴍᴀᴛᴛᴇᴅ sɪᴢᴇ sᴛʀɪɴɢ
    """
    if size > 1024 ** 5:
        return f"{size / (1024 ** 5):.2f} ᴘɪʙ"
    elif size > 1024 ** 4:
        return f"{size / (1024 ** 4):.2f} ᴛɪʙ"
    elif size > 1024 ** 3:
        return f"{size / (1024 ** 3):.2f} ɢɪʙ"
    elif size > 1024 ** 2:
        return f"{size / (1024 ** 2):.2f} ᴍɪʙ"
    elif size > 1024:
        return f"{size / 1024:.2f} ᴋɪʙ"
    else:
        return f"{size:.2f} ʙ"


# =============================================================================
#  ғɪʟᴇ ᴛʏᴘᴇ ᴅᴇᴛᴇᴄᴛɪᴏɴ
# =============================================================================
def fileType(file_path: str) -> str:
    """
    ᴅᴇᴛᴇᴄᴛ ғɪʟᴇ ᴛʏᴘᴇ ʙᴀsᴇᴅ ᴏɴ ᴇxᴛᴇɴsɪᴏɴ.
    
    ᴀʀɢs:
        ғɪʟᴇ_ᴘᴀᴛʜ: ᴘᴀᴛʜ ᴛᴏ ᴛʜᴇ ғɪʟᴇ
    
    ʀᴇᴛᴜʀɴs:
        sᴛʀ: ғɪʟᴇ ᴛʏᴘᴇ (ᴠɪᴅᴇᴏ, ᴀᴜᴅɪᴏ, ᴘʜᴏᴛᴏ, ᴅᴏᴄᴜᴍᴇɴᴛ)
    """
    extensions_dict = {
        # ᴠɪᴅᴇᴏ ғᴏʀᴍᴀᴛs
        ".mp4": "video", ".avi": "video", ".mkv": "video",
        ".m2ts": "video", ".mov": "video", ".ts": "video",
        ".m3u8": "video", ".webm": "video", ".mpg": "video",
        ".mpeg": "video", ".mpeg4": "video", ".vob": "video",
        ".m4v": "video", ".flv": "video", ".wmv": "video",
        # ᴀᴜᴅɪᴏ ғᴏʀᴍᴀᴛs
        ".mp3": "audio", ".wav": "audio", ".flac": "audio",
        ".aac": "audio", ".ogg": "audio", ".m4a": "audio",
        ".wma": "audio", ".opus": "audio",
        # ɪᴍᴀɢᴇ ғᴏʀᴍᴀᴛs
        ".jpg": "photo", ".jpeg": "photo", ".png": "photo",
        ".bmp": "photo", ".gif": "photo", ".webp": "photo",
        ".tiff": "photo",
    }
    
    _, extension = ospath.splitext(file_path)
    return extensions_dict.get(extension.lower(), "document")


# =============================================================================
#  ғɪʟᴇɴᴀᴍᴇ ʜᴀɴᴅʟɪɴɢ
# =============================================================================
def shortFileName(path: str) -> str:
    """
    ᴛʀᴜɴᴄᴀᴛᴇ ғɪʟᴇɴᴀᴍᴇ ᴛᴏ ғɪᴛ ᴛᴇʟᴇɢʀᴀᴍ ʟɪᴍɪᴛs.
    
    ᴀʀɢs:
        ᴘᴀᴛʜ: ғɪʟᴇ ᴏʀ ᴅɪʀᴇᴄᴛᴏʀʏ ᴘᴀᴛʜ
    
    ʀᴇᴛᴜʀɴs:
        sᴛʀ: ᴛʀᴜɴᴄᴀᴛᴇᴅ ᴘᴀᴛʜ
    """
    max_len = 60
    
    if ospath.isfile(path):
        dir_path, filename = ospath.split(path)
        if len(filename) > max_len:
            basename, ext = ospath.splitext(filename)
            basename = basename[:max_len - len(ext)]
            filename = basename + ext
            path = ospath.join(dir_path, filename)
        return path
    elif ospath.isdir(path):
        dir_path, dirname = ospath.split(path)
        if len(dirname) > max_len:
            dirname = dirname[:max_len]
            path = ospath.join(dir_path, dirname)
        return path
    else:
        return path[:max_len] if len(path) > max_len else path


# =============================================================================
#  ғɪʟᴇ sɪᴢᴇ ᴄᴀʟᴄᴜʟᴀᴛɪᴏɴ
# =============================================================================
def getSize(path: str) -> int:
    """
    ɢᴇᴛ ᴛᴏᴛᴀʟ sɪᴢᴇ ᴏғ ғɪʟᴇ ᴏʀ ᴅɪʀᴇᴄᴛᴏʀʏ.
    
    ᴀʀɢs:
        ᴘᴀᴛʜ: ғɪʟᴇ ᴏʀ ᴅɪʀᴇᴄᴛᴏʀʏ ᴘᴀᴛʜ
    
    ʀᴇᴛᴜʀɴs:
        ɪɴᴛ: ᴛᴏᴛᴀʟ sɪᴢᴇ ɪɴ ʙʏᴛᴇs
    """
    if ospath.isfile(path):
        return ospath.getsize(path)
    
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = ospath.join(dirpath, f)
            total_size += ospath.getsize(fp)
    return total_size


# =============================================================================
#  ᴠɪᴅᴇᴏ ᴇxᴛᴇɴsɪᴏɴ ғɪx
# =============================================================================
def videoExtFix(file_path: str) -> str:
    """
    ғɪx ᴠɪᴅᴇᴏ ғɪʟᴇ ᴇxᴛᴇɴsɪᴏɴ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ.
    
    ᴀʀɢs:
        ғɪʟᴇ_ᴘᴀᴛʜ: ᴘᴀᴛʜ ᴛᴏ ᴠɪᴅᴇᴏ ғɪʟᴇ
    
    ʀᴇᴛᴜʀɴs:
        sᴛʀ: ғɪxᴇᴅ ғɪʟᴇ ᴘᴀᴛʜ
    """
    _, f_name = ospath.split(file_path)
    if f_name.endswith(".mp4") or f_name.endswith(".mkv"):
        return file_path
    
    new_path = file_path + ".mp4"
    os.rename(file_path, new_path)
    return new_path


# =============================================================================
#  ᴛʜᴜᴍʙɴᴀɪʟ ɢᴇɴᴇʀᴀᴛɪᴏɴ
# =============================================================================
def thumbMaintainer(file_path: str):
    """
    ɢᴇɴᴇʀᴀᴛᴇ ᴏʀ ʀᴇᴛʀɪᴇᴠᴇ ᴛʜᴜᴍʙɴᴀɪʟ ғᴏʀ ᴠɪᴅᴇᴏ.
    
    ᴀʀɢs:
        ғɪʟᴇ_ᴘᴀᴛʜ: ᴘᴀᴛʜ ᴛᴏ ᴠɪᴅᴇᴏ ғɪʟᴇ
    
    ʀᴇᴛᴜʀɴs:
        ᴛᴜᴘʟᴇ: (ᴛʜᴜᴍʙɴᴀɪʟ_ᴘᴀᴛʜ, ᴅᴜʀᴀᴛɪᴏɴ)
    """
    if ospath.exists(Paths.VIDEO_FRAME):
        os.remove(Paths.VIDEO_FRAME)
    
    try:
        fname, _ = ospath.splitext(ospath.basename(file_path))
        ytdl_thmb = f"{Paths.WORK_PATH}/ytdl_thumbnails/{fname}.webp"
        
        with VideoFileClip(file_path) as video:
            # ᴜsᴇ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ɪғ sᴇᴛ
            if ospath.exists(Paths.THMB_PATH):
                return Paths.THMB_PATH, video.duration
            # ᴜsᴇ ʏᴛ-ᴅʟᴘ ᴛʜᴜᴍʙɴᴀɪʟ ɪғ ᴀᴠᴀɪʟᴀʙʟᴇ
            elif ospath.exists(ytdl_thmb):
                return convertIMG(ytdl_thmb), video.duration
            # ɢᴇɴᴇʀᴀᴛᴇ ғʀᴏᴍ ᴠɪᴅᴇᴏ
            else:
                video.save_frame(Paths.VIDEO_FRAME, t=math.floor(video.duration / 2))
                return Paths.VIDEO_FRAME, video.duration
    
    except Exception as e:
        logger.error(f"ᴛʜᴜᴍʙɴᴀɪʟ ɢᴇɴᴇʀᴀᴛɪᴏɴ ᴇʀʀᴏʀ: {e}")
        if ospath.exists(Paths.THMB_PATH):
            return Paths.THMB_PATH, 0
        return Paths.HERO_IMAGE, 0


# =============================================================================
#  ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛᴛɪɴɢ
# =============================================================================
async def setThumbnail(message):
    """
    sᴀᴠᴇ ᴜsᴇʀ sᴇɴᴛ ɪᴍᴀɢᴇ ᴀs ᴛʜᴜᴍʙɴᴀɪʟ.
    
    ᴀʀɢs:
        ᴍᴇssᴀɢᴇ: ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ ᴘʜᴏᴛᴏ
    
    ʀᴇᴛᴜʀɴs:
        ʙᴏᴏʟ: sᴜᴄᴄᴇss sᴛᴀᴛᴜs
    """
    try:
        if ospath.exists(Paths.THMB_PATH):
            os.remove(Paths.THMB_PATH)
        
        event_loop = get_event_loop()
        download_task = event_loop.create_task(
            message.download(file_name=Paths.THMB_PATH)
        )
        await download_task
        
        BOT.Setting.thumbnail = True
        
        if BOT.State.task_going and MSG.status_msg:
            await MSG.status_msg.edit_media(
                InputMediaPhoto(Paths.THMB_PATH),
                reply_markup=keyboard()
            )
        return True
    
    except Exception as e:
        BOT.Setting.thumbnail = False
        logger.error(f"ᴛʜᴜᴍʙɴᴀɪʟ ᴅᴏᴡɴʟᴏᴀᴅ ᴇʀʀᴏʀ: {e}")
        return False


# =============================================================================
#  ʏᴛ-ᴅʟᴘ ᴄᴏᴍᴘʟᴇᴛɪᴏɴ ᴄʜᴇᴄᴋ
# =============================================================================
def isYtdlComplete() -> bool:
    """
    ᴄʜᴇᴄᴋ ɪғ ʏᴛ-ᴅʟᴘ ʜᴀs ғɪɴɪsʜᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ.
    
    ʀᴇᴛᴜʀɴs:
        ʙᴏᴏʟ: ᴛʀᴜᴇ ɪғ ɴᴏ .ᴘᴀʀᴛ ᴏʀ .ʏᴛᴅʟ ғɪʟᴇs ғᴏᴜɴᴅ
    """
    for _, _, filenames in os.walk(Paths.down_path):
        for f in filenames:
            _, ext = ospath.splitext(f)
            if ext in [".part", ".ytdl"]:
                return False
    return True


# =============================================================================
#  ɪᴍᴀɢᴇ ᴄᴏɴᴠᴇʀsɪᴏɴ
# =============================================================================
def convertIMG(image_path: str) -> str:
    """
    ᴄᴏɴᴠᴇʀᴛ ɪᴍᴀɢᴇ ᴛᴏ ᴊᴘᴇɢ ғᴏʀᴍᴀᴛ.
    
    ᴀʀɢs:
        ɪᴍᴀɢᴇ_ᴘᴀᴛʜ: ᴘᴀᴛʜ ᴛᴏ ɪᴍᴀɢᴇ ғɪʟᴇ
    
    ʀᴇᴛᴜʀɴs:
        sᴛʀ: ᴘᴀᴛʜ ᴛᴏ ᴄᴏɴᴠᴇʀᴛᴇᴅ ɪᴍᴀɢᴇ
    """
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    output_path = ospath.splitext(image_path)[0] + ".jpg"
    image.save(output_path, "JPEG")
    os.remove(image_path)
    return output_path


# =============================================================================
#  sʏsᴛᴇᴍ ɪɴғᴏʀᴍᴀᴛɪᴏɴ
# =============================================================================
def sysINFO() -> str:
    """
    ɢᴇᴛ sʏsᴛᴇᴍ ʀᴇsᴏᴜʀᴄᴇ ᴜsᴀɢᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.
    
    ʀᴇᴛᴜʀɴs:
        sᴛʀ: ғᴏʀᴍᴀᴛᴛᴇᴅ sʏsᴛᴇᴍ ɪɴғᴏ sᴛʀɪɴɢ
    """
    ram_usage = psutil.Process(os.getpid()).memory_info().rss
    disk_usage = psutil.disk_usage("/")
    cpu_usage = psutil.cpu_percent(interval=0.1)
    
    info = f"""

⌬───── **sʏsᴛᴇᴍ ɪɴғᴏ** ─────⌬

╭🖥️ **ᴄᴘᴜ:** `{cpu_usage}%`
├💽 **ʀᴀᴍ:** `{sizeUnit(ram_usage)}`
╰💾 **ᴅɪsᴋ:** `{sizeUnit(disk_usage.free)}`"""
    
    return info


# =============================================================================
#  ᴍᴜʟᴛɪᴘᴀʀᴛ ᴀʀᴄʜɪᴠᴇ ʜᴀɴᴅʟɪɴɢ
# =============================================================================
def multipartArchive(path: str, archive_type: str, remove: bool):
    """
    ʜᴀɴᴅʟᴇ ᴍᴜʟᴛɪᴘᴀʀᴛ ᴀʀᴄʜɪᴠᴇ ғɪʟᴇs.
    
    ᴀʀɢs:
        ᴘᴀᴛʜ: ᴘᴀᴛʜ ᴛᴏ ᴀʀᴄʜɪᴠᴇ
        ᴀʀᴄʜɪᴠᴇ_ᴛʏᴘᴇ: ᴛʏᴘᴇ ᴏғ ᴀʀᴄʜɪᴠᴇ (ʀᴀʀ, 7ᴢ, ᴢɪᴘ)
        ʀᴇᴍᴏᴠᴇ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀʀᴄʜɪᴠᴇs
    
    ʀᴇᴛᴜʀɴs:
        ᴛᴜᴘʟᴇ: (ʀᴇᴀʟ_ɴᴀᴍᴇ, ᴛᴏᴛᴀʟ_sɪᴢᴇ)
    """
    dirname, filename = ospath.split(path)
    name, _ = ospath.splitext(filename)
    
    count, size, real_name = 1, 0, name
    
    if archive_type == "rar":
        name_, _ = ospath.splitext(name)
        real_name = name_
        part_name = f"{name_}.part{count}.rar"
        part_path = ospath.join(dirname, part_name)
        
        while ospath.exists(part_path):
            if remove:
                os.remove(part_path)
            size += getSize(part_path)
            count += 1
            part_name = f"{name_}.part{count}.rar"
            part_path = ospath.join(dirname, part_name)
    
    elif archive_type == "7z":
        part_name = f"{name}.{str(count).zfill(3)}"
        part_path = ospath.join(dirname, part_name)
        
        while ospath.exists(part_path):
            if remove:
                os.remove(part_path)
            size += getSize(part_path)
            count += 1
            part_name = f"{name}.{str(count).zfill(3)}"
            part_path = ospath.join(dirname, part_name)
    
    elif archive_type == "zip":
        zip_path = ospath.join(dirname, f"{name}.zip")
        if ospath.exists(zip_path):
            if remove:
                os.remove(zip_path)
            size += getSize(zip_path)
        
        part_name = f"{name}.z{str(count).zfill(2)}"
        part_path = ospath.join(dirname, part_name)
        
        while ospath.exists(part_path):
            if remove:
                os.remove(part_path)
            size += getSize(part_path)
            count += 1
            part_name = f"{name}.z{str(count).zfill(2)}"
            part_path = ospath.join(dirname, part_name)
        
        if real_name.endswith(".zip"):
            real_name, _ = ospath.splitext(real_name)
    
    return real_name, size


# =============================================================================
#  ᴛɪᴍᴇ ᴄʜᴇᴄᴋ
# =============================================================================
def isTimeOver() -> bool:
    """
    ᴄʜᴇᴄᴋ ɪғ 3 sᴇᴄᴏɴᴅs ʜᴀᴠᴇ ᴘᴀssᴇᴅ sɪɴᴄᴇ ʟᴀsᴛ ᴜᴘᴅᴀᴛᴇ.
    
    ʀᴇᴛᴜʀɴs:
        ʙᴏᴏʟ: ᴛʀᴜᴇ ɪғ ᴛɪᴍᴇ ʜᴀs ᴘᴀssᴇᴅ
    """
    elapsed = time() - BotTimes.current_time
    if elapsed >= 3:
        BotTimes.current_time = time()
        return True
    return False


# =============================================================================
#  ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ ᴀᴘᴘʟɪᴄᴀᴛɪᴏɴ
# =============================================================================
def applyCustomName():
    """
    ᴀᴘᴘʟʏ ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ғɪʟᴇs.
    """
    if BOT.Options.custom_name and BOT.Mode.type not in ["zip", "undzip"]:
        files = os.listdir(Paths.down_path)
        for file_ in files:
            current_name = ospath.join(Paths.down_path, file_)
            new_name = ospath.join(Paths.down_path, BOT.Options.custom_name)
            os.rename(current_name, new_name)


# =============================================================================
#  sᴘᴇᴇᴅ ᴀɴᴅ ᴇᴛᴀ ᴄᴀʟᴄᴜʟᴀᴛɪᴏɴ
# =============================================================================
def speedETA(start_time: datetime, done: int, total: int):
    """
    ᴄᴀʟᴄᴜʟᴀᴛᴇ ᴅᴏᴡɴʟᴏᴀᴅ sᴘᴇᴇᴅ ᴀɴᴅ ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ.
    
    ᴀʀɢs:
        sᴛᴀʀᴛ_ᴛɪᴍᴇ: ᴅᴏᴡɴʟᴏᴀᴅ sᴛᴀʀᴛ ᴛɪᴍᴇ
        ᴅᴏɴᴇ: ʙʏᴛᴇs ᴄᴏᴍᴘʟᴇᴛᴇᴅ
        ᴛᴏᴛᴀʟ: ᴛᴏᴛᴀʟ ʙʏᴛᴇs
    
    ʀᴇᴛᴜʀɴs:
        ᴛᴜᴘʟᴇ: (sᴘᴇᴇᴅ, ᴇᴛᴀ, ᴘᴇʀᴄᴇɴᴛᴀɢᴇ)
    """
    percentage = (done / total) * 100 if total > 0 else 0
    percentage = min(percentage, 100)
    
    elapsed = (datetime.now() - start_time).seconds
    
    if done > 0 and elapsed > 0:
        raw_speed = done / elapsed
        speed = f"{sizeUnit(raw_speed)}/s"
        eta = (total - done) / raw_speed if raw_speed > 0 else 0
    else:
        speed, eta = "ɴ/ᴀ", 0
    
    return speed, eta, percentage


# =============================================================================
#  ᴍᴇssᴀɢᴇ ᴅᴇʟᴇᴛɪᴏɴ
# =============================================================================
async def message_deleter(msg1, msg2):
    """
    sᴀғᴇʟʏ ᴅᴇʟᴇᴛᴇ ᴛᴡᴏ ᴍᴇssᴀɢᴇs.
    
    ᴀʀɢs:
        ᴍsɢ1: ғɪʀsᴛ ᴍᴇssᴀɢᴇ
        ᴍsɢ2: sᴇᴄᴏɴᴅ ᴍᴇssᴀɢᴇ
    """
    try:
        await msg1.delete()
    except Exception as e:
        logger.error(f"ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍsɢ1: {e}")
    
    try:
        await msg2.delete()
    except Exception as e:
        logger.error(f"ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍsɢ2: {e}")


# =============================================================================
#  sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ
# =============================================================================
async def send_settings(client, message, msg_id: int, is_command: bool):
    """
    sᴇɴᴅ ᴏʀ ᴇᴅɪᴛ sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ.
    
    ᴀʀɢs:
        ᴄʟɪᴇɴᴛ: ᴘʏʀᴏɢʀᴀᴍ ᴄʟɪᴇɴᴛ
        ᴍᴇssᴀɢᴇ: ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇ
        ᴍsɢ_ɪᴅ: ᴍᴇssᴀɢᴇ ɪᴅ ᴛᴏ ᴇᴅɪᴛ
        ɪs_ᴄᴏᴍᴍᴀɴᴅ: ᴡʜᴇᴛʜᴇʀ ᴛʜɪs ɪs ᴀ ɴᴇᴡ ᴄᴏᴍᴍᴀɴᴅ
    """
    up_mode = "ᴅᴏᴄᴜᴍᴇɴᴛ" if not BOT.Options.stream_upload else "ᴍᴇᴅɪᴀ"
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"📤 {up_mode}", callback_data="media" if up_mode == "ᴅᴏᴄᴜᴍᴇɴᴛ" else "document"),
                InlineKeyboardButton("🎬 ᴠɪᴅᴇᴏ", callback_data="video"),
            ],
            [
                InlineKeyboardButton("📝 ᴄᴀᴘᴛɪᴏɴ", callback_data="caption"),
                InlineKeyboardButton("🖼️ ᴛʜᴜᴍʙ", callback_data="thumb"),
            ],
            [
                InlineKeyboardButton("➕ sᴜғғɪx", callback_data="set-suffix"),
                InlineKeyboardButton("➕ ᴘʀᴇғɪx", callback_data="set-prefix"),
            ],
            [InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close")],
        ]
    )
    
    pr = "✅" if BOT.Setting.prefix else "❌"
    su = "✅" if BOT.Setting.suffix else "❌"
    thmb = "✅" if BOT.Setting.thumbnail else "❌"
    
    text = f"""**⚙️ ʙᴏᴛ sᴇᴛᴛɪɴɢs**

╭📤 **ᴜᴘʟᴏᴀᴅ:** `{BOT.Setting.stream_upload}`
├✂️ **sᴘʟɪᴛ:** `{BOT.Setting.split_video}`
├🔄 **ᴄᴏɴᴠᴇʀᴛ:** `{BOT.Setting.convert_video}`
├📝 **ᴄᴀᴘᴛɪᴏɴ:** `{BOT.Setting.caption}`
├➕ **ᴘʀᴇғɪx:** {pr}
├➕ **sᴜғғɪx:** {su}
╰🖼️ **ᴛʜᴜᴍʙ:** {thmb}"""
    
    try:
        if is_command:
            await message.reply_text(text=text, reply_markup=keyboard)
        else:
            await leechbot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg_id,
                text=text,
                reply_markup=keyboard
            )
    except BadRequest as e:
        logger.error(f"sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ ᴇʀʀᴏʀ: {e}")
    except Exception as e:
        logger.error(f"sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ ᴇʀʀᴏʀ: {e}")


# =============================================================================
#  sᴛᴀᴛᴜs ʙᴀʀ ᴜᴘᴅᴀᴛᴇ
# =============================================================================
async def status_bar(down_msg: str, speed: str, percentage: float, eta: str, done: str, left: str, engine: str):
    """
    ᴜᴘᴅᴀᴛᴇ ᴅᴏᴡɴʟᴏᴀᴅ/ᴜᴘʟᴏᴀᴅ sᴛᴀᴛᴜs ʙᴀʀ.
    
    ᴀʀɢs:
        ᴅᴏᴡɴ_ᴍsɢ: sᴛᴀᴛᴜs ʜᴇᴀᴅᴇʀ ᴍᴇssᴀɢᴇ
        sᴘᴇᴇᴅ: ᴄᴜʀʀᴇɴᴛ sᴘᴇᴇᴅ
        ᴘᴇʀᴄᴇɴᴛᴀɢᴇ: ᴄᴏᴍᴘʟᴇᴛɪᴏɴ ᴘᴇʀᴄᴇɴᴛᴀɢᴇ
        ᴇᴛᴀ: ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ
        ᴅᴏɴᴇ: ʙʏᴛᴇs ᴘʀᴏᴄᴇssᴇᴅ
        ʟᴇғᴛ: ʙʏᴛᴇs ʀᴇᴍᴀɪɴɪɴɢ
        ᴇɴɢɪɴᴇ: ᴅᴏᴡɴʟᴏᴀᴅ ᴇɴɢɪɴᴇ ɴᴀᴍᴇ
    """
    bar_length = 12
    filled = int(percentage / 100 * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    text = f"""
╭「{bar}」 **»** `{percentage:.1f}%`
├⚡ **sᴘᴇᴇᴅ:** `{speed}`
├🔧 **ᴇɴɢɪɴᴇ:** `{engine}`
├⏳ **ᴇᴛᴀ:** `{eta}`
├⏱️ **ᴇʟᴀᴘsᴇᴅ:** `{getTime((datetime.now() - BotTimes.start_time).seconds)}`
├✅ **ᴅᴏɴᴇ:** `{done}`
╰📦 **ᴛᴏᴛᴀʟ:** `{left}`"""
    
    try:
        if isTimeOver():
            await MSG.status_msg.edit_text(
                text=Messages.task_msg + down_msg + text + sysINFO(),
                disable_web_page_preview=True,
                reply_markup=keyboard()
            )
    except BadRequest as e:
        logger.error(f"sᴛᴀᴛᴜs ʙᴀʀ ᴇʀʀᴏʀ: {e}")
    except Exception as e:
        logger.error(f"sᴛᴀᴛᴜs ʙᴀʀ ᴇʀʀᴏʀ: {e}")


# =============================================================================
#  ᴄᴀɴᴄᴇʟ ᴋᴇʏʙᴏᴀʀᴅ
# =============================================================================
def keyboard():
    """
    ɢᴇɴᴇʀᴀᴛᴇ ᴄᴀɴᴄᴇʟ ʙᴜᴛᴛᴏɴ ᴋᴇʏʙᴏᴀʀᴅ.
    
    ʀᴇᴛᴜʀɴs:
        ɪɴʟɪɴᴇᴋᴇʏʙᴏᴀʀᴅᴍᴀʀᴋᴜᴘ: ᴄᴀɴᴄᴇʟ ʙᴜᴛᴛᴏɴ
    """
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="cancel")]]
    )
