# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ʟᴇᴇᴄʜʙᴏᴛ ᴛᴀsᴋ ʜᴀɴᴅʟᴇʀs

ᴛʜɪs ᴍᴏᴅᴜʟᴇ ᴄᴏɴᴛᴀɪɴs ᴛʜᴇ ᴍᴀɪɴ ʟᴇᴇᴄʜ, ᴢɪᴘ, ᴜɴᴢɪᴘ, ᴀɴᴅ ʟᴏɢ ɢᴇɴᴇʀᴀᴛɪᴏɴ ғᴜɴᴄᴛɪᴏɴs.
ɪᴛ ʜᴀɴᴅʟᴇs ғɪʟᴇ ᴜᴘʟᴏᴀᴅs, ᴄᴀɴᴄᴇʟʟᴀᴛɪᴏɴs, ᴀɴᴅ ᴄᴏᴍᴘʟᴇᴛɪᴏɴ ʟᴏɢs.
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

logger = logging.getLogger(__name__)


# =============================================================================
#  ᴍᴀɪɴ ʟᴇᴇᴄʜ ғᴜɴᴄᴛɪᴏɴ
# =============================================================================
async def Leech(folder_path: str, remove: bool):
    """
    ᴍᴀɪɴ ʟᴇᴇᴄʜ ғᴜɴᴄᴛɪᴏɴ ᴛᴏ ᴘʀᴏᴄᴇss ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ғɪʟᴇs.
    
    ᴀʀɢs:
        ғᴏʟᴅᴇʀ_ᴘᴀᴛʜ: ᴘᴀᴛʜ ᴛᴏ ғᴏʟᴅᴇʀ ᴄᴏɴᴛᴀɪɴɪɴɢ ғɪʟᴇs
        ʀᴇᴍᴏᴠᴇ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ʀᴇᴍᴏᴠᴇ ғɪʟᴇs ᴀғᴛᴇʀ ᴜᴘʟᴏᴀᴅ
    """
    global BOT, BotTimes, Messages, Paths, Transfer
    
    # ɢᴇᴛ ᴀʟʟ ғɪʟᴇs ɪɴ ғᴏʟᴅᴇʀ
    files = [str(p) for p in pathlib.Path(folder_path).glob("**/*") if p.is_file()]
    
    # ᴄᴏɴᴠᴇʀᴛ ᴠɪᴅᴇᴏs ɪғ ɴᴇᴇᴅᴇᴅ
    for f in natsorted(files):
        file_path = ospath.join(folder_path, f)
        if BOT.Options.convert_video and fileType(file_path) == "video":
            file_path = await videoConverter(file_path)
    
    Transfer.total_down_size = getSize(folder_path)
    
    # ᴘʀᴏᴄᴇss ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ғɪʟᴇs
    files = [str(p) for p in pathlib.Path(folder_path).glob("**/*") if p.is_file()]
    for f in natsorted(files):
        file_path = ospath.join(folder_path, f)
        leech_result = await sizeChecker(file_path, remove)
        
        if leech_result:  # ғɪʟᴇ ᴡᴀs sᴘʟɪᴛ
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
                Messages.status_head = f"**📤 ᴜᴘʟᴏᴀᴅɪɴɢ sᴘʟɪᴛ** `{count}/{len(dir_list)}`\n\n`{file_name}`\n"
                
                try:
                    MSG.status_msg = await MSG.status_msg.edit_text(
                        text=Messages.task_msg + Messages.status_head + "\n⏳ `sᴛᴀʀᴛɪɴɢ...`" + sysINFO(),
                        reply_markup=keyboard()
                    )
                except Exception as e:
                    logger.info(e)
                
                await upload_file(new_path, file_name)
                Transfer.up_bytes.append(os.stat(new_path).st_size)
                count += 1
            
            shutil.rmtree(Paths.temp_zpath)
        
        else:  # ʀᴇɢᴜʟᴀʀ ғɪʟᴇ ᴜᴘʟᴏᴀᴅ
            if not ospath.exists(Paths.temp_files_dir):
                makedirs(Paths.temp_files_dir)
            
            if not remove:
                file_path = shutil.copy(file_path, Paths.temp_files_dir)
            
            file_name = ospath.basename(file_path)
            new_path = shortFileName(file_path)
            os.rename(file_path, new_path)
            
            BotTimes.current_time = time()
            Messages.status_head = f"**📤 ᴜᴘʟᴏᴀᴅɪɴɢ**\n\n`{file_name}`\n"
            
            try:
                MSG.status_msg = await MSG.status_msg.edit_text(
                    text=Messages.task_msg + Messages.status_head + "\n⏳ `sᴛᴀʀᴛɪɴɢ...`" + sysINFO(),
                    reply_markup=keyboard()
                )
            except Exception as e:
                logger.error(f"sᴛᴀᴛᴜs ᴜᴘᴅᴀᴛᴇ ᴇʀʀᴏʀ: {e}")
            
            file_size = os.stat(new_path).st_size
            await upload_file(new_path, file_name)
            Transfer.up_bytes.append(file_size)
            
            if remove:
                if ospath.exists(new_path):
                    os.remove(new_path)
            else:
                for file in os.listdir(Paths.temp_files_dir):
                    os.remove(ospath.join(Paths.temp_files_dir, file))
    
    # ᴄʟᴇᴀɴᴜᴘ
    if remove and ospath.exists(folder_path):
        shutil.rmtree(folder_path)
    if ospath.exists(Paths.thumbnail_ytdl):
        shutil.rmtree(Paths.thumbnail_ytdl)
    if ospath.exists(Paths.temp_files_dir):
        shutil.rmtree(Paths.temp_files_dir)


