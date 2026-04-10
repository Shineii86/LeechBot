# =============================================================================
# LeechBot Pro - Configuration Settings
# =============================================================================
# Project   : LeechBot Pro v3.0
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://t.me/Shineii86
# =============================================================================

import os
import json

# =============================================================================
# TELEGRAM API CREDENTIALS
# =============================================================================
# Get these from https://my.telegram.org/auth
API_ID = int(os.environ.get("API_ID", 0))  # Your API ID
API_HASH = os.environ.get("API_HASH", "")  # Your API Hash
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")  # Get from @BotFather

# =============================================================================
# USER CONFIGURATION
# =============================================================================
# Your Telegram User ID (Get from @userinfobot)
OWNER_ID = int(os.environ.get("OWNER_ID", 0))

# Dump Channel ID for logging (Optional, starts with -100)
DUMP_ID = int(os.environ.get("DUMP_ID", 0))

# =============================================================================
# PATH CONFIGURATION
# =============================================================================
# Base working directory
BASE_PATH = "/content/leechbot"

# Subdirectories
DOWNLOAD_PATH = f"{BASE_PATH}/downloads"
WORK_PATH = f"{BASE_PATH}/work"
TEMP_PATH = f"{BASE_PATH}/temp"
THUMBNAIL_PATH = f"{BASE_PATH}/thumbnail.jpg"
LOG_PATH = f"{BASE_PATH}/logs"

# Google Drive mirror path
GDRIVE_MIRROR_PATH = "/content/drive/MyDrive/LeechBot_Downloads"

# Google Drive token
TOKEN_PICKLE = f"{BASE_PATH}/token.pickle"
CREDENTIALS_JSON = f"{BASE_PATH}/credentials.json"

# =============================================================================
# DOWNLOAD SETTINGS
# =============================================================================
# Maximum file size before splitting (2GB = 2147483648 bytes)
MAX_FILE_SIZE = 2097152000

# Video split size (1.9GB for safety)
VIDEO_SPLIT_SIZE = 1999999999

# Aria2c configuration
ARIA2_MAX_CONNECTIONS = 16
ARIA2_SPLIT = 10
ARIA2_MAX_TRIES = 3

# =============================================================================
# UPLOAD SETTINGS
# =============================================================================
# Default upload mode: "media" or "document"
DEFAULT_UPLOAD_MODE = "media"

# Caption length limit
MAX_CAPTION_LENGTH = 1024

# =============================================================================
# VIDEO CONVERSION SETTINGS
# =============================================================================
# Default video output format
DEFAULT_VIDEO_FORMAT = "mp4"

# Conversion quality: "high" or "low"
DEFAULT_CONVERT_QUALITY = "low"

# Enable/disable video conversion by default
AUTO_CONVERT_VIDEO = True

# =============================================================================
# BOT MESSAGES & UI
# =============================================================================
# Bot version
BOT_VERSION = "3.0.0"

# Bot name
BOT_NAME = "LeechBot Pro"

# Developer info
DEVELOPER_NAME = "Shinei Nouzen"
DEVELOPER_GITHUB = "https://github.com/Shineii86"
DEVELOPER_TELEGRAM = "https://t.me/Shineii86"
DEVELOPER_TWITTER = "https://x.com/Shineii86"

# =============================================================================
# ADVANCED SETTINGS
# =============================================================================
# Enable debug logging
DEBUG_MODE = False

# Log level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = "INFO"

# Status update interval (seconds)
STATUS_UPDATE_INTERVAL = 3

# Maximum concurrent downloads
MAX_CONCURRENT_DOWNLOADS = 3

# Enable auto-retry on failure
AUTO_RETRY = True
MAX_RETRY_ATTEMPTS = 3

# =============================================================================
# TRACKER URLS FOR TORRENTS
# =============================================================================
TRACKER_URLS = [
    "https://cf.trackerslist.com/best_aria2.txt",
    "https://cf.trackerslist.com/all_aria2.txt",
    "https://cf.trackerslist.com/http_aria2.txt",
]

# =============================================================================
# YT-DLP SETTINGS
# =============================================================================
YTDL_OPTIONS = {
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
    "writethumbnail": True,
    "concurrent_fragment_downloads": 4,
    "overwrites": True,
    "writesubtitles": True,
    "subtitleslangs": ["en"],
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def load_credentials_from_json(filepath: str = "credentials.json"):
    """
    Load credentials from a JSON file.
    
    Args:
        filepath: Path to the credentials JSON file
        
    Returns:
        dict: Credentials dictionary
    """
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def ensure_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        BASE_PATH,
        DOWNLOAD_PATH,
        WORK_PATH,
        TEMP_PATH,
        LOG_PATH,
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# Auto-create directories on import
ensure_directories()
