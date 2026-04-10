# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ʟᴇᴇᴄʜʙᴏᴛ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ᴍᴏᴅᴜʟᴇs

ᴛʜɪs ᴘᴀᴄᴋᴀɢᴇ ᴄᴏɴᴛᴀɪɴs ᴀʟʟ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ɪᴍᴘʟᴇᴍᴇɴᴛᴀᴛɪᴏɴs ғᴏʀ ᴠᴀʀɪᴏᴜs sᴏᴜʀᴄᴇs.
"""

from .aria2 import aria2_Download, get_Aria2c_Name, Aria2c
from .gdrive import build_service, g_DownLoad, get_Gfolder_size, getFileMetadata, getIDFromURL
from .mega import megadl
from .telegram import TelegramDownload, media_Identifier
from .ytdl import YTDL_Status, get_YT_Name
from .terabox import terabox_download
from .manager import downloadManager, calDownSize, get_d_name

__all__ = [
    "aria2_Download",
    "get_Aria2c_Name",
    "Aria2c",
    "build_service",
    "g_DownLoad",
    "get_Gfolder_size",
    "getFileMetadata",
    "getIDFromURL",
    "megadl",
    "TelegramDownload",
    "media_Identifier",
    "YTDL_Status",
    "get_YT_Name",
    "terabox_download",
    "downloadManager",
    "calDownSize",
    "get_d_name",
]
