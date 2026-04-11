# =============================================================================
# Telegram Leech Bot - Task Handlers
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
Main leech task handlers for file processing, zipping, and upload.
"""

import os
import shutil
import logging
import pathlib
from asyncio import sleep
from time import time
from leechbot import OWNER, leechbot
from natsort import natsorted
from datetime import datetime
from os import makedirs, path as ospath
from leechbot.uploader.telegram import upload_file
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from leechbot.utility.variables import BOT, MSG, BotTimes, Messages, Paths, Transfer
from leechbot.utility.converters import archive, extract, videoConverter, sizeChecker
from leechbot.utility.helper import fileType, getSize, getTime, keyboard, shortFileName, sizeUnit, sysINFO
from leechbot.utility.style import style_text

logger = logging.getLogger(__name__)


# =============================================================================
# Main Leech Function
# =============================================================================
async def Leech(folder_path: str, remove: bool):
    """
    Main leech function to process and upload files.
    
    Args:
        folder_path: path to folder containing files
        remove: whether to remove files after upload
    """
    global BOT, BotTimes, Messages, Paths, Transfer
    
    # Get all files in folder
    files = [str(p) for p in pathlib.Path(folder_path).glob("**/*") if p.is_file()]
    
    # Convert videos if needed
    for f in natsorted(files):
        file_path = ospath.join(folder_path, f)
        if BOT.Options.convert_video and fileType(file_path) == "video":
            file_path = await videoConverter(file_path)
    
    Transfer.total_down_size = getSize(folder_path)
    
    # Process and upload files
    files = [str(p) for p in pathlib.Path(folder_path).glob("**/*") if p.is_file()]
    for f in natsorted(files):
        file_path = ospath.join(folder_path, f)
        leech_result = await sizeChecker(file_path, remove)
        
        if leech_result:  # File was split
            if ospath.exists(file_path) and remove:
                os.remove(file_path)
            
            dir_list = natsorted(os.listdir(Paths.temp_zpath))
            count = 1
            
            for dir_path in dir_list:
                short_path = ospath.join(Paths.temp_zpath, dir_path)
                file_name = ospath.basename(short_path)
                new_path = shortFileName(short_path)
                os.rename(short_path, new_path)
                
                BotTimes.current_time = time()
                Messages.status_head = style_text(f"**📤 Uploading Split** `{count}/{len(dir_list)}`\n\n`{file_name}`\n")
                
                try:
                    MSG.status_msg = await MSG.status_msg.edit_text(
                        text=Messages.task_msg + Messages.status_head + "\n⏳ " + style_text("Starting...") + sysINFO(),
                        reply_markup=keyboard()
                    )
                except Exception as e:
                    logger.info(e)
                
                await upload_file(new_path, file_name)
                Transfer.up_bytes.append(os.stat(new_path).st_size)
                count += 1
            
            shutil.rmtree(Paths.temp_zpath)
        
        else:  # Regular file upload
            if not ospath.exists(Paths.temp_files_dir):
                makedirs(Paths.temp_files_dir)
            
            if not remove:
                file_path = shutil.copy(file_path, Paths.temp_files_dir)
            
            file_name = ospath.basename(file_path)
            new_path = shortFileName(file_path)
            os.rename(file_path, new_path)
            
            BotTimes.current_time = time()
            Messages.status_head = style_text(f"**📤 Uploading**\n\n`{file_name}`\n")
            
            try:
                MSG.status_msg = await MSG.status_msg.edit_text(
                    text=Messages.task_msg + Messages.status_head + "\n⏳ " + style_text("Starting...") + sysINFO(),
                    reply_markup=keyboard()
                )
            except Exception as e:
                logger.error(f"Status update error: {e}")
            
            file_size = os.stat(new_path).st_size
            await upload_file(new_path, file_name)
            Transfer.up_bytes.append(file_size)
            
            if remove:
                if ospath.exists(new_path):
                    os.remove(new_path)
            else:
                for file in os.listdir(Paths.temp_files_dir):
                    os.remove(ospath.join(Paths.temp_files_dir, file))
    
    # Cleanup
    if remove and ospath.exists(folder_path):
        shutil.rmtree(folder_path)
    if ospath.exists(Paths.thumbnail_ytdl):
        shutil.rmtree(Paths.thumbnail_ytdl)
    if ospath.exists(Paths.temp_files_dir):
        shutil.rmtree(Paths.temp_files_dir)


# =============================================================================
# Zip Handler
# =============================================================================
async def Zip_Handler(down_path: str, is_split: bool, remove: bool):
    """
    Handle zip compression of files.
    
    Args:
        down_path: path to file/folder to zip
        is_split: whether to split large archives
        remove: whether to remove original files
    """
    global BOT, Messages, MSG, Transfer
    
    Messages.status_head = style_text(f"**🗜️ Zipping**\n\n`{Messages.download_name}`\n")
    
    try:
        MSG.status_msg = await MSG.status_msg.edit_text(
            text=Messages.task_msg + Messages.status_head + sysINFO(),
            reply_markup=keyboard()
        )
    except Exception as e:
        logger.error(f"Zip handler error: {e}")
    
    logger.info("Starting zip compression...")
    BotTimes.current_time = time()
    
    if not ospath.exists(Paths.temp_zpath):
        makedirs(Paths.temp_zpath)
    
    await archive(down_path, is_split, remove)
    await sleep(2)
    
    Transfer.total_down_size = getSize(Paths.temp_zpath)
    
    if remove and ospath.exists(down_path):
        shutil.rmtree(down_path)


# =============================================================================
# Unzip Handler
# =============================================================================
async def Unzip_Handler(down_path: str, remove: bool):
    """
    Handle extraction of archive files.
    
    Args:
        down_path: path containing archives
        remove: whether to remove archives after extraction
    """
    global MSG, Messages
    
    Messages.status_head = style_text(f"\n**📂 Extracting**\n\n`{Messages.download_name}`\n")
    
    MSG.status_msg = await MSG.status_msg.edit_text(
        text=Messages.task_msg + Messages.status_head + "\n⏳ " + style_text("Starting...") + sysINFO(),
        reply_markup=keyboard()
    )
    
    filenames = [str(p) for p in pathlib.Path(down_path).glob("**/*") if p.is_file()]
    
    for f in natsorted(filenames):
        short_path = ospath.join(down_path, f)
        if not ospath.exists(Paths.temp_unzip_path):
            makedirs(Paths.temp_unzip_path)
        
        filename = ospath.basename(f).lower()
        _, ext = ospath.splitext(filename)
        
        try:
            if ospath.exists(short_path):
                if ext in [".7z", ".gz", ".zip", ".rar", ".001", ".tar", ".z01"]:
                    await extract(short_path, remove)
                else:
                    shutil.copy(short_path, Paths.temp_unzip_path)
        except Exception as e:
            logger.error(f"Unzip handler error: {e}")
    
    if remove:
        shutil.rmtree(down_path)


# =============================================================================
# Task Cancellation
# =============================================================================
async def cancelTask(reason: str):
    """
    Cancel the current running task.
    
    Args:
        reason: cancellation reason
    """
    text = style_text(f"""**❌ Task Cancelled**

