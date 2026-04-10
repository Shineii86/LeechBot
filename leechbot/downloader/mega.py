# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ᴍᴇɢᴀ.ɴᴢ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ᴍᴏᴅᴜʟᴇ

ᴛʜɪs ᴍᴏᴅᴜʟᴇ ʜᴀɴᴅʟᴇs ᴅᴏᴡɴʟᴏᴀᴅs ғʀᴏᴍ ᴍᴇɢᴀ.ɴᴢ ᴜsɪɴɢ ᴍᴇɢᴀᴛᴏᴏʟs.
"""

import subprocess
import logging
from datetime import datetime
from leechbot.utility.helper import status_bar
from leechbot.utility.variables import BotTimes, Messages, Paths

logger = logging.getLogger(__name__)


# =============================================================================
#  ᴍᴀɪɴ ᴅᴏᴡɴʟᴏᴀᴅ ғᴜɴᴄᴛɪᴏɴ
# =============================================================================
async def megadl(link: str, num: int):
    """
    ᴅᴏᴡɴʟᴏᴀᴅ ғɪʟᴇ ғʀᴏᴍ ᴍᴇɢᴀ.ɴᴢ.
    
    ᴀʀɢs:
        ʟɪɴᴋ: ᴍᴇɢᴀ.ɴᴢ sʜᴀʀᴇ ʟɪɴᴋ
        ɴᴜᴍ: ʟɪɴᴋ ɴᴜᴍʙᴇʀ ғᴏʀ ᴅɪsᴘʟᴀʏ
    """
    global BotTimes, Messages
    
    BotTimes.task_start = datetime.now()
    
    try:
        # ʙᴜɪʟᴅ ᴍᴇɢᴀᴅʟ ᴄᴏᴍᴍᴀɴᴅ
        command = [
            "megadl",
            "--no-ask-password",
            "--path", Paths.down_path,
            link
        ]
        
        # ᴇxᴇᴄᴜᴛᴇ ᴅᴏᴡɴʟᴏᴀᴅ
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0
        )
        
        # ʀᴇᴀᴅ ᴏᴜᴛᴘᴜᴛ
        while True:
            output = process.stdout.readline()
            if output == b"" and process.poll() is not None:
                break
            
            if output:
                await extract_info(output.strip().decode("utf-8"), num)
    
    except Exception as e:
        logger.error(f"ᴍᴇɢᴀ ᴅᴏᴡɴʟᴏᴀᴅ ᴇʀʀᴏʀ: {e}")


# =============================================================================
#  ᴘʀᴏɢʀᴇss ᴇxᴛʀᴀᴄᴛɪᴏɴ
# =============================================================================
async def extract_info(line: str, num: int):
    """
    ᴇxᴛʀᴀᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ ᴘʀᴏɢʀᴇss ғʀᴏᴍ ᴍᴇɢᴀᴅʟ ᴏᴜᴛᴘᴜᴛ.
    
    ᴀʀɢs:
        ʟɪɴᴇ: ᴏᴜᴛᴘᴜᴛ ʟɪɴᴇ
        ɴᴜᴍ: ʟɪɴᴋ ɴᴜᴍʙᴇʀ
    """
    try:
        parts = line.split(": ")
        subparts = parts[1].split() if len(parts) > 1 else []
        
        file_name = "ɴ/ᴀ"
        progress = "ɴ/ᴀ"
        downloaded_size = "ɴ/ᴀ"
        total_size = "ɴ/ᴀ"
        speed = "ɴ/ᴀ"
        
        if len(subparts) > 10:
            file_name = parts[0]
            Messages.download_name = file_name
            progress = subparts[0][:-1]
            if progress != "ɴ/ᴀ":
                progress = round(float(progress))
            downloaded_size = f"{subparts[2]} {subparts[3]}"
            total_size = f"{subparts[7]} {subparts[8]}"
            speed = f"{subparts[9][1:]} {subparts[10][:-1]}"
        
        Messages.status_head = f"**📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ** `ʟɪɴᴋ {str(num).zfill(2)}`\n\n**🏷️ ɴᴀᴍᴇ:** `{file_name}`\n"
        
        await status_bar(
            Messages.status_head,
            speed,
            progress,
            "ᴄᴀʟᴄᴜʟᴀᴛɪɴɢ...",
            downloaded_size,
            total_size,
            "ᴍᴇɢᴀ 💾"
        )
    
    except Exception as e:
        logger.error(f"ᴍᴇɢᴀ ᴘʀᴏɢʀᴇss ᴇʀʀᴏʀ: {e}")
