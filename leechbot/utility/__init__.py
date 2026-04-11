# =============================================================================
# Telegram Leech Bot - Package Initialization
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
LeechBot utility package initialization.
Exports all core modules and functions.
"""

from .variables import BOT, YTDL, Transfer, TaskError, BotTimes, Paths, Messages, MSG, Aria2c, Gdrive, MAX_FILE_SIZE, VERSION
from .helper import isLink, getTime, sizeUnit, fileType, getSize, sysINFO, speedETA, status_bar, keyboard
from .handler import Leech, Zip_Handler, Unzip_Handler, SendLogs, cancelTask
from .task_manager import taskScheduler, task_starter
from .converters import videoConverter, sizeChecker, archive, extract
from .style import style_text, to_small_caps, style_button

__all__ = [
    "BOT",
    "YTDL",
    "Transfer",
    "TaskError",
    "BotTimes",
    "Paths",
    "Messages",
    "MSG",
    "Aria2c",
    "Gdrive",
    "MAX_FILE_SIZE",
    "VERSION",
    "isLink",
    "getTime",
    "sizeUnit",
    "fileType",
    "getSize",
    "sysINFO",
    "speedETA",
    "status_bar",
    "keyboard",
    "Leech",
    "Zip_Handler",
    "Unzip_Handler",
    "SendLogs",
    "cancelTask",
    "taskScheduler",
    "task_starter",
    "videoConverter",
    "sizeChecker",
    "archive",
    "extract",
    "style_text",
    "to_small_caps",
    "style_button",
]
