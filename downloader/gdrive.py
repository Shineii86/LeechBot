# =============================================================================
# LeechBot Pro - Google Drive Downloader
# =============================================================================
# Project   : LeechBot Pro v3.0
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://t.me/Shineii86
# =============================================================================

import io
import re
import logging
import pickle
from natsort import natsorted
from os import makedirs, path as ospath
from urllib.parse import parse_qs, urlparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from colab_leecher.utility.handler import cancel_task
from colab_leecher.utility.helper import format_size, get_time_string, update_status_bar, calculate_speed_eta
from colab_leecher.utility.variables import Gdrive, Messages, Paths, BotTimes, Transfer


# =============================================================================
# SERVICE BUILDER
# =============================================================================
async def build_service():
    """Build Google Drive API service from token.pickle."""
    if ospath.exists(Paths.access_token):
        try:
            with open(Paths.access_token, "rb") as token:
                creds = pickle.load(token)
                Gdrive.service = build("drive", "v3", credentials=creds, cache_discovery=False)
        except Exception as e:
            logging.error(f"Failed to build service: {e}")
            await cancel_task("Failed to initialize Google Drive. Please re-authenticate.")
    else:
        await cancel_task("token.pickle not found. Please authenticate with Google Drive first.")


# =============================================================================
# URL PARSER
# =============================================================================
async def get_id_from_url(link: str) -> str:
    """
    Extract file/folder ID from Google Drive URL.
    
    Args:
        link: Google Drive URL
        
    Returns:
        str: File ID
    """
    # Handle different URL formats
    patterns = [
        r"/folders/([-\w]+)",
        r"/file/d/([-\w]+)",
        r"id=([-\w]+)",
        r"open\?id=([-\w]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)
    
    await cancel_task("Could not extract Google Drive ID from URL")
    return ""


# =============================================================================
# METADATA FUNCTIONS
# =============================================================================
def get_file_metadata(file_id: str) -> dict:
    """
    Get file metadata from Google Drive.
    
    Args:
        file_id: Google Drive file ID
        
    Returns:
        dict: File metadata
    """
    return Gdrive.service.files().get(
        fileId=file_id,
        supportsAllDrives=True,
        fields="name, id, mimeType, size, modifiedTime"
    ).execute()


def get_files_in_folder(folder_id: str) -> list:
    """
    List all files in a folder.
    
    Args:
        folder_id: Folder ID
        
    Returns:
        list: List of file metadata
    """
    files = []
    page_token = None
    
    while True:
        response = Gdrive.service.files().list(
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            q=f"'{folder_id}' in parents and trashed = false",
            spaces="drive",
            pageSize=200,
            fields="nextPageToken, files(id, name, mimeType, size, shortcutDetails)",
            orderBy="folder, name",
            pageToken=page_token,
        ).execute()
        
        files.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        
        if not page_token:
            break
    
    return files


def get_folder_size(folder_id: str) -> int:
    """
    Calculate total size of folder contents recursively.
    
    Args:
        folder_id: Folder ID
        
    Returns:
        int: Total size in bytes
    """
    total_size = 0
    
    try:
        query = f"trashed = false and '{folder_id}' in parents"
        results = Gdrive.service.files().list(
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            q=query,
            fields="files(id, mimeType, size, shortcutDetails)",
        ).execute()
        
        items = results.get("files", [])
        
        for item in items:
            mime_type = item.get("mimeType", "")
            
            # Handle shortcuts
            shortcut = item.get("shortcutDetails")
            if shortcut:
                mime_type = shortcut.get("targetMimeType", mime_type)
                item["id"] = shortcut.get("targetId", item["id"])
            
            # Recurse into folders
            if mime_type == "application/vnd.google-apps.folder":
                total_size += get_folder_size(item["id"])
            else:
                size = item.get("size")
                if size:
                    total_size += int(size)
                    
    except HttpError as e:
        logging.error(f"Folder size error: {e}")
    
    return total_size


# =============================================================================
# DOWNLOAD FUNCTIONS
# =============================================================================
async def google_download(link: str, num: int):
    """
    Download file from Google Drive.
    
    Args:
        link: Google Drive URL
        num: Download number for display
    """
    global down_msg
    
    file_id = await get_id_from_url(link)
    meta = get_file_metadata(file_id)
    
    Messages.status_head = (
        f"<b>📥 DOWNLOADING</b> <code>Link {num:02d}</code>\n\n"
        f"<b>🏷️ Name:</b> <code>{Messages.download_name}</code>\n"
    )
    
    # Check if folder or file
    if meta.get("mimeType") == "application/vnd.google-apps.folder":
        await download_folder(file_id, Paths.down_path)
    else:
        await download_file(file_id, Paths.down_path)


async def download_file(file_id: str, path: str):
    """
    Download single file from Google Drive.
    
    Args:
        file_id: File ID
        path: Download destination
    """
    try:
        file = get_file_metadata(file_id)
    except HttpError as e:
        await cancel_task(f"File not found or not accessible: {e}")
        return
    
    # Check for Google Workspace files
    if file["mimeType"].startswith("application/vnd.google-apps"):
        await cancel_task(
            "Google Workspace files (Docs, Sheets, etc.) cannot be downloaded directly. "
            "Please export them first."
        )
        return
    
    try:
        file_name = file.get("name", f"untitled_{file_id}")
        file_path = ospath.join(path, file_name)
        file_size = int(file.get("size", 0))
        
        # Setup download
        file_buffer = io.BytesIO()
        request = Gdrive.service.files().get_media(
            fileId=file_id,
            supportsAllDrives=True
        )
        
        downloader = MediaIoBaseDownload(
            file_buffer,
            request,
            chunksize=70 * 1024 * 1024  # 70MB chunks
        )
        
        BotTimes.task_start = datetime.now()
        done = False
        
        while not done:
            status, done = downloader.next_chunk()
            
            # Write chunk to file
            file_buffer.seek(0)
            with open(file_path, "ab") as f:
                f.write(file_buffer.getvalue())
            file_buffer.seek(0)
            file_buffer.truncate()
            
            # Update progress
            if status:
                downloaded = int(status.progress() * file_size)
                total_done = sum(Transfer.down_bytes) + downloaded
                
                speed, eta, percent = calculate_speed_eta(
                    BotTimes.task_start,
                    total_done,
                    Transfer.total_down_size
                )
                
                await update_status_bar(
                    down_msg=Messages.status_head,
                    speed=speed,
                    percentage=percent,
                    eta=get_time_string(eta),
                    done=format_size(total_done),
                    left=format_size(Transfer.total_down_size),
                    engine="Google Drive API",
                )
        
        Transfer.down_bytes.append(file_size)
        
    except HttpError as e:
        if e.resp.status == 403 and "User Rate Limit Exceeded" in str(e):
            await cancel_task("Google Drive download quota exceeded for this file.")
        else:
            await cancel_task(f"Download error: {e}")
    except Exception as e:
        await cancel_task(f"Unexpected error: {e}")


async def download_folder(folder_id: str, path: str):
    """
    Download folder contents recursively.
    
    Args:
        folder_id: Folder ID
        path: Download destination
    """
    folder_meta = get_file_metadata(folder_id)
    folder_name = folder_meta.get("name", "Untitled Folder")
    folder_path = ospath.join(path, folder_name)
    
    if not ospath.exists(folder_path):
        makedirs(folder_path)
    
    # Get folder contents
    items = get_files_in_folder(folder_id)
    
    if not items:
        return
    
    # Sort naturally
    items = natsorted(items, key=lambda x: x.get("name", ""))
    
    for item in items:
        file_id = item["id"]
        mime_type = item.get("mimeType", "")
        
        # Handle shortcuts
        shortcut = item.get("shortcutDetails")
        if shortcut:
            file_id = shortcut.get("targetId", file_id)
            mime_type = shortcut.get("targetMimeType", mime_type)
        
        # Recurse into subfolders
        if mime_type == "application/vnd.google-apps.folder":
            await download_folder(file_id, folder_path)
        else:
            await download_file(file_id, folder_path)
