# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ᴅᴏᴡɴʟᴏᴀᴅ ᴍᴀɴᴀɢᴇʀ ᴍᴏᴅᴜʟᴇ

ᴛʜɪs ᴍᴏᴅᴜʟᴇ ᴏʀᴄʜᴇsᴛʀᴀᴛᴇs ᴅᴏᴡɴʟᴏᴀᴅs ғʀᴏᴍ ᴠᴀʀɪᴏᴜs sᴏᴜʀᴄᴇs ᴀɴᴅ ᴍᴀɴᴀɢᴇs
ᴛʜᴇ ᴏᴠᴇʀᴀʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ᴘʀᴏᴄᴇss.
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

logger = logging.getLogger(__name__)


# =============================================================================
#  ᴍᴀɪɴ ᴅᴏᴡɴʟᴏᴀᴅ ᴍᴀɴᴀɢᴇʀ
# =============================================================================
async def downloadManager(sources: list, is_ytdl: bool):
    """
    ᴍᴀɴᴀɢᴇ ᴅᴏᴡɴʟᴏᴀᴅs ғʀᴏᴍ ᴍᴜʟᴛɪᴘʟᴇ sᴏᴜʀᴄᴇs.
    
    ᴀʀɢs:
        sᴏᴜʀᴄᴇs: ʟɪsᴛ ᴏғ ᴜʀʟs ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ
        ɪs_ʏᴛᴅʟ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ᴜsᴇ ʏᴛ-ᴅʟᴘ
    """
    message = "\n**⏳ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n`ᴍᴇʀɢɪɴɢ ʏᴛ-ᴅʟᴘ ᴠɪᴅᴇᴏ...`"
    BotTimes.task_start = datetime.now()
    
    if is_ytdl:
        # ʏᴛ-ᴅʟᴘ ᴍᴏᴅᴇ
        for i, link in enumerate(sources):
            await YTDL_Status(link, i + 1)
        
        try:
            await MSG.status_msg.edit_text(
                text=Messages.task_msg + Messages.status_head + message + sysINFO(),
                reply_markup=keyboard()
            )
        except Exception as e:
            logger.error(f"ʏᴛᴅʟ ᴍᴇssᴀɢᴇ ᴇʀʀᴏʀ: {e}")
        
        while not isYtdlComplete():
            await sleep(2)
    
    else:
        # ɢᴇɴᴇʀᴀʟ ᴅᴏᴡɴʟᴏᴀᴅ ᴍᴏᴅᴇ
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
                        logger.error(f"ʏᴛᴅʟ ᴍᴇssᴀɢᴇ ᴇʀʀᴏʀ: {e}")
                    while not isYtdlComplete():
                        await sleep(2)
                elif "mega.nz" in link:
                    await megadl(link, i + 1)
                elif "terabox" in link or "1024tera" in link:
                    from leechbot.downloader.terabox import terabox_download
                    await terabox_download(link, i + 1)
                else:
                    # ɢᴇɴᴇʀᴀʟ ʜᴛᴛᴘ/ᴛᴏʀʀᴇɴᴛ
                    aria_msg = f"**⏳ ɢᴇᴛᴛɪɴɢ ɪɴғᴏ...**\n\n`{link}`"
                    try:
                        await MSG.status_msg.edit_text(
                            text=aria_msg + sysINFO(),
                            reply_markup=keyboard()
                        )
                    except Exception as e:
                        logger.error(f"ᴀʀɪᴀ2 ᴍᴇssᴀɢᴇ ᴇʀʀᴏʀ: {e}")
                    
                    Aria2c.link_info = False
                    await aria2_Download(link, i + 1)
            
            except Exception as error:
                await cancelTask(f"ᴅᴏᴡɴʟᴏᴀᴅ ᴇʀʀᴏʀ: {error}")
                logger.error(f"ᴅᴏᴡɴʟᴏᴀᴅ ᴇʀʀᴏʀ: {error}")
                return


# =============================================================================
#  ᴄᴀʟᴄᴜʟᴀᴛᴇ ᴛᴏᴛᴀʟ ᴅᴏᴡɴʟᴏᴀᴅ sɪᴢᴇ
# =============================================================================
async def calDownSize(sources: list):
    """
    ᴄᴀʟᴄᴜʟᴀᴛᴇ ᴛᴏᴛᴀʟ ᴅᴏᴡɴʟᴏᴀᴅ sɪᴢᴇ ғʀᴏᴍ sᴏᴜʀᴄᴇs.
    
    ᴀʀɢs:
        sᴏᴜʀᴄᴇs: ʟɪsᴛ ᴏғ ᴜʀʟs
    """
    for link in natsorted(sources):
        if "drive.google.com" in link:
            await build_service()
            file_id = await getIDFromURL(link)
            try:
                meta = getFileMetadata(file_id)
            except Exception as e:
                if "ғɪʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ" in str(e):
                    err_msg = "ғɪʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ ᴏʀ ɴᴏ ᴀᴄᴄᴇss"
                elif "ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ" in str(e):
                    err_msg = "ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ ғᴀɪʟᴇᴅ"
                else:
                    err_msg = f"ɢᴅʀɪᴠᴇ ᴇʀʀᴏʀ: {e}"
                logger.error(err_msg)
                await cancelTask(err_msg)
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
                logger.error("ᴄᴏᴜʟᴅ ɴᴏᴛ ɢᴇᴛ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ sɪᴢᴇ")


# =============================================================================
#  ɢᴇᴛ ᴅᴏᴡɴʟᴏᴀᴅ ɴᴀᴍᴇ
# =============================================================================
async def get_d_name(link: str):
    """
    ɢᴇᴛ ᴅᴏᴡɴʟᴏᴀᴅ ɴᴀᴍᴇ ғʀᴏᴍ ʟɪɴᴋ.
    
    ᴀʀɢs:
        ʟɪɴᴋ: sᴏᴜʀᴄᴇ ᴜʀʟ
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
        Messages.download_name = media.file_name if hasattr(media, "file_name") else "ᴜɴᴋɴᴏᴡɴ"
    elif "youtube.com" in link or "youtu.be" in link:
        Messages.download_name = await get_YT_Name(link)
    elif "mega.nz" in link:
        Messages.download_name = "ᴍᴇɢᴀ ᴅᴏᴡɴʟᴏᴀᴅ"
    else:
        Messages.download_name = get_Aria2c_Name(link)
