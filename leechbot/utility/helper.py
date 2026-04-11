# =============================================================================
# Telegram Leech Bot - Helper Utilities
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
Helper functions for file operations, formatting, and UI updates.
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
from leechbot.utility.style import style_text, style_button

logger = logging.getLogger(__name__)


# =============================================================================
# Link Validation
# =============================================================================
def isLink(_, __, update):
    """
    Validate if the message contains a valid download link.
    
    Args:
        update: the message update object
    
    Returns:
        bool: True if valid link found
    """
    if update.text:
        # Local paths
        if "/content/" in str(update.text) or "/home" in str(update.text):
            return True
        # Magnet links
        elif update.text.startswith("magnet:?xt=urn:btih:"):
            return True
        
        parsed = urlparse(update.text)
        
        # HTTP/HTTPS URLs
        if parsed.scheme in ("http", "https") and parsed.netloc:
            return True
    
    return False


def is_google_drive(link: str) -> bool:
    """Check if link is Google Drive"""
    return "drive.google.com" in link


def is_mega(link: str) -> bool:
    """Check if link is Mega.nz"""
    return "mega.nz" in link


def is_terabox(link: str) -> bool:
    """Check if link is Terabox"""
    return "terabox" in link or "1024tera" in link


def is_ytdl_link(link: str) -> bool:
    """Check if link is YouTube/YT-DLP supported"""
    return "youtube.com" in link or "youtu.be" in link


def is_telegram(link: str) -> bool:
    """Check if link is Telegram"""
    return "t.me" in link


def is_torrent(link: str) -> bool:
    """Check if link is torrent/magnet"""
    return "magnet" in link or ".torrent" in link