┏🔗 **Source:** [Here]({Messages.src_link})
┠🎯 **Mode:** `{BOT.Mode.mode.capitalize()}`
┠⚠️ **Reason:** `{reason}`
┗⏱️ **Elapsed:** `{getTime((datetime.now() - BotTimes.start_time).seconds)}`""")
    
    if BOT.State.task_going:
        try:
            BOT.TASK.cancel()
            shutil.rmtree(Paths.WORK_PATH)
        except Exception as e:
            logger.error(f"Task cancellation error: {e}")
        else:
            logger.info("Task cancelled successfully")
        finally:
            BOT.State.task_going = False
            await MSG.status_msg.delete()
            await leechbot.send_message(
                chat_id=OWNER,
                text=text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(style_button("📣 Channel"), url="https://t.me/MaximXBots", style="primary"),
                            InlineKeyboardButton(style_button("Support 💬"), url="https://t.me/MaximXGroup", style="success"),
                        ]
                    ]
                )
            )


# =============================================================================
# Completion Logs
# =============================================================================
async def SendLogs(is_leech: bool):
    """
    Send completion logs and summary.
    
    Args:
        is_leech: whether this was a leech task
    """
    global Transfer, Messages
    
    final_text = style_text(f"**📋 File List:** `{len(Transfer.sent_file)}`\n\n**📜 Logs:**\n")
    
    if is_leech:
        file_count = f"┠📋 **Files:** `{len(Transfer.sent_file)}`\n"
        size = sizeUnit(sum(Transfer.up_bytes))
    else:
        file_count = ""
        size = sizeUnit(Transfer.total_down_size)
    
    summary = style_text(f"""

**✅ Task Complete**

┏📛 **Name:** `{Messages.download_name}`
┠📦 **Size:** `{size}`
{file_count}
┠⏱️ **Time:** `{getTime((datetime.now() - BotTimes.start_time).seconds)}`
┗🤖 **By:** [LeechBot](https://github.com/Shineii86/LeechBot)""")
    
    if BOT.State.task_going:
        await MSG.sent_msg.reply_text(
            text=f"**🔗 Source:** [Here]({Messages.src_link})" + summary
        )
        
        await MSG.status_msg.edit_text(
            text=Messages.task_msg + summary,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(style_button("📣 Channel"), url="https://t.me/MaximXBots", style="primary"),
                        InlineKeyboardButton(style_button("Support 💬"), url="https://t.me/MaximXGroup", style="success"),
                    ],
                    [
                        InlineKeyboardButton(style_button("📂 GitHub ✨"), url="https://github.com/Shineii86/LeechBot", style="primary"),
                    ]
                ]
            )
        )
        
        # Send file list if leech task
        if is_leech:
            try:
                final_texts = []
                for i in range(len(Transfer.sent_file)):
                    file_link = f"https://t.me/c/{Messages.link_p}/{Transfer.sent_file[i].id}"
                    fileName = Transfer.sent_file_names[i]
                    fileText = f"\n({str(i+1).zfill(2)}) [{fileName}]({file_link})"
                    
                    if len(final_text + fileText) >= 4096:
                        final_texts.append(final_text)
                        final_text = fileText
                    else:
                        final_text += fileText
                
                final_texts.append(final_text)
                
                for fn_txt in final_texts:
                    MSG.status_msg = await MSG.status_msg.reply_text(text=fn_txt)
            
            except Exception as e:
                error_msg = f"**❌ Log Error:** `{e}`"
                await MSG.status_msg.reply_text(text=error_msg)
    
    BOT.State.started = False
    BOT.State.task_going = False
