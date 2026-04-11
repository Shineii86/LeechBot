# =============================================================================
# Telegram Leech Bot - YT-DLP Downloader
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
YT-DLP downloader module.

Handles downloads from YouTube and other sites supported by yt-dlp.
"""

import logging
import yt_dlp
from asyncio import sleep
from threading import Thread
from os import makedirs, path as ospath
from leechbot.utility.handler import cancelTask
from leechbot.utility.variables import YTDL, MSG, Messages, Paths, BOT
from leechbot.utility.helper import getTime, keyboard, sizeUnit, status_bar, sysINFO

logger = logging.getLogger(__name__)


# =============================================================================
# YT-DLP Status Monitor
# =============================================================================
async def YTDL_Status(link: str, num: int):
    """
    Monitor YT-DLP download progress.
    
    Args:
        link: video URL
        num: link number for display
    """
    global Messages, YTDL
    
    name = await get_YT_Name(link)
    Messages.status_head = f"**📥 Downloading** `Link {str(num).zfill(2)}`\n\n`{name}`\n"
    
    # Start YT-DLP in separate thread
    ytdl_thread = Thread(target=YouTubeDL, name="YT-DLP", args=(link,))
    ytdl_thread.start()
    
    # Monitor progress
    while ytdl_thread.is_alive():
        if YTDL.header:
            try:
                await MSG.status_msg.edit_text(
                    text=Messages.task_msg + Messages.status_head + YTDL.header + sysINFO(),
                    reply_markup=keyboard()
                )
            except Exception:
                pass
        else:
            try:
                await status_bar(
                    down_msg=Messages.status_head,
                    speed=YTDL.speed,
                    percentage=float(YTDL.percentage),
                    eta=YTDL.eta,
                    done=YTDL.done,
                    left=YTDL.left,
                    engine="YT-DLP 🏮"
                )
            except Exception:
                pass
        
        await sleep(2.5)


# =============================================================================
# YT-DLP Logger
# =============================================================================
class MyLogger:
    """Custom logger for YT-DLP"""
    
    def __init__(self):
        pass
    
    def debug(self, msg):
        global YTDL
        if "item" in str(msg):
            msgs = msg.split(" ")
            YTDL.header = f"\n⏳ `Getting Info {msgs[-3]} of {msgs[-1]}`"
    
    @staticmethod
    def warning(msg):
        pass
    
    @staticmethod
    def error(msg):
        pass


# =============================================================================
# YT-DLP Download Function
# =============================================================================
def YouTubeDL(url: str):
    """
    Download video using YT-DLP.
    
    Args:
        url: video URL
    """
    global YTDL
    
    def progress_hook(d):
        """Progress hook for YT-DLP"""
        global YTDL
        
        if d["status"] == "downloading":
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            dl_bytes = d.get("downloaded_bytes", 0)
            speed = d.get("speed", "N/A")
            eta = d.get("eta", 0)
            
            if total_bytes:
                percent = round((float(dl_bytes) * 100 / float(total_bytes)), 2)
            else:
                percent = 0
            
            YTDL.header = ""
            YTDL.speed = sizeUnit(speed) if speed else "N/A"
            YTDL.percentage = percent
            YTDL.eta = getTime(eta) if eta else "N/A"
            YTDL.done = sizeUnit(dl_bytes) if dl_bytes else "N/A"
            YTDL.left = sizeUnit(total_bytes) if total_bytes else "N/A"
    
    # YT-DLP options
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "writethumbnail": True,
        "concurrent_fragment_downloads": 5,
        "overwrites": True,
        "progress_hooks": [progress_hook],
        "writesubtitles": True,
        "subtitleslangs": ["en", "en-US", "en-GB"],
        "extractor_args": {"subtitlesformat": "srt"},
        "logger": MyLogger(),
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "outtmpl": {
            "default": f"{Paths.down_path}/%(title)s.%(ext)s",
            "thumbnail": f"{Paths.thumbnail_ytdl}/%(id)s.%(ext)s",
        }
    }
    
    # Create thumbnail directory
    if not ospath.exists(Paths.thumbnail_ytdl):
        makedirs(Paths.thumbnail_ytdl)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            YTDL.header = "⏳ `Preparing...`"
            
            if info.get("_type") == "playlist":
                # Playlist download
                playlist_name = info["title"]
                playlist_path = ospath.join(Paths.down_path, playlist_name)
                
                if not ospath.exists(playlist_path):
                    makedirs(playlist_path)
                
                ydl_opts["outtmpl"]["default"] = f"{playlist_path}/%(title)s.%(ext)s"
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
                    for entry in info["entries"]:
                        if entry:
                            try:
                                ydl2.download([entry["webpage_url"]])
                            except Exception as e:
                                logger.error(f"Playlist item error: {e}")
            else:
                # Single video download
                ydl.download([url])
        
        except Exception as e:
            logger.error(f"YT-DLP error: {e}")


# =============================================================================
# Get Video Name
# =============================================================================
async def get_YT_Name(link: str) -> str:
    """
    Get video title from link.
    
    Args:
        link: video URL
    
    Returns:
        str: video title
    """
    with yt_dlp.YoutubeDL({"logger": MyLogger()}) as ydl:
        try:
            info = ydl.extract_info(link, download=False)
            return info.get("title", "Unknown")
        except Exception as e:
            await cancelTask(f"Cannot Download: {e}")
            return "Unknown"
