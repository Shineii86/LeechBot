# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ᴛᴇʀᴀʙᴏx ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ᴍᴏᴅᴜʟᴇ

ᴛʜɪs ᴍᴏᴅᴜʟᴇ ʜᴀɴᴅʟᴇs ᴅᴏᴡɴʟᴏᴀᴅs ғʀᴏᴍ ᴛᴇʀᴀʙᴏx ᴜsɪɴɢ ᴛʜɪʀᴅ-ᴘᴀʀᴛʏ ᴀᴘɪs.
"""

import aiohttp
import logging
from leechbot.utility.variables import Aria2c
from leechbot.utility.handler import cancelTask
from leechbot.downloader.aria2 import aria2_Download

logger = logging.getLogger(__name__)


# =============================================================================
#  ᴍᴀɪɴ ᴅᴏᴡɴʟᴏᴀᴅ ғᴜɴᴄᴛɪᴏɴ
# =============================================================================
async def terabox_download(link: str, index: int):
    """
    ᴅᴏᴡɴʟᴏᴀᴅ ғɪʟᴇ ғʀᴏᴍ ᴛᴇʀᴀʙᴏx.
    
    ᴀʀɢs:
        ʟɪɴᴋ: ᴛᴇʀᴀʙᴏx sʜᴀʀᴇ ʟɪɴᴋ
        ɪɴᴅᴇx: ʟɪɴᴋ ɴᴜᴍʙᴇʀ
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
            # ɢᴇᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋs
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
                    logger.error(f"ᴛᴇʀᴀʙᴏx ᴀᴘɪ ᴇʀʀᴏʀ: {e}")
                    await cancelTask(f"ᴛᴇʀᴀʙᴏx ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛɪᴏɴ ғᴀɪʟᴇᴅ: {e}")
                    return
            
            # ᴛʀʏ ғᴀsᴛ ᴅᴏᴡɴʟᴏᴀᴅ ғɪʀsᴛ
            async with session.get(fast_url, allow_redirects=True) as response:
                content_type = response.headers.get("Content-Type", "")
                Aria2c.link_info = False
                
                if "application/octet-stream" in content_type or "video" in content_type:
                    await aria2_Download(fast_url, index)
                else:
                    logger.info("ғᴀsᴛ ʟɪɴᴋ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ, ᴜsɪɴɢ sʟᴏᴡ ʟɪɴᴋ")
                    await aria2_Download(slow_url, index)
    
    except Exception as e:
        logger.error(f"ᴛᴇʀᴀʙᴏx ᴅᴏᴡɴʟᴏᴀᴅ ᴇʀʀᴏʀ: {e}")
        await cancelTask(f"ᴛᴇʀᴀʙᴏx ᴅᴏᴡɴʟᴏᴀᴅ ғᴀɪʟᴇᴅ: {e}")
