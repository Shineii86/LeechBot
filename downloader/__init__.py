# =============================================================================
# LeechBot Pro - Downloader Module
# =============================================================================
# Project   : LeechBot Pro v3.0
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://t.me/Shineii86
# =============================================================================

from .aria2 import aria2_download, get_aria2_name
from .ytdl import youtube_download, get_youtube_name
from .gdrive import (
    google_download,
    build_service,
    get_id_from_url,
    get_file_metadata,
    get_folder_size,
)
from .telegram import telegram_download, get_media_info
from .mega import mega_download
from .terabox import terabox_download
from .manager import download_manager
