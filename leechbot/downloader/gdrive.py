# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ᴍᴏᴅᴜʟᴇ

ᴛʜɪs ᴍᴏᴅᴜʟᴇ ʜᴀɴᴅʟᴇs ᴅᴏᴡɴʟᴏᴀᴅs ғʀᴏᴍ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ, ɪɴᴄʟᴜᴅɪɴɢ
ғɪʟᴇs, ғᴏʟᴅᴇʀs, ᴀɴᴅ sʜᴀʀᴇᴅ ᴅʀɪᴠᴇs. ɪᴛ ᴜsᴇs ᴛʜᴇ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ ᴀᴘɪ.
"""

import io
import logging
import pickle
from natsort import natsorted
from re import search as re_search
from os import makedirs, path as ospath
from urllib.parse import parse_qs, urlparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from leechbot.utility.handler import cancelTask
from leechbot.utility.helper import sizeUnit, getTime, speedETA, status_bar
from leechbot.utility.variables import Gdrive, Messages, Paths, BotTimes, Transfer

logger = logging.getLogger(__name__)


# =============================================================================
#  sᴇʀᴠɪᴄᴇ ʙᴜɪʟᴅᴇʀ
# =============================================================================
async def build_service():
    """
    ʙᴜɪʟᴅ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ ᴀᴘɪ sᴇʀᴠɪᴄᴇ ғʀᴏᴍ ᴛᴏᴋᴇɴ.
    """
    global Gdrive
    
    if ospath.exists(Paths.access_token):
        with open(Paths.access_token, "rb") as token:
            creds = pickle.load(token)
            Gdrive.service = build("drive", "v3", credentials=creds)
    else:
        await cancelTask("ᴛᴏᴋᴇɴ.ᴘɪᴄᴋʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ! ᴘʟᴇᴀsᴇ ʀᴜɴ ᴛʜᴇ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ sᴇᴛᴜᴘ ғɪʀsᴛ.")


# =============================================================================
#  ᴍᴀɪɴ ᴅᴏᴡɴʟᴏᴀᴅ ғᴜɴᴄᴛɪᴏɴ
# =============================================================================
async def g_DownLoad(link: str, num: int):
    """
    ᴅᴏᴡɴʟᴏᴀᴅ ғɪʟᴇ ᴏʀ ғᴏʟᴅᴇʀ ғʀᴏᴍ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ.
    
    ᴀʀɢs:
        ʟɪɴᴋ: ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ sʜᴀʀᴇ ʟɪɴᴋ
        ɴᴜᴍ: ʟɪɴᴋ ɴᴜᴍʙᴇʀ ғᴏʀ ᴅɪsᴘʟᴀʏ
    """
    global down_msg
    
    down_msg = f"**📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ** `ʟɪɴᴋ {str(num).zfill(2)}`\n\n**🏷️ ɴᴀᴍᴇ:** `{Messages.download_name}`\n"
    file_id = await getIDFromURL(link)
    meta = getFileMetadata(file_id)
    
    if meta.get("mimeType") == "application/vnd.google-apps.folder":
        await gDownloadFolder(file_id, Paths.down_path)
    else:
        await gDownloadFile(file_id, Paths.down_path)


# =============================================================================
#  ᴇxᴛʀᴀᴄᴛ ғɪʟᴇ ɪᴅ
# =============================================================================
async def getIDFromURL(link: str) -> str:
    """
    ᴇxᴛʀᴀᴄᴛ ғɪʟᴇ ɪᴅ ғʀᴏᴍ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ ʟɪɴᴋ.
    
    ᴀʀɢs:
        ʟɪɴᴋ: ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ sʜᴀʀᴇ ʟɪɴᴋ
    
    ʀᴇᴛᴜʀɴs:
        sᴛʀ: ғɪʟᴇ/ғᴏʟᴅᴇʀ ɪᴅ
    """
    if "folders" in link or "file" in link:
        regex = r"https:\/\/drive\.google\.com\/(?:drive(.*?)\/folders\/|file(.*?)?\/d\/)([-\w]+)"
        res = re_search(regex, link)
        if res is None:
            await cancelTask("ɪɴᴠᴀʟɪᴅ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ ʟɪɴᴋ")
            logger.error("ɢ-ᴅʀɪᴠᴇ ɪᴅ ɴᴏᴛ ғᴏᴜɴᴅ")
            return ""
        return res.group(3)
    
    parsed = urlparse(link)
    return parse_qs(parsed.query)["id"][0]


# =============================================================================
#  ɢᴇᴛ ғɪʟᴇs ɪɴ ғᴏʟᴅᴇʀ
# =============================================================================
def getFilesByFolderID(folder_id: str):
    """
    ɢᴇᴛ ᴀʟʟ ғɪʟᴇs ɪɴ ᴀ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ ғᴏʟᴅᴇʀ.
    
    ᴀʀɢs:
        ғᴏʟᴅᴇʀ_ɪᴅ: ғᴏʟᴅᴇʀ ɪᴅ
    
    ʀᴇᴛᴜʀɴs:
        ʟɪsᴛ: ʟɪsᴛ ᴏғ ғɪʟᴇ ᴏʙᴊᴇᴄᴛs
    """
    page_token = None
    files = []
    
    while True:
        response = (
            Gdrive.service.files()
            .list(
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                q=f"'{folder_id}' in parents and trashed = false",
                spaces="drive",
                pageSize=200,
                fields="nextPageToken, files(id, name, mimeType, size, shortcutDetails)",
                orderBy="folder, name",
                pageToken=page_token,
            )
            .execute()
        )
        files.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        if page_token is None:
            break
    
    return files


# =============================================================================
#  ɢᴇᴛ ғɪʟᴇ ᴍᴇᴛᴀᴅᴀᴛᴀ
# =============================================================================
def getFileMetadata(file_id: str):
    """
    ɢᴇᴛ ᴍᴇᴛᴀᴅᴀᴛᴀ ғᴏʀ ᴀ ғɪʟᴇ.
    
    ᴀʀɢs:
        ғɪʟᴇ_ɪᴅ: ғɪʟᴇ ɪᴅ
    
    ʀᴇᴛᴜʀɴs:
        ᴅɪᴄᴛ: ғɪʟᴇ ᴍᴇᴛᴀᴅᴀᴛᴀ
    """
    return (
        Gdrive.service.files()
        .get(fileId=file_id, supportsAllDrives=True, fields="name, id, mimeType, size")
        .execute()
    )


# =============================================================================
#  ɢᴇᴛ ғᴏʟᴅᴇʀ sɪᴢᴇ
# =============================================================================
def get_Gfolder_size(folder_id: str) -> int:
    """
    ᴄᴀʟᴄᴜʟᴀᴛᴇ ᴛᴏᴛᴀʟ sɪᴢᴇ ᴏғ ᴀ ғᴏʟᴅᴇʀ ʀᴇᴄᴜʀsɪᴠᴇʟʏ.
    
    ᴀʀɢs:
        ғᴏʟᴅᴇʀ_ɪᴅ: ғᴏʟᴅᴇʀ ɪᴅ
    
    ʀᴇᴛᴜʀɴs:
        ɪɴᴛ: ᴛᴏᴛᴀʟ sɪᴢᴇ ɪɴ ʙʏᴛᴇs
    """
    try:
        query = f"trashed = false and '{folder_id}' in parents"
        results = (
            Gdrive.service.files()
            .list(
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                q=query,
                fields="files(id, mimeType, size)",
            )
            .execute()
        )
        
        total_size = 0
        items = results.get("files", [])
        
        folders = [
            item["id"] for item in items
            if item.get("size") is None and item["mimeType"] == "application/vnd.google-apps.folder"
        ]
        
        for item in items:
            if "size" in item:
                total_size += int(item["size"])
        
        for fid in folders:
            total_size += get_Gfolder_size(fid)
        
        return total_size
    
    except HttpError as error:
        logger.error(f"ғᴏʟᴅᴇʀ sɪᴢᴇ ᴇʀʀᴏʀ: {error}")
        return -1


# =============================================================================
#  ᴅᴏᴡɴʟᴏᴀᴅ sɪɴɢʟᴇ ғɪʟᴇ
# =============================================================================
async def gDownloadFile(file_id: str, path: str):
    """
    ᴅᴏᴡɴʟᴏᴀᴅ ᴀ sɪɴɢʟᴇ ғɪʟᴇ ғʀᴏᴍ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ.
    
    ᴀʀɢs:
        ғɪʟᴇ_ɪᴅ: ғɪʟᴇ ɪᴅ
        ᴘᴀᴛʜ: ᴅᴏᴡɴʟᴏᴀᴅ ᴘᴀᴛʜ
    """
    try:
        file = getFileMetadata(file_id)
    except HttpError as error:
        err = "ғɪʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ ᴏʀ ɴᴏᴛ ᴀᴄᴄᴇssɪʙʟᴇ"
        logger.error(err)
        await cancelTask(err)
        return
    
    if file["mimeType"].startswith("application/vnd.google-apps"):
        err = "ɢᴏᴏɢʟᴇ ᴅᴏᴄs/sʜᴇᴇᴛs/sʟɪᴅᴇs ᴄᴀɴɴᴏᴛ ʙᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ᴅɪʀᴇᴄᴛʟʏ"
        logger.error(err)
        await cancelTask(err)
        return
    
    try:
        file_name = file.get("name", f"ᴜɴᴛɪᴛʟᴇᴅ_{file_id}")
        file_path = ospath.join(path, file_name)
        file_contents = io.BytesIO()
        
        request = Gdrive.service.files().get_media(
            fileId=file_id, supportsAllDrives=True
        )
        
        file_downloader = MediaIoBaseDownload(
            file_contents, request, chunksize=70 * 1024 * 1024
        )
        
        done = False
        while not done:
            status, done = file_downloader.next_chunk()
            file_contents.seek(0)
            
            with open(file_path, "ab") as f:
                f.write(file_contents.getvalue())
            
            file_contents.seek(0)
            file_contents.truncate()
            
            file_d_size = int(status.progress() * int(file["size"]))
            down_done = sum(Transfer.down_bytes) + file_d_size
            
            speed_string, eta, percentage = speedETA(
                BotTimes.task_start, down_done, Transfer.total_down_size
            )
            
            await status_bar(
                down_msg=down_msg,
                speed=speed_string,
                percentage=percentage,
                eta=getTime(eta),
                done=sizeUnit(down_done),
                left=sizeUnit(Transfer.total_down_size),
                engine="ɢᴅʀɪᴠᴇ ♻️"
            )
        
        Transfer.down_bytes.append(int(file["size"]))
    
    except HttpError as error:
        if error.resp.status == 403 and "ᴜsᴇʀ ʀᴀᴛᴇ ʟɪᴍɪᴛ" in str(error):
            logger.error("ᴅᴏᴡɴʟᴏᴀᴅ ǫᴜᴏᴛᴀ ᴇxᴄᴇᴇᴅᴇᴅ")
            await cancelTask("ᴅᴏᴡɴʟᴏᴀᴅ ǫᴜᴏᴛᴀ ᴇxᴄᴇᴇᴅᴇᴅ")
        else:
            logger.error(f"ɢᴅʀɪᴠᴇ ᴇʀʀᴏʀ: {error}")
            await cancelTask(f"ɢᴅʀɪᴠᴇ ᴇʀʀᴏʀ: {error}")
    
    except Exception as e:
        logger.error(f"ᴅᴏᴡɴʟᴏᴀᴅ ᴇʀʀᴏʀ: {e}")
        await cancelTask(f"ᴅᴏᴡɴʟᴏᴀᴅ ᴇʀʀᴏʀ: {e}")


# =============================================================================
#  ᴅᴏᴡɴʟᴏᴀᴅ ғᴏʟᴅᴇʀ
# =============================================================================
async def gDownloadFolder(folder_id: str, path: str):
    """
    ᴅᴏᴡɴʟᴏᴀᴅ ᴀ ғᴏʟᴅᴇʀ ʀᴇᴄᴜʀsɪᴠᴇʟʏ ғʀᴏᴍ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ.
    
    ᴀʀɢs:
        ғᴏʟᴅᴇʀ_ɪᴅ: ғᴏʟᴅᴇʀ ɪᴅ
        ᴘᴀᴛʜ: ᴅᴏᴡɴʟᴏᴀᴅ ᴘᴀᴛʜ
    """
    folder_meta = getFileMetadata(folder_id)
    folder_name = folder_meta["name"]
    
    if not ospath.exists(f"{path}/{folder_name}"):
        makedirs(f"{path}/{folder_name}")
    
    path += f"/{folder_name}"
    result = getFilesByFolderID(folder_id)
    
    if not result:
        return
    
    result = natsorted(result, key=lambda k: k["name"])
    
    for item in result:
        file_id = item["id"]
        shortcut = item.get("shortcutDetails")
        
        if shortcut:
            file_id = shortcut["targetId"]
            mime_type = shortcut["targetMimeType"]
        else:
            mime_type = item.get("mimeType")
        
        if mime_type == "application/vnd.google-apps.folder":
            await gDownloadFolder(file_id, path)
        else:
            await gDownloadFile(file_id, path)
