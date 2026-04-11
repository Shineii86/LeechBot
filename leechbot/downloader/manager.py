# =============================================================================
# Telegram Leech Bot - Download Manager
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
Download manager module.

Orchestrates downloads from various sources and manages the overall process.
"""

import logging
from natsort import natsorted
from datetime import datetime
from asyncio import sleep
from leechbot.downloader.mega import megadl
from leechbot.downloader.ytdl import YTDL_Status, get_YT_Name
from leechbot.downloader.aria2 import aria2_Download, get_Aria2c_Name, Aria2c
from leechbot.utility.helper import isYtdlComplete, keyboard, sysINFO
from leechbot.downloader.telegram import TelegramDownload, media_Identifier
from leechbot.utility.variables import BOT, Transfer, MSG, Messages, BotTimes
from leechbot.downloader.gdrive import build_service, g_DownLoad, get_Gfolder_size, getFileMetadata, getIDFromURL
from leechbot.utility.style import style_text

logger = logging.getLogger(__name__)


# =============================================================================
# Main Download Manager
# =============================================================================
async def downloadManager(sources: list, is_ytdl: bool):
    """
    Manage downloads from multiple sources.
    
    Args:
        sources: list of URLs to download
        is_ytdl: whether to use YT-DLP
    """
    message = style_text("\n**⏳ Please Wait...**\n`Merging YT-DLP Video...`")
    BotTimes.task_start = datetime.now()
    
    if is_ytdl:
        # YT-DLP mode
        for i, link in enumerate(sources):
            await YTDL_Status(link, i + 1)
        
        try:
            await MSG.status_msg.edit_text(
                text=Messages.task_msg + Messages.status_head + message + sysINFO(),
                reply_markup=keyboard()
            )
        except Exception as e:
            logger.error(f"YTDL message error: {e}")
        
        while not isYtdlComplete():
            await sleep(2)
    
    else:
        # General download mode
        for i, link in enumerate(sources):
            try:
                if "drive.google.com" in link:
                    await g_DownLoad(link, i + 1)
                elif "t.me" in link:
                    await TelegramDownload(link, i + 1)
                elif "youtube.com" in link or "youtu.be" in link:
                    await YTDL_Status(link, i + 1)
                    try:
                        await MSG.status_msg.edit_text(
                            text=Messages.task_msg + Messages.status_head + message + sysINFO(),
                            reply_markup=keyboard()
                        )
                    except Exception as e:
                        logger.error(f"YTDL message error: {e}")
                    while not isYtdlComplete():
                        await sleep(2)
                elif "mega.nz" in link:
                    await megadl(link, i + 1)
                elif "terabox" in link or "1024tera" in link:
                    from leechbot.downloader.terabox import terabox_download
                    await terabox_download(link, i + 1)
                else:
                    # General HTTP/torrent
                    aria_msg = style_text(f"**⏳ Getting Info...**\n\n`{link}`")
                    try:
                        await MSG.status_msg.edit_text(
                            text=aria_msg + sysINFO(),
                            reply_markup=keyboard()
                        )
                    except Exception as e:
                        logger.error(f"Aria2 message error: {e}")
                    
                    Aria2c.link_info = False
                    await aria2_Download(link, i + 1)
            
            except Exception as error:
                await cancelTask(style_text(f"Download Error: {error}"))
                logger.error(f"Download error: {error}")
                return


# =============================================================================
# Calculate Total Download Size
# =============================================================================
async def calDownSize(sources: list):
    """
    Calculate total download size from sources.
    
    Args:
        sources: list of URLs
    """
    for link in natsorted(sources):
        if "drive.google.com" in link:
            await build_service()
            file_id = await getIDFromURL(link)
            try:
                meta = getFileMetadata(file_id)
            except Exception as e:
                if "File not found" in str(e):
                    err_msg = "File not found or no access"
                elif "authorization" in str(e):
                    err_msg = "Google Drive authorization failed"
                else:
                    err_msg = f"GDrive error: {e}"
                logger.error(err_msg)
                await cancelTask(style_text(err_msg))
            else:
                if meta.get("mimeType") == "application/vnd.google-apps.folder":
                    Transfer.total_down_size += get_Gfolder_size(file_id)
                else:
                    Transfer.total_down_size += int(meta["size"])
        
        elif "t.me" in link:
            media, _ = await media_Identifier(link)
            if media and hasattr(media, "file_size"):
                Transfer.total_down_size += media.file_size
            else:
                logger.error("Could not get Telegram file size")


# =============================================================================
# Get Download Name
# =============================================================================
async def get_d_name(link: str):
    """
    Get download name from link.
    
    Args:
        link: source URL
    """
    if BOT.Options.custom_name:
        Messages.download_name = BOT.Options.custom_name
        return
    
    if "drive.google.com" in link:
        file_id = await getIDFromURL(link)
        meta = getFileMetadata(file_id)
        Messages.download_name = meta["name"]
    elif "t.me" in link:
        media, _ = await media_Identifier(link)
        Messages.download_name = media.file_name if hasattr(media, "file_name") else "Unknown"
    elif "youtube.com" in link or "youtu.be" in link:
        Messages.download_name = await get_YT_Name(link)
    elif "mega.nz" in link:
        Messages.download_name = "Mega Download"
    else:
        Messages.download_name = get_Aria2c_Name(link)
