# =============================================================================
# Telegram Leech Bot - Mega.nz Downloader
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
Mega.nz downloader module.

Handles downloads from Mega.nz using megatools.
"""

import subprocess
import logging
from datetime import datetime
from leechbot.utility.helper import status_bar
from leechbot.utility.variables import BotTimes, Messages, Paths
from leechbot.utility.style import style_text

logger = logging.getLogger(__name__)


# =============================================================================
# Main Download Function
# =============================================================================
async def megadl(link: str, num: int):
    """
    Download file from Mega.nz.
    
    Args:
        link: Mega.nz share link
        num: link number for display
    """
    global BotTimes, Messages
    
    BotTimes.task_start = datetime.now()
    
    try:
        # Build megadl command
        command = [
            "megadl",
            "--no-ask-password",
            "--path", Paths.down_path,
            link
        ]
        
        # Execute download
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0
        )
        
        # Read output
        while True:
            output = process.stdout.readline()
            if output == b"" and process.poll() is not None:
                break
            
            if output:
                await extract_info(output.strip().decode("utf-8"), num)
    
    except Exception as e:
        logger.error(f"Mega download error: {e}")


# =============================================================================
# Progress Extraction
# =============================================================================
async def extract_info(line: str, num: int):
    """
    Extract download progress from megadl output.
    
    Args:
        line: output line
        num: link number
    """
    try:
        parts = line.split(": ")
        subparts = parts[1].split() if len(parts) > 1 else []
        
        file_name = "N/A"
        progress = "N/A"
        downloaded_size = "N/A"
        total_size = "N/A"
        speed = "N/A"
        
        if len(subparts) > 10:
            file_name = parts[0]
            Messages.download_name = file_name
            progress = subparts[0][:-1]
            if progress != "N/A":
                progress = round(float(progress))
            downloaded_size = f"{subparts[2]} {subparts[3]}"
            total_size = f"{subparts[7]} {subparts[8]}"
            speed = f"{subparts[9][1:]} {subparts[10][:-1]}"
        
        Messages.status_head = style_text(f"**📥 Downloading** `Link {str(num).zfill(2)}`\n\n**🏷️ Name:** ") + f"`{file_name}`\n"
        
        await status_bar(
            Messages.status_head,
            speed,
            progress,
            "Calculating...",
            downloaded_size,
            total_size,
            "Mega 💾"
        )
    
    except Exception as e:
        logger.error(f"Mega progress error: {e}")
