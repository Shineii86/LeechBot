# =============================================================================
# LeechBot Pro - Download Manager
# =============================================================================
# Project   : LeechBot Pro v3.0
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://t.me/Shineii86
# =============================================================================

import logging
from datetime import datetime
from asyncio import sleep

from colab_leecher.utility.handler import cancel_task
from colab_leecher.utility.helper import is_ytdl_complete, create_cancel_keyboard, get_system_info
from colab_leecher.utility.variables import BOT, Transfer, MSG, Messages, BotTimes

from .aria2 import aria2_download
from .ytdl import youtube_download
from .gdrive import build_service, google_download
from .telegram import telegram_download
from .mega import mega_download
from .terabox import terabox_download


# =============================================================================
# MAIN DOWNLOAD MANAGER
# =============================================================================
async def download_manager(sources: list, is_ytdl: bool):
    """
    Coordinate downloads from multiple sources.
    
    Args:
        sources: List of download URLs
        is_ytdl: Whether to use yt-dlp for all downloads
    """
    BotTimes.task_start = datetime.now()
    
    if is_ytdl:
        # YT-DLP mode for all links
        for i, link in enumerate(sources, 1):
            await youtube_download(link, i)
        
        # Wait for yt-dlp to complete
        await wait_for_ytdl_complete()
        
    else:
        # Auto-detect source type for each link
        for i, link in enumerate(sources, 1):
            try:
                await process_link(link, i)
            except Exception as e:
                logging.error(f"Download error for link {i}: {e}")
                await cancel_task(f"Download failed: {e}")
                return


# =============================================================================
# LINK PROCESSOR
# =============================================================================
async def process_link(link: str, index: int):
    """
    Process a single download link based on its type.
    
    Args:
        link: Download URL
        index: Download number
    """
    from colab_leecher.utility.helper import (
        is_google_drive, is_telegram, is_ytdl_link, 
        is_mega, is_terabox, is_torrent
    )
    
    # Show getting info message
    info_msg = f"<b>⏳ PLEASE WAIT</b>\n\n<i>Getting download info for:</i>\n<code>{link[:60]}...</code>"
    try:
        await MSG.status_msg.edit_text(
            text=info_msg + get_system_info(),
            reply_markup=create_cancel_keyboard(),
        )
    except Exception as e:
        logging.debug(f"Info message error: {e}")
    
    # Route to appropriate downloader
    if is_google_drive(link):
        await build_service()
        await google_download(link, index)
        
    elif is_telegram(link):
        await telegram_download(link, index)
        
    elif is_ytdl_link(link):
        await youtube_download(link, index)
        await wait_for_ytdl_complete()
        
    elif is_mega(link):
        await mega_download(link, index)
        
    elif is_terabox(link):
        await terabox_download(link, index)
        
    else:
        # Default to aria2c for direct links
        await aria2_download(link, index)


# =============================================================================
# YT-DLP WAITER
# =============================================================================
async def wait_for_ytdl_complete():
    """Wait for yt-dlp downloads to complete."""
    merge_msg = "<b>⏳ PLEASE WAIT</b>\n\n<i>Merging video and audio...</i> 🎬"
    
    try:
        await MSG.status_msg.edit_text(
            text=Messages.task_msg + Messages.status_head + merge_msg + get_system_info(),
            reply_markup=create_cancel_keyboard(),
        )
    except Exception as e:
        logging.debug(f"Merge message error: {e}")
    
    # Wait for .part files to disappear
    wait_count = 0
    max_wait = 300  # 5 minutes timeout
    
    while not is_ytdl_complete():
        await sleep(2)
        wait_count += 1
        
        if wait_count >= max_wait:
            logging.warning("YT-DLP merge wait timeout")
            break


# =============================================================================
# SIZE CALCULATOR
# =============================================================================
async def calculate_download_size(sources: list):
    """
    Calculate total download size from sources.
    
    Args:
        sources: List of download URLs
    """
    from colab_leecher.utility.helper import is_google_drive, is_telegram
    from .gdrive import build_service, get_file_metadata, get_folder_size, get_id_from_url
    from .telegram import get_media_info
    
    for link in sources:
        try:
            if is_google_drive(link):
                await build_service()
                file_id = await get_id_from_url(link)
                
                try:
                    meta = get_file_metadata(file_id)
                except Exception as e:
                    error_msg = ""
                    if "File not found" in str(e):
                        error_msg = "File not found or access denied"
                    elif "Failed to retrieve" in str(e):
                        error_msg = "Google Drive authorization failed"
                    else:
                        error_msg = f"Google Drive error: {e}"
                    
                    logging.error(error_msg)
                    await cancel_task(error_msg)
                    return
                
                if meta.get("mimeType") == "application/vnd.google-apps.folder":
                    Transfer.total_down_size += get_folder_size(file_id)
                else:
                    Transfer.total_down_size += int(meta.get("size", 0))
                    
            elif is_telegram(link):
                media, _ = await get_media_info(link)
                if media:
                    Transfer.total_down_size += media.file_size or 0
                else:
                    logging.error("Could not get Telegram media info")
                    
        except Exception as e:
            logging.error(f"Size calculation error: {e}")


# =============================================================================
# DOWNLOAD NAME GETTER
# =============================================================================
async def get_download_name(link: str) -> str:
    """
    Get the name of the file to be downloaded.
    
    Args:
        link: Download URL
        
    Returns:
        str: File name
    """
    from colab_leecher.utility.helper import (
        is_google_drive, is_telegram, is_ytdl_link, is_mega
    )
    from .gdrive import get_id_from_url, get_file_metadata
    from .telegram import get_media_info
    from .ytdl import get_youtube_name
    from .aria2 import get_aria2_name
    
    if BOT.Options.custom_name:
        return BOT.Options.custom_name
    
    try:
        if is_google_drive(link):
            file_id = await get_id_from_url(link)
            meta = get_file_metadata(file_id)
            return meta.get("name", "Unknown")
            
        elif is_telegram(link):
            media, _ = await get_media_info(link)
            return media.file_name if hasattr(media, "file_name") else "Unknown"
            
        elif is_ytdl_link(link):
            return await get_youtube_name(link)
            
        elif is_mega(link):
            return "Mega Download"
            
        else:
            return await get_aria2_name(link)
            
    except Exception as e:
        logging.error(f"Get name error: {e}")
        return "Unknown Download"
