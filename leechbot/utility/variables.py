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

from time import time
from datetime import datetime
from pyrogram.types import Message


# =============================================================================
# Bot Configuration Class
# =============================================================================
class BOT:
    """
    Main bot configuration class.
    Stores all bot settings, options, modes, and states.
    """
    
    # Download sources list
    SOURCE = []
    
    # Active task reference
    TASK = None
    
    class Setting:
        """User preference settings"""
        stream_upload = "media"      # Upload mode: media or document
        convert_video = "yes"        # Video conversion enabled
        convert_quality = "low"      # Video quality: high or low
        caption = "regular"          # Caption font style
        split_video = "split"        # Video handling: split or zip
        prefix = ""                  # Filename prefix
        suffix = ""                  # Filename suffix
        thumbnail = False            # Thumbnail set status
        auto_delete = False          # Auto-delete bot messages
        auto_delete_delay = 30       # Delay in seconds
    
    class Options:
        """Runtime options for current task"""
        stream_upload = True         # Streaming upload enabled
        convert_video = True         # Video conversion enabled
        convert_quality = False      # High quality conversion
        is_split = True              # Split large videos
        caption = "code"             # Caption tag type
        video_out = "mp4"            # Output video format
        custom_name = ""             # Custom filename
        zip_pswd = ""                # Zip password
        unzip_pswd = ""              # Unzip password
    
    class Mode:
        """Current task mode"""
        mode = "leech"               # Task type: leech, mirror, dir-leech
        type = "normal"              # Upload type: normal, zip, unzip, undzip
        ytdl = False                 # YT-DLP mode enabled
    
    class State:
        """Bot state tracking"""
        started = False              # Task started flag
        task_going = False           # Task in progress flag
        prefix = False               # Waiting for prefix input
        suffix = False               # Waiting for suffix input
        setting_autodelete_delay = False  # Waiting for delay input


# =============================================================================
# YT-DLP Download Status
# =============================================================================
class YTDL:
    """
    YT-DLP download status tracker.
    Stores real-time download information.
    """
    header = ""           # Progress header message
    speed = ""            # Current download speed
    percentage = 0.0      # Download percentage
    eta = ""              # Estimated time of arrival
    done = ""             # Bytes downloaded
    left = ""             # Bytes remaining


# =============================================================================
# Transfer Statistics
# =============================================================================
class Transfer:
    """
    File transfer statistics tracker.
    Keeps track of downloaded and uploaded bytes.
    """
    down_bytes = [0, 0]           # List of downloaded file sizes
    up_bytes = [0, 0]             # List of uploaded file sizes
    total_down_size = 0           # Total download size
    sent_file = []                # List of sent message objects
    sent_file_names = []          # List of sent file names


# =============================================================================
# Task Error Handling
# =============================================================================
class TaskError:
    """
    Task error tracker.
    Stores error state and message.
    """
    state = False                 # Error occurred flag
    text = ""                     # Error message


# =============================================================================
# Time Tracking
# =============================================================================
class BotTimes:
    """
    Bot timing tracker.
    Keeps track of various timestamps for progress calculations.
    """
    current_time = time()                     # Last update time
    start_time = datetime.now()               # Task start time
    task_start = datetime.now()               # Current subtask start time


# =============================================================================
# File Paths
# =============================================================================
class Paths:
    """
    File system paths.
    Defines all working directories and file locations.
    """
    # Base working directory
    WORK_PATH = "/content/tgdl/BOT_WORK"
    
    # Thumbnail paths
    THMB_PATH = "/content/tgdl/leechbot/Thumbnail.jpg"
    VIDEO_FRAME = f"{WORK_PATH}/video_frame.jpg"
    HERO_IMAGE = f"{WORK_PATH}/Hero.jpg"
    DEFAULT_HERO = "/content/tgdl/custom_thmb.jpg"
    
    # Google Drive mount point
    MOUNTED_DRIVE = "/content/drive"
    
    # Working subdirectories
    down_path = f"{WORK_PATH}/Downloads"
    temp_dirleech_path = f"{WORK_PATH}/dir_leech_temp"
    mirror_dir = "/content/drive/MyDrive/Downloads/tgdl"
    temp_zpath = f"{WORK_PATH}/Leeched_Files"
    temp_unzip_path = f"{WORK_PATH}/Unzipped_Files"
    temp_files_dir = f"{WORK_PATH}/leech_temp"
    thumbnail_ytdl = f"{WORK_PATH}/ytdl_thumbnails"
    
    # Token file
    access_token = "/content/token.pickle"


# =============================================================================
# Message Templates
# =============================================================================
class Messages:
    """
    Message templates and texts.
    Stores dynamic message content.
    """
    caution_msg = ""              # Caution message for torrents
    download_name = ""            # Current download name
    task_msg = ""                 # Task information message
    status_head = ""              # Status header (set dynamically)
    dump_task = ""                # Task log message
    src_link = ""                 # Source link
    link_p = ""                   # Channel link part


# =============================================================================
# Message Objects
# =============================================================================
class MSG:
    """
    Telegram message objects.
    Stores references to sent messages for editing.
    """
    sent_msg = Message(id=1)       # Last sent message
    status_msg = Message(id=2)     # Status message


# =============================================================================
# Aria2c Configuration
# =============================================================================
class Aria2c:
    """
    Aria2c downloader configuration.
    Stores aria2c-specific settings and state.
    """
    link_info = False              # Link information received
    pic_dwn_url = "https://picsum.photos/900/600"  # Random image URL


# =============================================================================
# Google Drive Service
# =============================================================================
class Gdrive:
    """
    Google Drive service.
    Stores the Google Drive API service instance.
    """
    service = None                 # Google Drive API service


# =============================================================================
# Bot Statistics
# =============================================================================
class BotStats:
    """
    Bot usage statistics.
    Tracks total downloads, uploads, and other metrics.
    """
    total_tasks = 0                # Total completed tasks
    total_downloaded = 0           # Total bytes downloaded
    total_uploaded = 0             # Total bytes uploaded
    failed_tasks = 0               # Failed task count


# =============================================================================
# Constants
# =============================================================================
# Maximum file size for Telegram (2GB)
MAX_FILE_SIZE = 2097152000

# Maximum video split size (1.9GB)
MAX_VIDEO_SPLIT_SIZE = 1992294400

# Version information
VERSION = "2"
BUILD_DATE = "2026-04-10"