# =============================================================================
# Time Formatting
# =============================================================================
def getTime(seconds: int) -> str:
    """
    Convert seconds to human-readable format.
    
    Args:
        seconds: time in seconds
    
    Returns:
        str: formatted time string
    """
    seconds = int(seconds)
    days = seconds // (24 * 3600)
    seconds = seconds % (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m {seconds}s"
    elif hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


# =============================================================================
# Size Formatting
# =============================================================================
def sizeUnit(size: float) -> str:
    """
    Convert bytes to human-readable size.
    
    Args:
        size: size in bytes
    
    Returns:
        str: formatted size string
    """
    if size > 1024 ** 5:
        return f"{size / (1024 ** 5):.2f} PiB"
    elif size > 1024 ** 4:
        return f"{size / (1024 ** 4):.2f} TiB"
    elif size > 1024 ** 3:
        return f"{size / (1024 ** 3):.2f} GiB"
    elif size > 1024 ** 2:
        return f"{size / (1024 ** 2):.2f} MiB"
    elif size > 1024:
        return f"{size / 1024:.2f} KiB"
    else:
        return f"{size:.2f} B"


# =============================================================================
# File Type Detection
# =============================================================================
def fileType(file_path: str) -> str:
    """
    Detect file type based on extension.
    
    Args:
        file_path: path to the file
    
    Returns:
        str: file type (video, audio, photo, document)
    """
    extensions_dict = {
        # Video formats
        ".mp4": "video", ".avi": "video", ".mkv": "video",
        ".m2ts": "video", ".mov": "video", ".ts": "video",
        ".m3u8": "video", ".webm": "video", ".mpg": "video",
        ".mpeg": "video", ".mpeg4": "video", ".vob": "video",
        ".m4v": "video", ".flv": "video", ".wmv": "video",
        # Audio formats
        ".mp3": "audio", ".wav": "audio", ".flac": "audio",
        ".aac": "audio", ".ogg": "audio", ".m4a": "audio",
        ".wma": "audio", ".opus": "audio",
        # Image formats
        ".jpg": "photo", ".jpeg": "photo", ".png": "photo",
        ".bmp": "photo", ".gif": "photo", ".webp": "photo",
        ".tiff": "photo",
    }
    
    _, extension = ospath.splitext(file_path)
    return extensions_dict.get(extension.lower(), "document")


# =============================================================================
# Filename Handling
# =============================================================================
def shortFileName(path: str) -> str:
    """
    Truncate filename to fit Telegram limits.
    
    Args:
        path: file or directory path
    
    Returns:
        str: truncated path
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
# Get Total Size of Path
# =============================================================================
def getSize(path: str) -> int:
    """
    Get total size of file or directory.
    
    Args:
        path: file or directory path
    
    Returns:
        int: total size in bytes
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
# Video Extension Fix
# =============================================================================
def videoExtFix(file_path: str) -> str:
    """
    Fix video file extension for Telegram compatibility.
    
    Args:
        file_path: path to video file
    
    Returns:
        str: fixed file path
    """
    _, f_name = ospath.split(file_path)
    if f_name.endswith(".mp4") or f_name.endswith(".mkv"):
        return file_path
    
    new_path = file_path + ".mp4"
    os.rename(file_path, new_path)
    return new_path


# =============================================================================
# Thumbnail Generation
# =============================================================================
def thumbMaintainer(file_path: str):
    """
    Generate or retrieve thumbnail for video.
    
    Args:
        file_path: path to video file
    
    Returns:
        tuple: (thumbnail_path, duration)
    """
    if ospath.exists(Paths.VIDEO_FRAME):
        os.remove(Paths.VIDEO_FRAME)
    
    try:
        fname, _ = ospath.splitext(ospath.basename(file_path))
        ytdl_thmb = f"{Paths.WORK_PATH}/ytdl_thumbnails/{fname}.webp"
        
        with VideoFileClip(file_path) as video:
            # Use custom thumbnail if set
            if ospath.exists(Paths.THMB_PATH):
                return Paths.THMB_PATH, video.duration
            # Use YT-DLP thumbnail if available
            elif ospath.exists(ytdl_thmb):
                return convertIMG(ytdl_thmb), video.duration
            # Generate frame from video
            else:
                video.save_frame(Paths.VIDEO_FRAME, t=math.floor(video.duration / 2))
                return Paths.VIDEO_FRAME, video.duration
    
    except Exception as e:
        logger.error(f"Thumbnail generation error: {e}")
        if ospath.exists(Paths.THMB_PATH):
            return Paths.THMB_PATH, 0
        return Paths.HERO_IMAGE, 0


# =============================================================================
# Set Thumbnail
# =============================================================================
async def setThumbnail(message):
    """
    Save user sent image as thumbnail.
    
    Args:
        message: Telegram message with photo
    
    Returns:
        bool: success status
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
        logger.error(f"Thumbnail download error: {e}")
        return False


# =============================================================================
# YT-DLP Completion Check
# =============================================================================
def isYtdlComplete() -> bool:
    """
    Check if YT-DLP has finished downloading.
    
    Returns:
        bool: True if no .part or .ytdl files found
    """
    for _, _, filenames in os.walk(Paths.down_path):
        for f in filenames:
            _, ext = ospath.splitext(f)
            if ext in [".part", ".ytdl"]:
                return False
    return True


# =============================================================================
# Image Conversion
# =============================================================================
def convertIMG(image_path: str) -> str:
    """
    Convert image to JPEG format.
    
    Args:
        image_path: path to image file
    
    Returns:
        str: path to converted image
    """
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    output_path = ospath.splitext(image_path)[0] + ".jpg"
    image.save(output_path, "JPEG")
    os.remove(image_path)
    return output_path


# =============================================================================
# System Information (Basic)
# =============================================================================
def sysINFO() -> str:
    """
    Get system resource usage information.
    
    Returns:
        str: formatted system info string
    """
    ram_usage = psutil.Process(os.getpid()).memory_info().rss
    disk_usage = psutil.disk_usage("/")
    cpu_usage = psutil.cpu_percent(interval=0.1)
    
    info = f"""

⌬───── **{style_text('System Info')}** ─────⌬

┏🖥️ **{style_text('CPU')}:** `{cpu_usage}%`
┠💽 **{style_text('RAM')}:** `{sizeUnit(ram_usage)}`
┖💾 **{style_text('Disk')}:** `{sizeUnit(disk_usage.free)}`"""
    
    return info


# =============================================================================
# System Information (Detailed)
# =============================================================================
def sysINFO_full() -> str:
    """Get detailed system information."""
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    cpu_percent = psutil.cpu_percent(interval=0.5, percpu=True)
    net = psutil.net_io_counters()
    
    info = f"""

⌬───── **{style_text('System Info (Detailed)')}** ─────⌬

┏🖥️ **{style_text('CPU')}:** `{psutil.cpu_percent()}%` (cores: {', '.join(f'{c}%' for c in cpu_percent)})
┠💽 **{style_text('RAM')}:** `{sizeUnit(ram.used)} / {sizeUnit(ram.total)}` ({ram.percent}%)
┠💾 **{style_text('Disk')}:** `{sizeUnit(disk.used)} / {sizeUnit(disk.total)}` ({disk.percent}%)
┠🌐 **{style_text('Net')}:** ↓`{sizeUnit(net.bytes_recv)}` ↑`{sizeUnit(net.bytes_sent)}`
┗⏱️ **{style_text('Uptime')}:** `{getTime(int(time() - psutil.boot_time()))}`"""
    return info


# =============================================================================
# Multipart Archive Handling
# =============================================================================
def multipartArchive(path: str, archive_type: str, remove: bool):
    """
    Handle multipart archive files.
    
    Args:
        path: path to archive
        archive_type: type of archive (rar, 7z, zip)
        remove: whether to remove parts after processing
    
    Returns:
        tuple: (real_name, total_size)
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
# Time Check for UI Updates
# =============================================================================
def isTimeOver() -> bool:
    """
    Check if 3 seconds have passed since last update.
    
    Returns:
        bool: True if time exceeded
    """
    elapsed = time() - BotTimes.current_time
    if elapsed >= 3:
        BotTimes.current_time = time()
        return True
    return False


# =============================================================================
# Custom Name Application
# =============================================================================
def applyCustomName():
    """
    Apply custom name to downloaded files.
    """
    if BOT.Options.custom_name and BOT.Mode.type not in ["zip", "undzip"]:
        files = os.listdir(Paths.down_path)
        for file_ in files:
            current_name = ospath.join(Paths.down_path, file_)
            new_name = ospath.join(Paths.down_path, BOT.Options.custom_name)
            os.rename(current_name, new_name)


# =============================================================================
# Speed and ETA Calculation
# =============================================================================
def speedETA(start_time: datetime, done: int, total: int):
    """
    Calculate download speed and ETA.
    
    Args:
        start_time: download start time
        done: bytes completed
        total: total bytes
    
    Returns:
        tuple: (speed, eta, percentage)
    """
    percentage = (done / total) * 100 if total > 0 else 0
    percentage = min(percentage, 100)
    
    elapsed = (datetime.now() - start_time).seconds
    
    if done > 0 and elapsed > 0:
        raw_speed = done / elapsed
        speed = f"{sizeUnit(raw_speed)}/s"
        eta = (total - done) / raw_speed if raw_speed > 0 else 0
    else:
        speed, eta = "N/A", 0
    
    return speed, eta, percentage


# =============================================================================
# Message Deleter
# =============================================================================
async def message_deleter(msg1, msg2):
    """
    Safely delete two messages.
    
    Args:
        msg1: first message
        msg2: second message
    """
    try:
        await msg1.delete()
    except Exception as e:
        logger.error(f"Failed to delete msg1: {e}")
    
    try:
        await msg2.delete()
    except Exception as e:
        logger.error(f"Failed to delete msg2: {e}")


# =============================================================================
# Settings Menu
# =============================================================================
async def send_settings(client, message, msg_id: int, is_command: bool):
    """
    Send or edit settings menu.
    
    Args:
        client: pyrogram client
        message: Telegram message
        msg_id: message id to edit
        is_command: whether this is a new command
    """
    up_mode = "Document" if not BOT.Options.stream_upload else "Media"
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"📤 {style_button(up_mode)}",
                    callback_data="media" if up_mode == "Document" else "document"
                ),
                InlineKeyboardButton(
                    f"🎬 {style_button('Video')}",
                    callback_data="video"
                ),
            ],
            [
                InlineKeyboardButton(
                    f"📝 {style_button('Caption')}",
                    callback_data="caption"
                ),
                InlineKeyboardButton(
                    f"🖼️ {style_button('Thumb')}",
                    callback_data="thumb"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ Suffix", callback_data="set-suffix"
                ),
                InlineKeyboardButton(
                    "➕ Prefix", callback_data="set-prefix"
                ),
            ],
            [
                InlineKeyboardButton(
                    "Close", callback_data="close"
                )
            ],
        ]
    )
    
    pr = "✅" if BOT.Setting.prefix else "❎"
    su = "✅" if BOT.Setting.suffix else "❎"
    thmb = "✅" if BOT.Setting.thumbnail else "❎"
    
    text = style_text(f"""**⚙️ Bot Settings**

┏📤 **Upload:** `{BOT.Setting.stream_upload}`
┠✂️ **Split:** `{BOT.Setting.split_video}`
┠🔄 **Convert:** `{BOT.Setting.convert_video}`
┠📝 **Caption:** `{BOT.Setting.caption}`
┠➕ **Prefix:** {pr}
┠➕ **Suffix:** {su}
┗🖼️ **Thumb:** {thmb}""")
    
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
        logger.error(f"Settings menu error: {e}")
    except Exception as e:
        logger.error(f"Settings menu error: {e}")


