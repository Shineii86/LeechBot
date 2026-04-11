# =============================================================================
# Telegram Leech Bot - Global Variables and Configuration
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
Global variables and configuration classes for the bot.
"""

import json
import os
from time import time
from datetime import datetime
from pyrogram.types import Message

SETTINGS_FILE = "settings.json"
UPLOADED_CACHE_FILE = "uploaded_cache.json"

class BOT:
    """
    Main bot configuration class.
    Stores all bot settings, options, modes, and states.
    """
    
    # Download sources list
    SOURCE = []
    
    # Active task reference
    TASK = None
    
    # Task queue: list of (chat_id, message, sources, mode, ytdl_flag, upload_type)
    TASK_QUEUE = []
    CURRENT_TASK_OWNER = None
    
    # Duplicate detection cache: set of (file_hash, size)
    UPLOADED_FILES = set()
    
    class Setting:
        """User preference settings (persisted)"""
        stream_upload = "media"
        convert_video = "yes"
        convert_quality = "low"
        caption = "regular"
        split_video = "split"
        prefix = ""
        suffix = ""
        thumbnail = False
        auto_delete = False
        auto_delete_delay = 30
        download_speed_limit = 0      # bytes/sec, 0 = unlimited
        upload_speed_limit = 0        # bytes/sec, 0 = unlimited
        
        @classmethod
        def save(cls):
            """Save settings to JSON file."""
            data = {k: v for k, v in cls.__dict__.items() if not k.startswith("_") and not callable(v)}
            try:
                with open(SETTINGS_FILE, "w") as f:
                    json.dump(data, f, indent=2)
            except Exception:
                pass
        
        @classmethod
        def load(cls):
            """Load settings from JSON file."""
            if os.path.exists(SETTINGS_FILE):
                try:
                    with open(SETTINGS_FILE, "r") as f:
                        data = json.load(f)
                        for k, v in data.items():
                            if hasattr(cls, k):
                                setattr(cls, k, v)
                except Exception:
                    pass
    
    class Options:
        """Runtime options for current task"""
        stream_upload = True
        convert_video = True
        convert_quality = False
        is_split = True
        caption = "code"
        video_out = "mp4"
        custom_name = ""
        zip_pswd = ""
        unzip_pswd = ""
    
    class Mode:
        """Current task mode"""
        mode = "leech"
        type = "normal"
        ytdl = False
    
    class State:
        """Bot state tracking"""
        started = False
        task_going = False
        prefix = False
        suffix = False
        setting_autodelete_delay = False


class YTDL:
    """YT-DLP download status tracker."""
    header = ""
    speed = ""
    percentage = 0.0
    eta = ""
    done = ""
    left = ""


class Transfer:
    """File transfer statistics tracker."""
    down_bytes = [0, 0]
    up_bytes = [0, 0]
    total_down_size = 0
    sent_file = []
    sent_file_names = []


class TaskError:
    """Task error tracker."""
    state = False
    text = ""


class BotTimes:
    """Bot timing tracker."""
    current_time = time()
    start_time = datetime.now()
    task_start = datetime.now()


class Paths:
    """File system paths."""
    WORK_PATH = "/content/tgdl/BOT_WORK"
    THMB_PATH = "/content/tgdl/leechbot/Thumbnail.jpg"
    VIDEO_FRAME = f"{WORK_PATH}/video_frame.jpg"
    HERO_IMAGE = f"{WORK_PATH}/Hero.jpg"
    DEFAULT_HERO = "/content/tgdl/custom_thmb.jpg"
    MOUNTED_DRIVE = "/content/drive"
    down_path = f"{WORK_PATH}/Downloads"
    temp_dirleech_path = f"{WORK_PATH}/dir_leech_temp"
    mirror_dir = "/content/drive/MyDrive/Downloads/tgdl"
    temp_zpath = f"{WORK_PATH}/Leeched_Files"
    temp_unzip_path = f"{WORK_PATH}/Unzipped_Files"
    temp_files_dir = f"{WORK_PATH}/leech_temp"
    thumbnail_ytdl = f"{WORK_PATH}/ytdl_thumbnails"
    access_token = "/content/token.pickle"
    ARIA2_SESSION = f"{WORK_PATH}/aria2_session.txt"


class Messages:
    """Message templates and texts."""
    caution_msg = ""
    download_name = ""
    task_msg = ""
    status_head = ""
    dump_task = ""
    src_link = ""
    link_p = ""


class MSG:
    """Telegram message objects."""
    sent_msg = Message(id=1)
    status_msg = Message(id=2)


class Aria2c:
    """Aria2c downloader configuration."""
    link_info = False
    pic_dwn_url = "https://picsum.photos/900/600"


class Gdrive:
    """Google Drive service."""
    service = None


MAX_FILE_SIZE = 2097152000
MAX_VIDEO_SPLIT_SIZE = 1992294400
VERSION = "0.3"
BUILD_DATE = "2026-04-11"


# Load persisted data on import
def load_persisted_data():
    """Load uploaded cache and settings."""
    # Load uploaded files cache
    if os.path.exists(UPLOADED_CACHE_FILE):
        try:
            with open(UPLOADED_CACHE_FILE, "r") as f:
                data = json.load(f)
                BOT.UPLOADED_FILES = set(tuple(x) for x in data)
        except Exception:
            pass
    
    # Load settings
    BOT.Setting.load()

def save_uploaded_cache():
    """Save uploaded files cache."""
    try:
        with open(UPLOADED_CACHE_FILE, "w") as f:
            json.dump(list(BOT.UPLOADED_FILES), f)
    except Exception:
        pass

load_persisted_data()