# =============================================================================
#  ᴢɪᴘ ʜᴀɴᴅʟᴇʀ
# =============================================================================
async def Zip_Handler(down_path: str, is_split: bool, remove: bool):
    """
    ʜᴀɴᴅʟᴇ ᴢɪᴘ ᴄᴏᴍᴘʀᴇssɪᴏɴ ᴏғ ғɪʟᴇs.
    
    ᴀʀɢs:
        ᴅᴏᴡɴ_ᴘᴀᴛʜ: ᴘᴀᴛʜ ᴛᴏ ғᴏʟᴅᴇʀ/ғɪʟᴇ ᴛᴏ ᴢɪᴘ
        ɪs_sᴘʟɪᴛ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ sᴘʟɪᴛ ʟᴀʀɢᴇ ᴀʀᴄʜɪᴠᴇs
        ʀᴇᴍᴏᴠᴇ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴏʀɪɢɪɴᴀʟ ғɪʟᴇs
    """
    global BOT, Messages, MSG, Transfer
    
    Messages.status_head = f"**🗜️ ᴢɪᴘᴘɪɴɢ**\n\n`{Messages.download_name}`\n"
    
    try:
        MSG.status_msg = await MSG.status_msg.edit_text(
            text=Messages.task_msg + Messages.status_head + sysINFO(),
            reply_markup=keyboard()
        )
    except Exception as e:
        logger.error(f"ᴢɪᴘ ʜᴀɴᴅʟᴇʀ ᴇʀʀᴏʀ: {e}")
    
    logger.info("sᴛᴀʀᴛɪɴɢ ᴢɪᴘ ᴄᴏᴍᴘʀᴇssɪᴏɴ...")
    BotTimes.current_time = time()
    
    if not ospath.exists(Paths.temp_zpath):
        makedirs(Paths.temp_zpath)
    
    await archive(down_path, is_split, remove)
    await sleep(2)
    
    Transfer.total_down_size = getSize(Paths.temp_zpath)
    
    if remove and ospath.exists(down_path):
        shutil.rmtree(down_path)


