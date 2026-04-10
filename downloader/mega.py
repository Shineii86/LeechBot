# =============================================================================
# LeechBot Pro - Mega.nz Downloader
# =============================================================================
# Project   : LeechBot Pro v3.0
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://t.me/Shineii86
# =============================================================================

import subprocess
import logging
from datetime import datetime
from colab_leecher.utility.helper import update_status_bar, format_size
from colab_leecher.utility.variables import BotTimes, Messages, Paths


# =============================================================================
# MEGA DOWNLOAD
# =============================================================================
async def mega_download(link: str, num: int):
    """
    Download file from Mega.nz using megadl.
    
    Args:
        link: Mega.nz URL
        num: Download number for display
    """
    BotTimes.task_start = datetime.now()
    
    try:
        # Validate link format
        if "mega.nz" not in link and "mega.co.nz" not in link:
            logging.error("Invalid Mega.nz link format")
            return
        
        # Build command
        command = [
            "megadl",
            "--no-ask-password",
            "--path", Paths.down_path,
            link,
        ]
        
        # Start download
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
            text=True
        )
        
        # Process output
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            
            if output:
                await parse_mega_output(output.strip(), num)
        
        # Check exit code
        exit_code = process.wait()
        if exit_code != 0:
            stderr = process.stderr.read()
            logging.error(f"Mega download failed: {stderr}")
            
    except Exception as e:
        logging.error(f"Mega download error: {e}")


# =============================================================================
# OUTPUT PARSER
# =============================================================================
async def parse_mega_output(line: str, num: int):
    """
    Parse megadl output and update status.
    
    Args:
        line: Output line from megadl
        num: Download number
    """
    try:
        # Parse format: "filename: progress% downloaded_size/total_size speed"
        if ": " not in line:
            return
        
        parts = line.split(": ")
        if len(parts) < 2:
            return
        
        file_name = parts[0]
        subparts = parts[1].split()
        
        if len(subparts) < 10:
            return
        
        # Extract progress info
        progress = subparts[0].rstrip("%")
        downloaded = f"{subparts[2]} {subparts[3]}"
        total = f"{subparts[7]} {subparts[8]}"
        speed = f"{subparts[9].lstrip('(')} {subparts[10].rstrip(')')}" if len(subparts) > 10 else "N/A"
        
        Messages.download_name = file_name
        Messages.status_head = (
            f"<b>📥 DOWNLOADING</b> <code>Link {num:02d}</code>\n\n"
            f"<b>🏷️ Name:</b> <code>{file_name}</code>\n"
        )
        
        # Parse percentage
        try:
            percent = float(progress) if progress != "N/A" else 0
        except ValueError:
            percent = 0
        
        await update_status_bar(
            Messages.status_head,
            speed,
            percent,
            "Calculating...",
            downloaded,
            total,
            "Mega.nz",
        )
        
    except Exception as e:
        logging.debug(f"Mega output parse error: {e}")
