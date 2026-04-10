# =============================================================================
# LeechBot Pro - Terabox Downloader
# =============================================================================
# Project   : LeechBot Pro v3.0
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://t.me/Shineii86
# =============================================================================

import aiohttp
import logging
from colab_leecher.utility.variables import Aria2c
from colab_leecher.utility.handler import cancel_task
from .aria2 import aria2_download


# =============================================================================
# TERABOX DOWNLOAD
# =============================================================================
async def terabox_download(link: str, index: int):
    """
    Download file from Terabox.
    
    Uses external API to get direct download link,
    then passes to aria2c for actual download.
    
    Args:
        link: Terabox share URL
        index: Download number
    """
    # API endpoints to try
    api_endpoints = [
        "https://ytshorts.savetube.me/api/v1/terabox-downloader",
        "https://terabox-downloader-api.vercel.app/api/download",
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }
    
    download_url = None
    
    # Try each API endpoint
    for api_url in api_endpoints:
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"url": link}
                
                async with session.post(
                    api_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status != 200:
                        continue
                    
                    data = await response.json()
                    
                    # Parse response based on API format
                    if "response" in data and data["response"]:
                        resolutions = data["response"][0].get("resolutions", {})
                        download_url = resolutions.get("Fast Download") or resolutions.get("HD Video")
                        if download_url:
                            break
                    elif "downloadUrl" in data:
                        download_url = data["downloadUrl"]
                        break
                        
        except Exception as e:
            logging.debug(f"Terabox API {api_url} failed: {e}")
            continue
    
    if not download_url:
        await cancel_task("Failed to get Terabox download link. The file may be restricted or the API is down.")
        return
    
    # Download using aria2c
    try:
        Aria2c.link_info = False
        await aria2_download(download_url, index)
    except Exception as e:
        logging.error(f"Terabox download error: {e}")
        await cancel_task(f"Terabox download failed: {e}")
