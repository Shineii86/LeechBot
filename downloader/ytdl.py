# =============================================================================
# LeechBot Pro - YT-DLP Downloader
# =============================================================================
# Project   : LeechBot Pro v3.0
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://t.me/Shineii86
# =============================================================================

import logging
import yt_dlp
from asyncio import sleep
from threading import Thread
from os import makedirs, path as ospath

from colab_leecher.utility.handler import cancel_task
from colab_leecher.utility.variables import YTDL, MSG, Messages, Paths, BOT
from colab_leecher.utility.helper import (
    get_time_string, create_cancel_keyboard, format_size, 
    get_system_info, update_status_bar, is_ytdl_complete
)


# =============================================================================
# YT-DLP LOGGER
# =============================================================================
class YTLogger:
    """Custom logger for yt-dlp."""
    
    def debug(self, msg: str):
        """Handle debug messages."""
        if "item" in str(msg):
            try:
                parts = msg.split()
                YTDL.header = f"\n⏳ <i>Getting info: {parts[-3]} of {parts[-1]}</i>"
            except Exception:
                pass
    
    def warning(self, msg: str):
        """Handle warning messages."""
        pass
    
    def error(self, msg: str):
        """Handle error messages."""
        pass


# =============================================================================
# DOWNLOAD OPTIONS
# =============================================================================
def get_ydl_options() -> dict:
    """
    Get yt-dlp options based on current settings.
    
    Returns:
        dict: yt-dlp configuration
    """
    return {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": BOT.Options.video_out,
        "writethumbnail": True,
        "concurrent_fragment_downloads": 4,
        "overwrites": True,
        "writesubtitles": True,
        "subtitleslangs": ["en"],
        "extractor_args": {"subtitlesformat": "srt"},
        "logger": YTLogger(),
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "noplaylist": False,
        "progress_hooks": [progress_hook],
    }


def progress_hook(d: dict):
    """
    Progress hook for yt-dlp downloads.
    
    Args:
        d: Progress dictionary from yt-dlp
    """
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
        downloaded = d.get("downloaded_bytes", 0)
        speed = d.get("speed", 0)
        eta = d.get("eta", 0)
        
        if total:
            percent = round((downloaded / total) * 100, 2)
        else:
            percent = d.get("downloaded_percent", 0) or 0
        
        YTDL.header = ""
        YTDL.speed = format_size(speed) + "/s" if speed else "N/A"
        YTDL.percentage = percent
        YTDL.eta = get_time_string(eta) if eta else "N/A"
        YTDL.done = format_size(downloaded) if downloaded else "N/A"
        YTDL.left = format_size(total) if total else "N/A"
        
    elif d["status"] == "finished":
        YTDL.percentage = 100
        YTDL.eta = "0s"


# =============================================================================
# MAIN DOWNLOAD FUNCTION
# =============================================================================
async def youtube_download(link: str, num: int):
    """
    Download video using yt-dlp.
    
    Args:
        link: Video URL
        num: Download number for display
    """
    name = await get_youtube_name(link)
    Messages.status_head = f"<b>📥 DOWNLOADING</b> <code>Link {num:02d}</code>\n\n<code>{name}</code>\n"
    
    # Start download in thread
    download_thread = Thread(target=download_worker, args=(link,), name="YTDLWorker")
    download_thread.start()
    
    # Monitor progress
    while download_thread.is_alive():
        if YTDL.header:
            # Show info gathering message
            try:
                await MSG.status_msg.edit_text(
                    text=Messages.task_msg + Messages.status_head + YTDL.header + get_system_info(),
                    reply_markup=create_cancel_keyboard(),
                )
            except Exception:
                pass
        else:
            # Show download progress
            try:
                await update_status_bar(
                    down_msg=Messages.status_head,
                    speed=YTDL.speed,
                    percentage=float(YTDL.percentage),
                    eta=YTDL.eta,
                    done=YTDL.done,
                    left=YTDL.left,
                    engine="YT-DLP 🎬",
                )
            except Exception:
                pass
        
        await sleep(2.5)


def download_worker(url: str):
    """
    Worker thread for yt-dlp download.
    
    Args:
        url: Video URL
    """
    ydl_opts = get_ydl_options()
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Create thumbnail directory
        if not ospath.exists(Paths.thumbnail_ytdl):
            makedirs(Paths.thumbnail_ytdl)
        
        try:
            # Get info first
            info = ydl.extract_info(url, download=False)
            
            if info.get("_type") == "playlist":
                # Handle playlist
                playlist_name = info.get("title", "Playlist")
                playlist_dir = ospath.join(Paths.down_path, playlist_name)
                
                if not ospath.exists(playlist_dir):
                    makedirs(playlist_dir)
                
                ydl_opts["outtmpl"] = {
                    "default": f"{playlist_dir}/%(title)s.%(ext)s",
                    "thumbnail": f"{Paths.thumbnail_ytdl}/%(id)s.%(ext)s",
                }
                
                # Download each entry
                for entry in info.get("entries", []):
                    if entry:
                        video_url = entry.get("webpage_url") or entry.get("url")
                        if video_url:
                            try:
                                with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
                                    ydl2.download([video_url])
                            except yt_dlp.utils.DownloadError as e:
                                if "File name too long" in str(e):
                                    # Use ID-based naming
                                    ydl_opts["outtmpl"] = {
                                        "default": f"{playlist_dir}/%(id)s.%(ext)s",
                                        "thumbnail": f"{Paths.thumbnail_ytdl}/%(id)s.%(ext)s",
                                    }
                                    with yt_dlp.YoutubeDL(ydl_opts) as ydl3:
                                        ydl3.download([video_url])
            else:
                # Single video
                YTDL.header = ""
                ydl_opts["outtmpl"] = {
                    "default": f"{Paths.down_path}/%(id)s.%(ext)s",
                    "thumbnail": f"{Paths.thumbnail_ytdl}/%(id)s.%(ext)s",
                }
                
                try:
                    ydl.download([url])
                except yt_dlp.utils.DownloadError as e:
                    if "File name too long" in str(e):
                        ydl_opts["outtmpl"] = {
                            "default": f"{Paths.down_path}/%(id)s.%(ext)s",
                            "thumbnail": f"{Paths.thumbnail_ytdl}/%(id)s.%(ext)s",
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
                            ydl2.download([url])
                            
        except Exception as e:
            logging.error(f"YT-DLP error: {e}")


# =============================================================================
# GET VIDEO NAME
# =============================================================================
async def get_youtube_name(link: str) -> str:
    """
    Get video/playlist title without downloading.
    
    Args:
        link: YouTube URL
        
    Returns:
        str: Title or "Unknown"
    """
    try:
        with yt_dlp.YoutubeDL({"logger": YTLogger(), "quiet": True}) as ydl:
            info = ydl.extract_info(link, download=False)
            
            if info.get("_type") == "playlist":
                return f"{info.get('title', 'Playlist')} ({info.get('playlist_count', '?')} videos)"
            else:
                return info.get("title", "Unknown Video")
                
    except Exception as e:
        logging.error(f"Get YouTube name error: {e}")
        return "Unknown Download"
