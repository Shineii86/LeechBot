# =============================================================================
# Telegram Leech Bot - Terabox Downloader
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
Terabox downloader module.

Handles downloads from Terabox using third-party APIs.
"""

import aiohttp
import logging
from leechbot.utility.variables import Aria2c
from leechbot.utility.handler import cancelTask
from leechbot.downloader.aria2 import aria2_Download
from leechbot.utility.style import style_text

logger = logging.getLogger(__name__)


# =============================================================================
# Main Download Function
# =============================================================================
async def terabox_download(link: str, index: int):
    """
    Download file from Terabox.
    
    Args:
        link: Terabox share link
        index: link number
    """
    global Aria2c
    
    payload = {"url": link}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
    }
    
    fast_url = ""
    slow_url = ""
    
    try:
        async with aiohttp.ClientSession() as session:
            # Get download links
            async with session.post(
                "https://ytshorts.savetube.me/api/v1/terabox-downloader",
                data=payload,
                headers=headers
            ) as response:
                try:
                    response.raise_for_status()
                    json_response = await response.json()
                    fast_url = json_response["response"][0]["resolutions"]["Fast Download"]
                    slow_url = json_response["response"][0]["resolutions"]["HD Video"]
                except Exception as e:
                    logger.error(f"Terabox API error: {e}")
                    await cancelTask(style_text(f"Terabox Link Generation Failed: {e}"))
                    return
            
            # Try fast download first
            async with session.get(fast_url, allow_redirects=True) as response:
                content_type = response.headers.get("Content-Type", "")
                Aria2c.link_info = False
                
                if "application/octet-stream" in content_type or "video" in content_type:
                    await aria2_Download(fast_url, index)
                else:
                    logger.info("Fast link unavailable, using slow link")
                    await aria2_Download(slow_url, index)
    
    except Exception as e:
        logger.error(f"Terabox download error: {e}")
        await cancelTask(style_text(f"Terabox Download Failed: {e}"))