# =============================================================================
#  ᴜɴᴢɪᴘ ʜᴀɴᴅʟᴇʀ
# =============================================================================
async def Unzip_Handler(down_path: str, remove: bool):
    """
    ʜᴀɴᴅʟᴇ ᴇxᴛʀᴀᴄᴛɪᴏɴ ᴏғ ᴀʀᴄʜɪᴠᴇ ғɪʟᴇs.
    
    ᴀʀɢs:
        ᴅᴏᴡɴ_ᴘᴀᴛʜ: ᴘᴀᴛʜ ᴄᴏɴᴛᴀɪɴɪɴɢ ᴀʀᴄʜɪᴠᴇs
        ʀᴇᴍᴏᴠᴇ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀʀᴄʜɪᴠᴇs ᴀғᴛᴇʀ ᴇxᴛʀᴀᴄᴛɪᴏɴ
    """
    global MSG, Messages
    
    Messages.status_head = f"\n**📂 ᴇxᴛʀᴀᴄᴛɪɴɢ**\n\n`{Messages.download_name}`\n"
    
    MSG.status_msg = await MSG.status_msg.edit_text(
        text=Messages.task_msg + Messages.status_head + "\n⏳ `sᴛᴀʀᴛɪɴɢ...`" + sysINFO(),
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
            logger.error(f"ᴜɴᴢɪᴘ ʜᴀɴᴅʟᴇʀ ᴇʀʀᴏʀ: {e}")
    
    if remove:
        shutil.rmtree(down_path)


# =============================================================================
#  ᴛᴀsᴋ ᴄᴀɴᴄᴇʟʟᴀᴛɪᴏɴ
# =============================================================================
async def cancelTask(reason: str):
    """
    ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ʀᴜɴɴɪɴɢ ᴛᴀsᴋ.
    
    ᴀʀɢs:
        ʀᴇᴀsᴏɴ: ᴄᴀɴᴄᴇʟʟᴀᴛɪᴏɴ ʀᴇᴀsᴏɴ
    """
    text = f"""**❌ ᴛᴀsᴋ ᴄᴀɴᴄᴇʟʟᴇᴅ**

╭🔗 **sᴏᴜʀᴄᴇ:** [ʜᴇʀᴇ]({Messages.src_link})
├🎯 **ᴍᴏᴅᴇ:** `{BOT.Mode.mode.capitalize()}`
├⚠️ **ʀᴇᴀsᴏɴ:** `{reason}`
╰⏱️ **ᴇʟᴀᴘsᴇᴅ:** `{getTime((datetime.now() - BotTimes.start_time).seconds)}`"""
    
    if BOT.State.task_going:
        try:
            BOT.TASK.cancel()
            shutil.rmtree(Paths.WORK_PATH)
        except Exception as e:
            logger.error(f"ᴛᴀsᴋ ᴄᴀɴᴄᴇʟʟᴀᴛɪᴏɴ ᴇʀʀᴏʀ: {e}")
        else:
            logger.info("ᴛᴀsᴋ ᴄᴀɴᴄᴇʟʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ")
        finally:
            BOT.State.task_going = False
            await MSG.status_msg.delete()
            await leechbot.send_message(
                chat_id=OWNER,
                text=text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📣 ᴄʜᴀɴɴᴇʟ", url="https://t.me/Shineii86"),
                            InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url="https://t.me/Shineii86"),
                        ]
                    ]
                )
            )


# =============================================================================
#  ᴄᴏᴍᴘʟᴇᴛɪᴏɴ ʟᴏɢs
# =============================================================================
async def SendLogs(is_leech: bool):
    """
    sᴇɴᴅ ᴄᴏᴍᴘʟᴇᴛɪᴏɴ ʟᴏɢs ᴀɴᴅ sᴜᴍᴍᴀʀʏ.
    
    ᴀʀɢs:
        ɪs_ʟᴇᴇᴄʜ: ᴡʜᴇᴛʜᴇʀ ᴛʜɪs ᴡᴀs ᴀ ʟᴇᴇᴄʜ ᴛᴀsᴋ
    """
    global Transfer, Messages
    
    final_text = f"**📋 ғɪʟᴇ ʟɪsᴛ:** `{len(Transfer.sent_file)}`\n\n**📜 ʟᴏɢs:**\n"
    
    if is_leech:
        file_count = f"├📋 **ғɪʟᴇs:** `{len(Transfer.sent_file)}`\n"
        size = sizeUnit(sum(Transfer.up_bytes))
    else:
        file_count = ""
        size = sizeUnit(Transfer.total_down_size)
    
    summary = f"""

**✅ ᴛᴀsᴋ ᴄᴏᴍᴘʟᴇᴛᴇ**

╭📛 **ɴᴀᴍᴇ:** `{Messages.download_name}`
├📦 **sɪᴢᴇ:** `{size}`
{file_count}├⏱️ **ᴛɪᴍᴇ:** `{getTime((datetime.now() - BotTimes.start_time).seconds)}`
╰👤 **ʙʏ:** @sʜɪɴᴇɪɪ86"""
    
    if BOT.State.task_going:
        await MSG.sent_msg.reply_text(
            text=f"**🔗 sᴏᴜʀᴄᴇ:** [ʜᴇʀᴇ]({Messages.src_link})" + summary
        )
        
        await MSG.status_msg.edit_text(
            text=Messages.task_msg + summary,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("📣 ᴄʜᴀɴɴᴇʟ", url="https://t.me/Shineii86"),
                        InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url="https://t.me/Shineii86"),
                    ],
                    [
                        InlineKeyboardButton("📂 ɢɪᴛʜᴜʙ", url="https://github.com/Shineii86/LeechBot"),
                    ]
                ]
            )
        )
        
        # sᴇɴᴅ ғɪʟᴇ ʟɪsᴛ ɪғ ʟᴇᴇᴄʜ ᴛᴀsᴋ
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
                error_msg = f"**❌ ʟᴏɢ ᴇʀʀᴏʀ:** `{e}`"
                await MSG.status_msg.reply_text(text=error_msg)
    
    BOT.State.started = False
    BOT.State.task_going = False
