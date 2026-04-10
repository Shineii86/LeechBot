# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ʟᴇᴇᴄʜʙᴏᴛ ᴛᴀsᴋ ᴍᴀɴᴀɢᴇʀ

ᴛʜɪs ᴍᴏᴅᴜʟᴇ ᴏʀᴄʜᴇsᴛʀᴀᴛᴇs ᴛʜᴇ ᴇɴᴛɪʀᴇ ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴡᴏʀᴋғʟᴏᴡ.
ɪᴛ ʜᴀɴᴅʟᴇs ᴛᴀsᴋ ɪɴɪᴛɪᴀʟɪᴢᴀᴛɪᴏɴ, sᴄʜᴇᴅᴜʟɪɴɢ, ᴀɴᴅ ᴇxᴇᴄᴜᴛɪᴏɴ.
"""

import pytz
import shutil
import logging
from time import time
from datetime import datetime
from asyncio import sleep
from os import makedirs, path as ospath, system
from leechbot import OWNER, leechbot, DUMP_ID
from leechbot.downloader.manager import calDownSize, get_d_name, downloadManager
from leechbot.utility.helper import getSize, applyCustomName, keyboard, sysINFO, is_google_drive, is_telegram, is_ytdl_link, is_mega, is_terabox, is_torrent
from leechbot.utility.handler import Leech, Unzip_Handler, Zip_Handler, SendLogs, cancelTask
from leechbot.utility.variables import BOT, MSG, BotTimes, Messages, Paths, Aria2c, Transfer, TaskError

logger = logging.getLogger(__name__)


# =============================================================================
#  ᴛᴀsᴋ sᴛᴀʀᴛᴇʀ
# =============================================================================
async def task_starter(message, text: str):
    """
    ɪɴɪᴛɪᴀᴛᴇ ᴀ ɴᴇᴡ ᴛᴀsᴋ.
    
    ᴀʀɢs:
        ᴍᴇssᴀɢᴇ: ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇ ᴏʙᴊᴇᴄᴛ
        ᴛᴇxᴛ: ɪɴsᴛʀᴜᴄᴛɪᴏɴ ᴛᴇxᴛ ᴛᴏ sᴇɴᴅ
    
    ʀᴇᴛᴜʀɴs:
        ᴍᴇssᴀɢᴇ: ʀᴇǫᴜᴇsᴛ ᴍᴇssᴀɢᴇ ᴏʙᴊᴇᴄᴛ
    """
    global BOT
    
    await message.delete()
    BOT.State.started = True
    
    if not BOT.State.task_going:
        src_request_msg = await message.reply_text(text)
        return src_request_msg
    else:
        msg = await message.reply_text("**⏳ ɪ'ᴍ ᴀʟʀᴇᴀᴅʏ ᴡᴏʀᴋɪɴɢ! ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**")
        await sleep(15)
        await msg.delete()
        return None


# =============================================================================
#  ᴍᴀɪɴ ᴛᴀsᴋ sᴄʜᴇᴅᴜʟᴇʀ
# =============================================================================
async def taskScheduler():
    """
    ᴍᴀɪɴ ᴛᴀsᴋ sᴄʜᴇᴅᴜʟᴇʀ ᴛʜᴀᴛ ᴏʀᴄʜᴇsᴛʀᴀᴛᴇs ᴛʜᴇ ᴇɴᴛɪʀᴇ ᴡᴏʀᴋғʟᴏᴡ.
    """
    global BOT, MSG, BotTimes, Messages, Paths, Transfer, TaskError
    
    # ᴅᴇᴛᴇʀᴍɪɴᴇ ᴛᴀsᴋ ᴛʏᴘᴇ
    is_dualzip = BOT.Mode.type == "undzip"
    is_unzip = BOT.Mode.type == "unzip"
    is_zip = BOT.Mode.type == "zip"
    is_dir = BOT.Mode.mode == "dir-leech"
    
    # ʀᴇsᴇᴛ ᴍᴇssᴀɢᴇs
    Messages.download_name = ""
    Messages.task_msg = "**🎯 ᴛᴀsᴋ ᴍᴏᴅᴇ:** "
    Messages.dump_task = Messages.task_msg + f"`{BOT.Mode.type.capitalize()} {BOT.Mode.mode.capitalize()} as {BOT.Setting.stream_upload}`\n\n**🔗 sᴏᴜʀᴄᴇs:**"
    
    Transfer.sent_file = []
    Transfer.sent_file_names = []
    Transfer.down_bytes = [0, 0]
    Transfer.up_bytes = [0, 0]
    Messages.download_name = ""
    Messages.task_msg = ""
    Messages.status_head = "**📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ**\n"
    
    # ʜᴀɴᴅʟᴇ ᴅɪʀᴇᴄᴛᴏʀʏ ʟᴇᴇᴄʜ
    if is_dir:
        if not ospath.exists(BOT.SOURCE[0]):
            TaskError.state = True
            TaskError.text = "ᴅɪʀᴇᴄᴛᴏʀʏ ᴘᴀᴛʜ ᴅᴏᴇs ɴᴏᴛ ᴇxɪsᴛ"
            logger.error(TaskError.text)
            return
        
        if not ospath.exists(Paths.temp_dirleech_path):
            makedirs(Paths.temp_dirleech_path)
        
        Messages.dump_task += f"\n\n📂 `{BOT.SOURCE[0]}`"
        Transfer.total_down_size = getSize(BOT.SOURCE[0])
        Messages.download_name = ospath.basename(BOT.SOURCE[0])
    
    else:  # ʜᴀɴᴅʟᴇ ᴜʀʟ ʟɪsᴛ
        for link in BOT.SOURCE:
            if is_telegram(link):
                icon = "💬"
            elif is_google_drive(link):
                icon = "♻️"
            elif is_torrent(link):
                icon = "🧲"
                Messages.caution_msg = "\n\n⚠️ **ᴛᴏʀʀᴇɴᴛs ᴀʀᴇ ʀᴇsᴛʀɪᴄᴛᴇᴅ ɪɴ sᴏᴍᴇ ᴇɴᴠɪʀᴏɴᴍᴇɴᴛs**"
            elif is_ytdl_link(link):
                icon = "🏮"
            elif is_terabox(link):
                icon = "🍑"
            elif is_mega(link):
                icon = "💾"
            else:
                icon = "🔗"
            
            code_link = f"\n\n{icon} `{link}`"
            
            if len(Messages.dump_task + code_link) >= 4096:
                await MSG.sent_msg.reply_text(Messages.dump_task)
                Messages.dump_task = code_link
            else:
                Messages.dump_task += code_link
    
    # ᴀᴅᴅ ᴛɪᴍᴇsᴛᴀᴍᴘ
    cdt = datetime.now(pytz.timezone("Asia/Kolkata"))
    dt = cdt.strftime(" %d-%m-%Y")
    Messages.dump_task += f"\n\n**📅 ᴅᴀᴛᴇ:** `{dt}`"
    
    # ᴄʀᴇᴀᴛᴇ ᴡᴏʀᴋɪɴɢ ᴅɪʀᴇᴄᴛᴏʀɪᴇs
    if ospath.exists(Paths.WORK_PATH):
        shutil.rmtree(Paths.WORK_PATH)
        makedirs(Paths.down_path)
    else:
        makedirs(Paths.WORK_PATH)
        makedirs(Paths.down_path)
    
    Messages.link_p = str(DUMP_ID)[4:]
    
    # ᴅᴏᴡɴʟᴏᴀᴅ ʜᴇʀᴏ ɪᴍᴀɢᴇ
    try:
        system(f"aria2c -d {Paths.WORK_PATH} -o Hero.jpg {Aria2c.pic_dwn_url}")
    except Exception:
        Paths.HERO_IMAGE = Paths.DEFAULT_HERO
    
    # sᴇɴᴅ ᴛᴀsᴋ ʟᴏɢ
    MSG.sent_msg = await leechbot.send_message(chat_id=DUMP_ID, text=Messages.dump_task)
    Messages.src_link = f"https://t.me/c/{Messages.link_p}/{MSG.sent_msg.id}"
    Messages.task_msg += f"[{BOT.Mode.type.capitalize()} {BOT.Mode.mode.capitalize()} as {BOT.Setting.stream_upload}]({Messages.src_link})\n\n"
    
    # ᴜᴘᴅᴀᴛᴇ sᴛᴀᴛᴜs ᴍᴇssᴀɢᴇ
    await MSG.status_msg.delete()
    img = Paths.THMB_PATH if ospath.exists(Paths.THMB_PATH) else Paths.HERO_IMAGE
    MSG.status_msg = await leechbot.send_photo(
        chat_id=OWNER,
        photo=img,
        caption=Messages.task_msg + Messages.status_head + "\n📝 `ɪɴɪᴛɪᴀʟɪᴢɪɴɢ...`" + sysINFO(),
        reply_markup=keyboard()
    )
    
    # ᴄᴀʟᴄᴜʟᴀᴛᴇ ᴛᴏᴛᴀʟ ᴅᴏᴡɴʟᴏᴀᴅ sɪᴢᴇ
    await calDownSize(BOT.SOURCE)
    
    # ɢᴇᴛ ᴅᴏᴡɴʟᴏᴀᴅ ɴᴀᴍᴇ
    if not is_dir:
        await get_d_name(BOT.SOURCE[0])
    else:
        Messages.download_name = ospath.basename(BOT.SOURCE[0])
    
    # ᴘʀᴇᴘᴀʀᴇ ᴢɪᴘ ᴘᴀᴛʜ ɪғ ɴᴇᴇᴅᴇᴅ
    if is_zip:
        Paths.down_path = ospath.join(Paths.down_path, Messages.download_name)
        if not ospath.exists(Paths.down_path):
            makedirs(Paths.down_path)
    
    BotTimes.current_time = time()
    
    # ᴇxᴇᴄᴜᴛᴇ ᴛᴀsᴋ
    if BOT.Mode.mode != "mirror":
        await Do_Leech(BOT.SOURCE, is_dir, BOT.Mode.ytdl, is_zip, is_unzip, is_dualzip)
    else:
        await Do_Mirror(BOT.SOURCE, BOT.Mode.ytdl, is_zip, is_unzip, is_dualzip)


# =============================================================================
#  ʟᴇᴇᴄʜ ᴇxᴇᴄᴜᴛɪᴏɴ
# =============================================================================
async def Do_Leech(source, is_dir: bool, is_ytdl: bool, is_zip: bool, is_unzip: bool, is_dualzip: bool):
    """
    ᴇxᴇᴄᴜᴛᴇ ʟᴇᴇᴄʜ ᴛᴀsᴋ.
    
    ᴀʀɢs:
        sᴏᴜʀᴄᴇ: ʟɪsᴛ ᴏғ sᴏᴜʀᴄᴇ ʟɪɴᴋs ᴏʀ ᴘᴀᴛʜs
        ɪs_ᴅɪʀ: ᴡʜᴇᴛʜᴇʀ ɪᴛ's ᴀ ᴅɪʀᴇᴄᴛᴏʀʏ ʟᴇᴇᴄʜ
        ɪs_ʏᴛᴅʟ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ᴜsᴇ ʏᴛ-ᴅʟᴘ
        ɪs_ᴢɪᴘ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ᴢɪᴘ ᴏᴜᴛᴘᴜᴛ
        ɪs_ᴜɴᴢɪᴘ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ᴇxᴛʀᴀᴄᴛ ᴀʀᴄʜɪᴠᴇs
        ɪs_ᴅᴜᴀʟᴢɪᴘ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ᴇxᴛʀᴀᴄᴛ ᴛʜᴇɴ ᴢɪᴘ
    """
    if is_dir:
        for s in source:
            if not ospath.exists(s):
                logger.error("ᴅɪʀᴇᴄᴛᴏʀʏ ᴅᴏᴇs ɴᴏᴛ ᴇxɪsᴛ")
                await cancelTask("ᴅɪʀᴇᴄᴛᴏʀʏ ᴅᴏᴇs ɴᴏᴛ ᴇxɪsᴛ")
                return
            
            Paths.down_path = s
            
            if is_zip:
                await Zip_Handler(Paths.down_path, True, False)
                await Leech(Paths.temp_zpath, True)
            elif is_unzip:
                await Unzip_Handler(Paths.down_path, False)
                await Leech(Paths.temp_unzip_path, True)
            elif is_dualzip:
                await Unzip_Handler(Paths.down_path, False)
                await Zip_Handler(Paths.temp_unzip_path, True, True)
                await Leech(Paths.temp_zpath, True)
            else:
                if ospath.isdir(s):
                    await Leech(Paths.down_path, False)
                else:
                    Transfer.total_down_size = ospath.getsize(s)
                    makedirs(Paths.temp_dirleech_path)
                    shutil.copy(s, Paths.temp_dirleech_path)
                    Messages.download_name = ospath.basename(s)
                    await Leech(Paths.temp_dirleech_path, True)
    else:
        await downloadManager(source, is_ytdl)
        Transfer.total_down_size = getSize(Paths.down_path)
        applyCustomName()
        
        if is_zip:
            await Zip_Handler(Paths.down_path, True, True)
            await Leech(Paths.temp_zpath, True)
        elif is_unzip:
            await Unzip_Handler(Paths.down_path, True)
            await Leech(Paths.temp_unzip_path, True)
        elif is_dualzip:
            await Unzip_Handler(Paths.down_path, True)
            await Zip_Handler(Paths.temp_unzip_path, True, True)
            await Leech(Paths.temp_zpath, True)
        else:
            await Leech(Paths.down_path, True)
    
    await SendLogs(True)


# =============================================================================
#  ᴍɪʀʀᴏʀ ᴇxᴇᴄᴜᴛɪᴏɴ
# =============================================================================
async def Do_Mirror(source, is_ytdl: bool, is_zip: bool, is_unzip: bool, is_dualzip: bool):
    """
    ᴇxᴇᴄᴜᴛᴇ ᴍɪʀʀᴏʀ ᴛᴀsᴋ (ᴜᴘʟᴏᴀᴅ ᴛᴏ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ).
    
    ᴀʀɢs:
        sᴏᴜʀᴄᴇ: ʟɪsᴛ ᴏғ sᴏᴜʀᴄᴇ ʟɪɴᴋs
        ɪs_ʏᴛᴅʟ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ᴜsᴇ ʏᴛ-ᴅʟᴘ
        ɪs_ᴢɪᴘ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ᴢɪᴘ ᴏᴜᴛᴘᴜᴛ
        ɪs_ᴜɴᴢɪᴘ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ᴇxᴛʀᴀᴄᴛ ᴀʀᴄʜɪᴠᴇs
        ɪs_ᴅᴜᴀʟᴢɪᴘ: ᴡʜᴇᴛʜᴇʀ ᴛᴏ ᴇxᴛʀᴀᴄᴛ ᴛʜᴇɴ ᴢɪᴘ
    """
    if not ospath.exists(Paths.MOUNTED_DRIVE):
        await cancelTask("ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ ɪs ɴᴏᴛ ᴍᴏᴜɴᴛᴇᴅ")
        return
    
    if not ospath.exists(Paths.mirror_dir):
        makedirs(Paths.mirror_dir)
    
    await downloadManager(source, is_ytdl)
    Transfer.total_down_size = getSize(Paths.down_path)
    applyCustomName()
    
    if is_zip:
        await Zip_Handler(Paths.down_path, True, True)
        shutil.copytree(Paths.temp_zpath, Paths.mirror_dir, dirs_exist_ok=True)
    elif is_unzip:
        await Unzip_Handler(Paths.down_path, True)
        shutil.copytree(Paths.temp_unzip_path, Paths.mirror_dir, dirs_exist_ok=True)
    elif is_dualzip:
        await Unzip_Handler(Paths.down_path, True)
        await Zip_Handler(Paths.temp_unzip_path, True, True)
        shutil.copytree(Paths.temp_zpath, Paths.mirror_dir, dirs_exist_ok=True)
    else:
        shutil.copytree(Paths.down_path, Paths.mirror_dir, dirs_exist_ok=True)
    
    await SendLogs(False)
