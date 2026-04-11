# =============================================================================
# Telegram Leech Bot - File Converters
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
File conversion module for video, archive creation, and extraction.
"""

import os
import json
import GPUtil
import shutil
import logging
import subprocess
from asyncio import sleep
from threading import Thread
from datetime import datetime
from os import makedirs, path as ospath
from moviepy.editor import VideoFileClip as VideoClip
from leechbot.utility.variables import BOT, MSG, BotTimes, Paths, Messages
from leechbot.utility.helper import getSize, fileType, keyboard, multipartArchive, sizeUnit, speedETA, status_bar, getTime
from leechbot.utility.style import style_text

logger = logging.getLogger(__name__)


# =============================================================================
# Video Conversion
# =============================================================================
async def videoConverter(file: str) -> str:
    """
    Convert video to target format.
    
    Args:
        file: path to video file
    
    Returns:
        str: path to converted file
    """
    global BOT, MSG, BotTimes
    
    def convert_to_mp4(input_file: str, out_file: str):
        """Fallback conversion using moviepy"""
        clip = VideoClip(input_file)
        clip.write_videofile(
            out_file,
            codec="libx264",
            audio_codec="aac",
            ffmpeg_params=["-strict", "-2"]
        )
    
    async def msg_updater(count: int, attempt: str, engine: str, core: str):
        """Update conversion progress"""
        bar = "░" * count + "█" + "░" * (11 - count)
        messg = f"\n┏「{bar}」"
        messg += f"\n┠⏳ **{style_text('Status')}:** `{style_text('Running')}`"
        messg += f"\n┠🔄 **{style_text('Attempt')}:** `{attempt}`"
        messg += f"\n┠🔧 **{style_text('Engine')}:** `{engine}`"
        messg += f"\n┠💪 **{style_text('Handler')}:** `{core}`"
        messg += f"\n┖⏱️ **{style_text('Elapsed')}:** `{getTime((datetime.now() - BotTimes.start_time).seconds)}`"
        
        try:
            await MSG.status_msg.edit_text(
                text=Messages.task_msg + mtext + messg + sysINFO(),
                reply_markup=keyboard()
            )
        except Exception:
            pass
    
    name, ext = ospath.splitext(file)
    
    # Skip if already in target format
    if ext.lower() in [".mkv", ".mp4"]:
        return file
    
    out_file = f"{name}.{BOT.Options.video_out}"
    gpu_available = len(GPUtil.getAvailable()) > 0
    
    # Quality settings
    quality = "-preset slow -qp 0" if BOT.Options.convert_quality else "-preset fast"
    
    # Build ffmpeg command
    if gpu_available:
        cmd = f"ffmpeg -y -i '{file}' {quality} -c:v h264_nvenc -c:a copy '{out_file}'"
        core = "GPU"
    else:
        cmd = f"ffmpeg -y -i '{file}' {quality} -c:v libx264 -c:a copy '{out_file}'"
        core = "CPU"
    
    mtext = style_text(f"**🎬 Converting Video**\n\n`{ospath.basename(file)}`\n")
    
    # Run ffmpeg
    proc = subprocess.Popen(cmd, shell=True)
    counter = 0
    
    while proc.poll() is None:
        await msg_updater(counter, "1st", "FFmpeg", core)
        counter = (counter + 1) % 12
        await sleep(3)
    
    # Check result
    error = False
    if ospath.exists(out_file) and getSize(out_file) == 0:
        os.remove(out_file)
        error = True
    elif not ospath.exists(out_file):
        error = True
    
    # Fallback to moviepy
    if error:
        logger.warning("FFmpeg failed, trying moviepy...")
        thread = Thread(target=convert_to_mp4, args=(file, out_file))
        thread.start()
        
        while thread.is_alive():
            await msg_updater(counter, "2nd", "MoviePy", "CPU")
            counter = (counter + 1) % 12
            await sleep(3)
    
    # Final check
    if ospath.exists(out_file) and getSize(out_file) > 0:
        os.remove(file)
        return out_file
    else:
        logger.error("Video conversion failed")
        return file


# =============================================================================
# File Size Checker
# =============================================================================
async def sizeChecker(file_path: str, remove: bool) -> bool:
    """
    Check if file needs splitting or archiving.
    
    Args:
        file_path: path to file
        remove: whether to remove original after processing
    
    Returns:
        bool: True if file was processed (split/archived)
    """
    max_size = 2097152000  # 2GB
    file_size = os.stat(file_path).st_size
    
    if file_size > max_size:
        if not ospath.exists(Paths.temp_zpath):
            makedirs(Paths.temp_zpath)
        
        filename = ospath.basename(file_path).lower()
        
        # Check if already an archive
        if any(filename.endswith(ext) for ext in [".zip", ".rar", ".7z", ".tar", ".gz"]):
            await splitArchive(file_path, max_size)
        else:
            f_type = fileType(file_path)
            if f_type == "video" and BOT.Options.is_split:
                await splitVideo(file_path, 1900, remove)
            else:
                await archive(file_path, True, remove)
            await sleep(2)
        
        return True
    
    return False


# =============================================================================
# Archive Creation
# =============================================================================
async def archive(path: str, is_split: bool, remove: bool):
    """
    Create zip archive.
    
    Args:
        path: path to file/folder
        is_split: whether to split large archives
        remove: whether to remove original
    """
    global BOT, Messages
    
    dir_p, p_name = ospath.split(path)
    recursive = "-r" if ospath.isdir(path) else ""
    
    if is_split:
        split = "-s 2000m" if not BOT.Options.zip_pswd else "-v2000m"
    else:
        split = ""
    
    if BOT.Options.custom_name:
        name = BOT.Options.custom_name
    elif ospath.isfile(path):
        name = ospath.basename(path)
    else:
        name = Messages.download_name
    
    Messages.status_head = style_text(f"**🗜️ Zipping**\n\n`{name}`\n")
    Messages.download_name = f"{name}.zip"
    BotTimes.task_start = datetime.now()
    
    # Build command
    if not BOT.Options.zip_pswd:
        cmd = f'cd "{dir_p}" && zip {recursive} {split} -0 "{Paths.temp_zpath}/{name}.zip" "{p_name}"'
    else:
        cmd = f'7z a -mx=0 -tzip -p{BOT.Options.zip_pswd} {split} "{Paths.temp_zpath}/{name}.zip" {path}'
    
    proc = subprocess.Popen(cmd, shell=True)
    total_size = getSize(path)
    
    while proc.poll() is None:
        speed_string, eta, percentage = speedETA(
            BotTimes.task_start, getSize(Paths.temp_zpath), total_size
        )
        await status_bar(
            Messages.status_head,
            speed_string,
            percentage,
            getTime(eta),
            sizeUnit(getSize(Paths.temp_zpath)),
            sizeUnit(total_size),
            "Zip 🗜️"
        )
        await sleep(1)
    
    if remove:
        if ospath.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)


# =============================================================================
# Archive Extraction
# =============================================================================
async def extract(zip_filepath: str, remove: bool):
    """
    Extract archive file.
    
    Args:
        zip_filepath: path to archive
        remove: whether to remove archive after extraction
    """
    global BOT, Paths, Messages
    
    _, filename = ospath.split(zip_filepath)
    Messages.status_head = style_text(f"**📂 Extracting**\n\n`{filename}`\n")
    
    password = f"-p{BOT.Options.unzip_pswd}" if BOT.Options.unzip_pswd else ""
    name, ext = ospath.splitext(filename)
    
    file_pattern = ""
    real_name = name
    
    # Determine extraction method
    if ext == ".rar":
        if "part" in name:
            cmd = f"unrar x -kb -idq {password} '{zip_filepath}' {Paths.temp_unzip_path}"
            file_pattern = "rar"
        else:
            cmd = f"unrar x {password} '{zip_filepath}' {Paths.temp_unzip_path}"
    elif ext == ".tar":
        cmd = f"tar -xvf '{zip_filepath}' -C {Paths.temp_unzip_path}"
    elif ext == ".gz":
        cmd = f"tar -zxvf '{zip_filepath}' -C {Paths.temp_unzip_path}"
    else:
        cmd = f"7z x {password} '{zip_filepath}' -o{Paths.temp_unzip_path}"
        if ext == ".001":
            file_pattern = "7z"
        elif ext == ".z01":
            file_pattern = "zip"
    
    # Get total size
    if file_pattern == "":
        total = getSize(zip_filepath)
    else:
        real_name, total = multipartArchive(zip_filepath, file_pattern, False)
    
    BotTimes.task_start = datetime.now()
    proc = subprocess.Popen(cmd, shell=True)
    
    while proc.poll() is None:
        speed_string, eta, percentage = speedETA(
            BotTimes.task_start, getSize(Paths.temp_unzip_path), total
        )
        await status_bar(
            Messages.status_head,
            speed_string,
            percentage,
            getTime(eta),
            sizeUnit(getSize(Paths.temp_unzip_path)),
            sizeUnit(total),
            "Unzip 📂"
        )
        await sleep(1)
    
    if remove:
        multipartArchive(zip_filepath, file_pattern, True)
        if ospath.exists(zip_filepath):
            os.remove(zip_filepath)
    
    Messages.download_name = real_name


# =============================================================================
# Archive Splitting
# =============================================================================
async def splitArchive(file_path: str, max_size: int):
    """
    Split large archive into chunks.
    
    Args:
        file_path: path to archive
        max_size: maximum chunk size
    """
    global Paths, BOT, MSG, Messages
    
    _, filename = ospath.split(file_path)
    new_path = f"{Paths.temp_zpath}/{filename}"
    Messages.status_head = style_text(f"**✂️ Splitting**\n\n`{filename}`\n")
    
    total_size = ospath.getsize(file_path)
    BotTimes.task_start = datetime.now()
    
    with open(file_path, "rb") as f:
        chunk = f.read(max_size)
        i = 1
        bytes_written = 0
        
        while chunk:
            ext = str(i).zfill(3)
            output_filename = f"{new_path}.{ext}"
            
            with open(output_filename, "wb") as out:
                out.write(chunk)
            
            bytes_written += len(chunk)
            speed_string, eta, percentage = speedETA(
                BotTimes.task_start, bytes_written, total_size
            )
            
            await status_bar(
                Messages.status_head,
                speed_string,
                percentage,
                getTime(eta),
                sizeUnit(bytes_written),
                sizeUnit(total_size),
                "Split ✂️"
            )
            
            chunk = f.read(max_size)
            i += 1


# =============================================================================
# Video Splitting
# =============================================================================
async def splitVideo(file_path: str, max_size: int, remove: bool):
    """
    Split large video into segments.
    
    Args:
        file_path: path to video
        max_size: maximum segment size in MB
        remove: whether to remove original
    """
    global Paths, BOT, MSG, Messages
    
    _, filename = ospath.split(file_path)
    just_name, extension = ospath.splitext(filename)
    
    # Get video bitrate
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", file_path]
    
    try:
        output = subprocess.check_output(cmd)
        video_info = json.loads(output)
        bitrate = float(video_info["format"].get("bit_rate", 1000000))
    except Exception:
        bitrate = 1000000
    
    # Calculate segment duration
    target_bits = max_size * 8 * 1024 * 1024
    duration = int(target_bits / bitrate)
    
    cmd = f'ffmpeg -i "{file_path}" -c copy -f segment -segment_time {duration} -reset_timestamps 1 "{Paths.temp_zpath}/{just_name}.part%03d{extension}"'
    
    Messages.status_head = style_text(f"**✂️ Splitting Video**\n\n`{filename}`\n")
    BotTimes.task_start = datetime.now()
    
    proc = subprocess.Popen(cmd, shell=True)
    total_size = getSize(file_path)
    
    while proc.poll() is None:
        speed_string, eta, percentage = speedETA(
            BotTimes.task_start, getSize(Paths.temp_zpath), total_size
        )
        await status_bar(
            Messages.status_head,
            speed_string,
            percentage,
            getTime(eta),
            sizeUnit(getSize(Paths.temp_zpath)),
            sizeUnit(total_size),
            "Split ✂️"
        )
        await sleep(1)
    
    if remove:
        os.remove(file_path)


# =============================================================================
# System Info Helper (import from helper)
# =============================================================================
def sysINFO():
    """Import system info from helper to avoid circular imports"""
    from leechbot.utility.helper import sysINFO as real_sysINFO
    return real_sysINFO()
