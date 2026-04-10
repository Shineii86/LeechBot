# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ʏᴛ-ᴅʟᴘ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ᴍᴏᴅᴜʟᴇ

ᴛʜɪs ᴍᴏᴅᴜʟᴇ ʜᴀɴᴅʟᴇs ᴅᴏᴡɴʟᴏᴀᴅs ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ᴀɴᴅ ᴏᴛʜᴇʀ sɪᴛᴇs sᴜᴘᴘᴏʀᴛᴇᴅ ʙʏ ʏᴛ-ᴅʟᴘ.
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
#  ʏᴛ-ᴅʟᴘ sᴛᴀᴛᴜs ᴍᴏɴɪᴛᴏʀ
# =============================================================================
async def YTDL_Status(link: str, num: int):
    """
    ᴍᴏɴɪᴛᴏʀ ʏᴛ-ᴅʟᴘ ᴅᴏᴡɴʟᴏᴀᴅ ᴘʀᴏɢʀᴇss.
    
    ᴀʀɢs:
        ʟɪɴᴋ: ᴠɪᴅᴇᴏ ᴜʀʟ
        ɴᴜᴍ: ʟɪɴᴋ ɴᴜᴍʙᴇʀ ғᴏʀ ᴅɪsᴘʟᴀʏ
    """
    global Messages, YTDL
    
    name = await get_YT_Name(link)
    Messages.status_head = f"**📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ** `ʟɪɴᴋ {str(num).zfill(2)}`\n\n`{name}`\n"
    
    # sᴛᴀʀᴛ ʏᴛ-ᴅʟᴘ ɪɴ sᴇᴘᴀʀᴀᴛᴇ ᴛʜʀᴇᴀᴅ
    ytdl_thread = Thread(target=YouTubeDL, name="ʏᴛ-ᴅʟᴘ", args=(link,))
    ytdl_thread.start()
    
    # ᴍᴏɴɪᴛᴏʀ ᴘʀᴏɢʀᴇss
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
                    engine="ʏᴛ-ᴅʟᴘ 🏮"
                )
            except Exception:
                pass
        
        await sleep(2.5)


# =============================================================================
#  ʏᴛ-ᴅʟᴘ ʟᴏɢɢᴇʀ
# =============================================================================
class MyLogger:
    """ᴄᴜsᴛᴏᴍ ʟᴏɢɢᴇʀ ғᴏʀ ʏᴛ-ᴅʟᴘ"""
    
    def __init__(self):
        pass
    
    def debug(self, msg):
        global YTDL
        if "item" in str(msg):
            msgs = msg.split(" ")
            YTDL.header = f"\n⏳ `ɢᴇᴛᴛɪɴɢ ɪɴғᴏ {msgs[-3]} ᴏғ {msgs[-1]}`"
    
    @staticmethod
    def warning(msg):
        pass
    
    @staticmethod
    def error(msg):
        pass


# =============================================================================
#  ʏᴛ-ᴅʟᴘ ᴅᴏᴡɴʟᴏᴀᴅ ғᴜɴᴄᴛɪᴏɴ
# =============================================================================
def YouTubeDL(url: str):
    """
    ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ ᴜsɪɴɢ ʏᴛ-ᴅʟᴘ.
    
    ᴀʀɢs:
        ᴜʀʟ: ᴠɪᴅᴇᴏ ᴜʀʟ
    """
    global YTDL
    
    def progress_hook(d):
        """ᴘʀᴏɢʀᴇss ʜᴏᴏᴋ ғᴏʀ ʏᴛ-ᴅʟᴘ"""
        global YTDL
        
        if d["status"] == "downloading":
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            dl_bytes = d.get("downloaded_bytes", 0)
            speed = d.get("speed", "ɴ/ᴀ")
            eta = d.get("eta", 0)
            
            if total_bytes:
                percent = round((float(dl_bytes) * 100 / float(total_bytes)), 2)
            else:
                percent = 0
            
            YTDL.header = ""
            YTDL.speed = sizeUnit(speed) if speed else "ɴ/ᴀ"
            YTDL.percentage = percent
            YTDL.eta = getTime(eta) if eta else "ɴ/ᴀ"
            YTDL.done = sizeUnit(dl_bytes) if dl_bytes else "ɴ/ᴀ"
            YTDL.left = sizeUnit(total_bytes) if total_bytes else "ɴ/ᴀ"
    
    # ʏᴛ-ᴅʟᴘ ᴏᴘᴛɪᴏɴs
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
    
    # ᴄʀᴇᴀᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ ᴅɪʀᴇᴄᴛᴏʀʏ
    if not ospath.exists(Paths.thumbnail_ytdl):
        makedirs(Paths.thumbnail_ytdl)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            YTDL.header = "⏳ `ᴘʀᴇᴘᴀʀɪɴɢ...`"
            
            if info.get("_type") == "playlist":
                # ᴘʟᴀʏʟɪsᴛ ᴅᴏᴡɴʟᴏᴀᴅ
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
                                logger.error(f"ᴘʟᴀʏʟɪsᴛ ɪᴛᴇᴍ ᴇʀʀᴏʀ: {e}")
            else:
                # sɪɴɢʟᴇ ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅ
                ydl.download([url])
        
        except Exception as e:
            logger.error(f"ʏᴛ-ᴅʟᴘ ᴇʀʀᴏʀ: {e}")


# =============================================================================
#  ɢᴇᴛ ᴠɪᴅᴇᴏ ɴᴀᴍᴇ
# =============================================================================
async def get_YT_Name(link: str) -> str:
    """
    ɢᴇᴛ ᴠɪᴅᴇᴏ ᴛɪᴛʟᴇ ғʀᴏᴍ ʟɪɴᴋ.
    
    ᴀʀɢs:
        ʟɪɴᴋ: ᴠɪᴅᴇᴏ ᴜʀʟ
    
    ʀᴇᴛᴜʀɴs:
        sᴛʀ: ᴠɪᴅᴇᴏ ᴛɪᴛʟᴇ
    """
    with yt_dlp.YoutubeDL({"logger": MyLogger()}) as ydl:
        try:
            info = ydl.extract_info(link, download=False)
            return info.get("title", "ᴜɴᴋɴᴏᴡɴ")
        except Exception as e:
            await cancelTask(f"ᴄᴀɴɴᴏᴛ ᴅᴏᴡɴʟᴏᴀᴅ: {e}")
            return "ᴜɴᴋɴᴏᴡɴ"