# =============================================================================
# Status Bar Update
# =============================================================================
async def status_bar(down_msg: str, speed: str, percentage: float, eta: str, done: str, left: str, engine: str):
    """
    Update download/upload status bar.
    
    Args:
        down_msg: status header message
        speed: current speed
        percentage: completion percentage
        eta: estimated time
        done: bytes processed
        left: bytes remaining
        engine: download engine name
    """
    bar_length = 12
    filled = int(percentage / 100 * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    text = style_text(f"""
┏「{bar}」 **»** `{percentage:.1f}%`
┠⚡ **Speed:** `{speed}`
┠🔧 **Engine:** `{engine}`
┠⏳ **ETA:** `{eta}`
┠⏱️ **Elapsed:** `{getTime((datetime.now() - BotTimes.start_time).seconds)}`
┠✅ **Done:** `{done}`
┗📦 **Total:** `{left}`""")
    
    try:
        if isTimeOver():
            await MSG.status_msg.edit_text(
                text=Messages.task_msg + down_msg + text + sysINFO(),
                disable_web_page_preview=True,
                reply_markup=status_keyboard()
            )
    except BadRequest as e:
        logger.error(f"Status bar error: {e}")
    except Exception as e:
        logger.error(f"Status bar error: {e}")


# =============================================================================
# Cancel Keyboard (Legacy)
# =============================================================================
def keyboard():
    """
    Generate inline keyboard with cancel button.
    
    Returns:
        InlineKeyboardMarkup: cancel button
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(style_button("Cancel", "danger"), callback_data="cancel")
            ]
        ]
    )


# =============================================================================
# Status Keyboard with System Info Buttons
# =============================================================================
def status_keyboard():
    """
    Generate inline keyboard with Cancel, Refresh, and Stats buttons.
    
    Returns:
        InlineKeyboardMarkup: enhanced status keyboard
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    style_button("🔄 Refresh", "primary"), 
                    callback_data="sys_refresh"
                ),
                InlineKeyboardButton(
                    style_button("📊 Stats", "primary"), 
                    callback_data="sys_stats"
                ),
            ],
            [
                InlineKeyboardButton(
                    style_button("❌ Cancel", "danger"), 
                    callback_data="cancel"
                )
            ]
        ]
    )
