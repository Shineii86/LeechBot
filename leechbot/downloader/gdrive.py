# =============================================================================
# Telegram Leech Bot - Google Drive Downloader
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
Google Drive downloader module.

Handles downloads from Google Drive, including files, folders, and shared drives.
Uses the Google Drive API.
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
from leechbot.utility.style import style_text

logger = logging.getLogger(__name__)


# =============================================================================
# Service Builder
# =============================================================================
async def build_service():
    """
    Build Google Drive API service from token.
    """
    global Gdrive
    
    if ospath.exists(Paths.access_token):
        with open(Paths.access_token, "rb") as token:
            creds = pickle.load(token)
            Gdrive.service = build("drive", "v3", credentials=creds)
    else:
        await cancelTask(style_text("Token.pickle Not Found! Please Run The Google Drive Setup First."))


# =============================================================================
# Main Download Function
# =============================================================================
async def g_DownLoad(link: str, num: int):
    """
    Download file or folder from Google Drive.
    
    Args:
        link: Google Drive share link
        num: link number for display
    """
    global down_msg
    
    down_msg = style_text(f"**📥 Downloading** `Link {str(num).zfill(2)}`\n\n**🏷️ Name:** ") + f"`{Messages.download_name}`\n"
    file_id = await getIDFromURL(link)
    meta = getFileMetadata(file_id)
    
    if meta.get("mimeType") == "application/vnd.google-apps.folder":
        await gDownloadFolder(file_id, Paths.down_path)
    else:
        await gDownloadFile(file_id, Paths.down_path)


# =============================================================================
# Extract File ID
# =============================================================================
async def getIDFromURL(link: str) -> str:
    """
    Extract file ID from Google Drive link.
    
    Args:
        link: Google Drive share link
    
    Returns:
        str: file/folder ID
    """
    if "folders" in link or "file" in link:
        regex = r"https:\/\/drive\.google\.com\/(?:drive(.*?)\/folders\/|file(.*?)?\/d\/)([-\w]+)"
        res = re_search(regex, link)
        if res is None:
            await cancelTask(style_text("Invalid Google Drive Link"))
            logger.error("G-Drive ID not found")
            return ""
        return res.group(3)
    
    parsed = urlparse(link)
    return parse_qs(parsed.query)["id"][0]


# =============================================================================
# Get Files in Folder
# =============================================================================
def getFilesByFolderID(folder_id: str):
    """
    Get all files in a Google Drive folder.
    
    Args:
        folder_id: folder ID
    
    Returns:
        list: list of file objects
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
# Get File Metadata
# =============================================================================
def getFileMetadata(file_id: str):
    """
    Get metadata for a file.
    
    Args:
        file_id: file ID
    
    Returns:
        dict: file metadata
    """
    return (
        Gdrive.service.files()
        .get(fileId=file_id, supportsAllDrives=True, fields="name, id, mimeType, size")
        .execute()
    )


# =============================================================================
# Get Folder Size
# =============================================================================
def get_Gfolder_size(folder_id: str) -> int:
    """
    Calculate total size of a folder recursively.
    
    Args:
        folder_id: folder ID
    
    Returns:
        int: total size in bytes
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
        logger.error(f"Folder size error: {error}")
        return -1


# =============================================================================
# Download Single File
# =============================================================================
async def gDownloadFile(file_id: str, path: str):
    """
    Download a single file from Google Drive.
    
    Args:
        file_id: file ID
        path: download path
    """
    try:
        file = getFileMetadata(file_id)
    except HttpError as error:
        err = "File not found or not accessible"
        logger.error(err)
        await cancelTask(style_text(err))
        return
    
    if file["mimeType"].startswith("application/vnd.google-apps"):
        err = "Google Docs/Sheets/Slides cannot be downloaded directly"
        logger.error(err)
        await cancelTask(style_text(err))
        return
    
    try:
        file_name = file.get("name", f"Untitled_{file_id}")
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
                engine="GDrive ♻️"
            )
        
        Transfer.down_bytes.append(int(file["size"]))
    
    except HttpError as error:
        if error.resp.status == 403 and "User rate limit" in str(error):
            logger.error("Download quota exceeded")
            await cancelTask(style_text("Download Quota Exceeded"))
        else:
            logger.error(f"GDrive error: {error}")
            await cancelTask(style_text(f"GDrive Error: {error}"))
    
    except Exception as e:
        logger.error(f"Download error: {e}")
        await cancelTask(style_text(f"Download Error: {e}"))


# =============================================================================
# Download Folder
# =============================================================================
async def gDownloadFolder(folder_id: str, path: str):
    """
    Download a folder recursively from Google Drive.
    
    Args:
        folder_id: folder ID
        path: download path
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
