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
import asyncio
import shutil
import logging
import pathlib
from asyncio import sleep
from time import time
from leechbot import OWNER, app
from natsort import natsorted
from datetime import datetime
from os import makedirs, path as ospath
from leechbot.uploader.telegram import upload_file, upload_photos_batch  # Added import
from pyrogram import types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from leechbot.utility.variables import BOT, MSG, BotTimes, Messages, Paths, Transfer
from leechbot.utility.converters import archive, extract, videoConverter, sizeChecker
from leechbot.utility.helper import fileType, getSize, getTime, keyboard, shortFileName, sizeUnit, sysINFO, _strip_sysinfo

logger = logging.getLogger(__name__)


# =============================================================================
# Auto-Rename Template
# =============================================================================
def _apply_autorename_template(original_name: str, template: str, metadata: dict = None) -> str:
    """
    Apply auto-rename template to a file name.

    Args:
        original_name: Original file name (with extension)
        template: Rename template with placeholders
        metadata: Optional metadata dict with keys like 'episode', 'season', 'quality', 'audio', 'title'

    Returns:
        New file name based on template

    Supported placeholders:
        {chapter} - Chapter number (auto-detected or from metadata)
        {season} - Season number (auto-detected or from metadata)
        {episode} - Episode number (auto-detected or from metadata)
        {quality} - Video quality (auto-detected or from metadata)
        {audio} - Audio info (auto-detected or from metadata)
        {title} - Title (from metadata only)
    """
    import re

    # Get file extension from original name
    _, ext = ospath.splitext(original_name)

    # If template already has an extension at the end, strip it
    if template.endswith(('.mkv', '.mp4', '.avi', '.webm', '.mov', '.flv')):
        template = template[:len(template) - len(ext)]

    # Start with metadata if provided, otherwise empty dict
    detected = {}
    if metadata:
        detected.update(metadata)

    # Auto-detect from filename (only if not already in metadata)
    # Detect chapter number (e.g., Ch.001, Chapter 1, c001, c12)
    if 'chapter' not in detected:
        chapter_match = re.search(r'(?:ch(?:apter)?[\s.]?|c)(\d+)', original_name, re.IGNORECASE)
        if chapter_match:
            detected['chapter'] = chapter_match.group(1).lstrip('0') or '0'

    # Detect season number (e.g., S01, Season 1, s01)
    if 'season' not in detected:
        season_match = re.search(r'(?:s(?:eason)?[\s.]?)(\d+)', original_name, re.IGNORECASE)
        if season_match:
            detected['season'] = season_match.group(1).lstrip('0') or '0'

    # Detect episode number (e.g., E01, Episode 1, ep01)
    if 'episode' not in detected:
        episode_match = re.search(r'(?:e(?:p(?:isode)?)?[\s.]?)(\d+)', original_name, re.IGNORECASE)
        if episode_match:
            detected['episode'] = episode_match.group(1).lstrip('0') or '0'

    # Detect quality (e.g., 1080p, 720p, 4K, 2160p)
    if 'quality' not in detected:
        quality_match = re.search(r'(\d{3,4}p|4k|2160p|1080p|720p|480p|360p)', original_name, re.IGNORECASE)
        if quality_match:
            detected['quality'] = quality_match.group(1).upper()

    # Detect audio info (e.g., AAC, FLAC, DTS, AC3, Dual Audio)
    if 'audio' not in detected:
        audio_match = re.search(r'(dual[\s-]?audio|aac|flac|dts|ac3|eac3|pcm|mp3|opus|7\.1|5\.1|2\.0|atmos)', original_name, re.IGNORECASE)
        if audio_match:
            detected['audio'] = audio_match.group(1).upper()

    # Replace placeholders in template with detected values
    result = template
    for key, value in detected.items():
        placeholder = '{' + key + '}'
        if placeholder in result:
            result = result.replace(placeholder, str(value))

    # Remove any remaining unreplaced placeholders
    result = re.sub(r'\{[^}]+\}', '', result)

    # Clean up multiple spaces and trailing/leading spaces
    result = re.sub(r'\s+', ' ', result).strip()

    # Add extension back
    if ext:
        result += ext

    return result


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
    from leechbot.utility.variables import BOT, BotTimes, Messages, Paths, Transfer

    # Get all files in folder
    files = [str(p) for p in pathlib.Path(folder_path).glob("**/*") if p.is_file()]

    # Convert videos if needed
    for f in natsorted(files):
        file_path = ospath.join(folder_path, f)
        if BOT.Options.convert_video and fileType(file_path) == "video":
            file_path = await videoConverter(file_path)

    Transfer.total_down_size = getSize(folder_path)

    # Refresh file list after possible conversions
    files = [str(p) for p in pathlib.Path(folder_path).glob("**/*") if p.is_file()]

    # Separate photos from other files
    photo_files = []
    other_files = []

    for f in natsorted(files):
        file_path = ospath.join(folder_path, f)
        if fileType(file_path) == "photo":
            photo_files.append(file_path)
        else:
            other_files.append(file_path)

    # Upload photos based on mode setting
    if photo_files:
        if BOT.Setting.photo_mode == "Group":
            # Group mode: batch upload in groups of 10 (Telegram limit)
            try:
                MSG.status_msg = await MSG.status_msg.edit_text(
                    text=_strip_sysinfo(Messages.task_msg) + "\n<b>📸 Uploading photos in batches...</b>" + sysINFO(),
                    reply_markup=keyboard()
                )
            except Exception as e:
                logger.error(f"Status update error: {e}")

            await upload_photos_batch(photo_files, remove=remove)
        else:
            # Single mode: upload each photo individually
            for idx, photo_path in enumerate(photo_files, 1):
                photo_name = ospath.basename(photo_path)
                BotTimes.current_time = time()
                Messages.status_head = f"<b>📸 Uploading photo</b> <code>{idx}/{len(photo_files)}</code>\n\n<code>{photo_name}</code>\n"

                try:
                    MSG.status_msg = await MSG.status_msg.edit_text(
                        text=_strip_sysinfo(Messages.task_msg + Messages.status_head) + "\n⏳ Starting..." + sysINFO(),
                        reply_markup=keyboard()
                    )
                except Exception as e:
                    logger.error(f"Status update error: {e}")

                await upload_file(photo_path, photo_name)
                Transfer.up_bytes.append(os.stat(photo_path).st_size)

                if remove and ospath.exists(photo_path):
                    os.remove(photo_path)

    # Process remaining files normally
    for file_path in other_files:
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
                try:
                    os.rename(short_path, new_path)
                except OSError as e:
                    logger.warning(f"Rename failed: {e}")

                BotTimes.current_time = time()
                Messages.status_head = f"<b>📤 Uploading Split</b> <code>{count}/{len(dir_list)}</code>\n\n<code>{file_name}</code>\n"

                try:
                    MSG.status_msg = await MSG.status_msg.edit_text(
                        text=_strip_sysinfo(Messages.task_msg + Messages.status_head) + "\n⏳ Starting..." + sysINFO(),
                        reply_markup=keyboard()
                    )
                except Exception as e:
                    logger.info(e)

                await upload_file(new_path, file_name)
                Transfer.up_bytes.append(os.stat(new_path).st_size)
                count += 1

            shutil.rmtree(Paths.temp_zpath, ignore_errors=True)

        else:  # Regular file upload
            if not ospath.exists(Paths.temp_files_dir):
                makedirs(Paths.temp_files_dir)

            if not remove:
                try:
                    file_path = shutil.copy(file_path, Paths.temp_files_dir)
                except (OSError, shutil.SameFileError) as e:
                    logger.warning(f"Copy failed, using original: {e}")

            file_name = ospath.basename(file_path)
            new_path = shortFileName(file_path)
            try:
                os.rename(file_path, new_path)
            except OSError as e:
                logger.warning(f"Rename failed: {e}")
                new_path = file_path

            BotTimes.current_time = time()
            Messages.status_head = f"<b>📤 Uploading</b>\n\n<code>{file_name}</code>\n"

            try:
                MSG.status_msg = await MSG.status_msg.edit_text(
                    text=_strip_sysinfo(Messages.task_msg + Messages.status_head) + "\n⏳ Starting..." + sysINFO(),
                    reply_markup=keyboard()
                )
            except Exception as e:
                logger.error(f"Status update error: {e}")

            file_size = os.stat(new_path).st_size
            await upload_file(new_path, file_name)
            Transfer.up_bytes.append(file_size)

            # Auto-screenshot: extract before cleanup while file still on disk
            if BOT.Setting.auto_screenshot and fileType(new_path) == "video":
                await send_auto_screenshots(new_path)

            if remove:
                if ospath.exists(new_path):
                    os.remove(new_path)
            else:
                for file in os.listdir(Paths.temp_files_dir):
                    try:
                        os.remove(ospath.join(Paths.temp_files_dir, file))
                    except OSError:
                        pass

    # Cleanup
    if remove and ospath.exists(folder_path):
        shutil.rmtree(folder_path, ignore_errors=True)
    if ospath.exists(Paths.thumbnail_ytdl):
        shutil.rmtree(Paths.thumbnail_ytdl, ignore_errors=True)
    if ospath.exists(Paths.temp_files_dir):
        shutil.rmtree(Paths.temp_files_dir, ignore_errors=True)

# =============================================================================
# Zip Handler (unchanged)
# =============================================================================
async def Zip_Handler(down_path: str, is_split: bool, remove: bool):
    """
    Handle zip compression of files.

    Args:
        down_path: path to file/folder to zip
        is_split: whether to split large archives
        remove: whether to remove original files
    """
    from leechbot.utility.variables import BOT, Messages, MSG, Transfer

    Messages.status_head = f"<b>🗜️ Zipping</b>\n\n<code>{Messages.download_name}</code>\n"

    try:
        MSG.status_msg = await MSG.status_msg.edit_text(
            text=_strip_sysinfo(Messages.task_msg + Messages.status_head) + sysINFO(),
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
        shutil.rmtree(down_path, ignore_errors=True)

# =============================================================================
# Unzip Handler (unchanged)
# =============================================================================
async def Unzip_Handler(down_path: str, remove: bool):
    """
    Handle extraction of archive files.

    Args:
        down_path: path containing archives
        remove: whether to remove archives after extraction
    """
    from leechbot.utility.variables import MSG, Messages

    Messages.status_head = f"\n<b>📂 Extracting</b>\n\n<code>{Messages.download_name}</code>\n"

    MSG.status_msg = await MSG.status_msg.edit_text(
        text=_strip_sysinfo(Messages.task_msg + Messages.status_head) + "\n⏳ Starting..." + sysINFO(),
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
        shutil.rmtree(down_path, ignore_errors=True)

# =============================================================================
# Task Cancellation (unchanged)
# =============================================================================
async def cancelTask(reason: str):
    """
    Cancel the current running task.

    Args:
        reason: cancellation reason
    """
    from leechbot.utility.variables import BOT, BotTimes, Messages, Paths, MSG

    elapsed = getTime(int((datetime.now() - BotTimes.start_time).total_seconds()))
    mode_label = BOT.Mode.mode.capitalize() if BOT.Mode.mode else "Unknown"

    src_line = f"• 🔗 <b>Source:</b> <a href=\"{Messages.src_link}\">Here</a>\n" if Messages.src_link else ""

    text = (
        f"🚫 <b>Task Cancelled</b>\n\n"
        f"{src_line}"
        f"• 🎯 <b>Mode:</b> <code>{mode_label}</code>\n"
        f"• ⚠️ <b>Reason:</b> <code>{reason}</code>\n"
        f"• ⏱️ <b>Elapsed:</b> <code>{elapsed}</code>"
    )

    if BOT.State.task_going:
        try:
            if BOT.TASK:
                BOT.TASK.cancel()
        except Exception as e:
            logger.error("Task cancel error: %s", e)

        try:
            shutil.rmtree(Paths.WORK_PATH, ignore_errors=True)
        except Exception as e:
            logger.warning("Cleanup error: %s", e)

        BOT.State.task_going = False
        logger.info("Task cancelled: %s", reason)

        # Clean up status message
        try:
            await MSG.status_msg.delete()
        except Exception:
            pass

        # Notify user
        try:
            await app.send_message(
                chat_id=OWNER,
                text=text,
                link_preview_options=types.LinkPreviewOptions(is_disabled=True),
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("📣 Channel", url="https://t.me/MaximXBots"),
                        InlineKeyboardButton("Support 💬", url="https://t.me/MaximXGroup"),
                    ]
                ]),
            )
        except Exception as e:
            logger.error("Failed to send cancel notification: %s", e)

# =============================================================================
# Auto-Screenshot After Upload
# =============================================================================
async def send_auto_screenshots(file_path: str):
    """Extract screenshots from uploaded video and send as media group to dump channel."""
    from leechbot.utility.variables import BOT, MSG, Paths

    if not BOT.Setting.auto_screenshot:
        return

    if fileType(file_path) != "video":
        return

    count = BOT.Setting.screenshot_count
    watermark = BOT.Setting.screenshot_watermark

    screenshots = []
    output_dir = Paths.temp_dirleech_path if ospath.exists(Paths.temp_dirleech_path) else "/tmp"
    base_name = ospath.splitext(ospath.basename(file_path))[0]

    try:
        # Get video duration
        probe_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        proc = await asyncio.create_subprocess_exec(
            *probe_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        duration = float(stdout.decode().strip()) if stdout else 60.0

        interval = duration / (count + 1)

        for i in range(1, count + 1):
            timestamp = interval * i
            output_path = ospath.join(output_dir, f"{base_name}_auto_ss_{i}.jpg")

            cmd = [
                "ffmpeg", "-y",
                "-ss", str(timestamp),
                "-i", file_path,
                "-vframes", "1",
                "-q:v", "2",
                output_path
            ]
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.communicate()

            if ospath.exists(output_path) and ospath.getsize(output_path) > 0:
                # Add watermark if set
                if watermark:
                    try:
                        from PIL import Image, ImageDraw, ImageFont
                        img = Image.open(output_path)
                        draw = ImageDraw.Draw(img)
                        try:
                            font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 36)
                        except (OSError, IOError):
                            font = ImageFont.load_default()
                        bbox = draw.textbbox((0, 0), watermark, font=font)
                        text_w = bbox[2] - bbox[0]
                        text_h = bbox[3] - bbox[1]
                        x = img.width - text_w - 20
                        y = img.height - text_h - 20
                        draw.text((x, y), watermark, fill="white", font=font)
                        img.save(output_path)
                    except Exception as e:
                        logger.warning(f"Watermark failed: {e}")

                screenshots.append(output_path)

        if screenshots and MSG.sent_msg:
            from leechbot import app
            from config import DUMP_ID
            media_group = [InputMediaPhoto(screenshot) for screenshot in screenshots]
            await app.send_media_group(chat_id=DUMP_ID, media=media_group)
            logger.info(f"Auto-sent {len(screenshots)} screenshots to dump channel")

    except Exception as e:
        logger.error(f"Auto-screenshot failed: {e}")
    finally:
        # Cleanup temp screenshots
        for ss in screenshots:
            try:
                if ospath.exists(ss):
                    os.remove(ss)
            except OSError:
                pass


# =============================================================================
# Completion Logs (unchanged)
# =============================================================================
async def SendLogs(is_leech: bool):
    """
    Send completion logs and summary.

    Args:
        is_leech: whether this was a leech task
    """
    from leechbot.utility.variables import BOT, BotTimes, Messages, MSG, Transfer
    import config

    elapsed_secs = (datetime.now() - BotTimes.start_time).total_seconds()
    elapsed = getTime(int(elapsed_secs))
    file_count_num = len(Transfer.sent_file) if is_leech else 0
    size = sizeUnit(sum(Transfer.up_bytes)) if is_leech else sizeUnit(Transfer.total_down_size)

    # Average speed
    total_bytes = sum(Transfer.up_bytes) if is_leech else Transfer.total_down_size
    avg_speed = sizeUnit(total_bytes / elapsed_secs) if elapsed_secs > 0 else "0 B"

    summary = (
        f"\n\n<b>✅ TASK COMPLETE</b>\n\n"
        f"📛 <b>Name:</b> <code>{Messages.download_name or 'Unknown'}</code>\n"
        f"📦 <b>Size:</b> <code>{size}</code>\n"
        f"{f'📋 <b>Files:</b> <code>{file_count_num}</code>\n' if is_leech else ''}"
        f"⚡ <b>Speed:</b> <code>{avg_speed}/s</code>\n"
        f"⏱️ <b>Time:</b> <code>{elapsed}</code>\n\n"
        f"🤖 <a href=\"https://github.com/Shineii86/LeechBot\">LeechBot</a> • v{config.VERSION}"
    )

    if not BOT.State.task_going:
        return

    # Send summary reply
    try:
        src_line = f"\n🔗 <b>Source:</b> <a href=\"{Messages.src_link}\">Here</a>" if Messages.src_link else ""
        await MSG.sent_msg.reply_text(text=src_line + summary)
    except Exception as e:
        logger.error("Failed to send source reply: %s", e)

    # Update status message
    try:
        await MSG.status_msg.edit_text(
            text=Messages.task_msg + summary,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("📣 Channel", url="https://t.me/MaximXBots"),
                    InlineKeyboardButton("Support 💬", url="https://t.me/MaximXGroup"),
                ],
                [
                    InlineKeyboardButton("📂 GitHub ✨", url="https://github.com/Shineii86/LeechBot"),
                ]
            ]),
        )
    except Exception as e:
        logger.error("Failed to update status message: %s", e)

    # Send file list if leech task
    if is_leech and Transfer.sent_file:
        final_text = f"<b>📋 FILES</b> » <code>{file_count_num}</code>\n\n"
        try:
            final_texts = []
            for i in range(len(Transfer.sent_file)):
                file_link = f"https://t.me/c/{Messages.link_p}/{Transfer.sent_file[i].id}"
                file_name = Transfer.sent_file_names[i] if i < len(Transfer.sent_file_names) else f"File {i+1}"
                file_text = f"\n({str(i+1).zfill(2)}) [{file_name}]({file_link})"

                if len(final_text + file_text) >= 4096:
                    final_texts.append(final_text)
                    final_text = file_text
                else:
                    final_text += file_text

            final_texts.append(final_text)

            for fn_txt in final_texts:
                MSG.status_msg = await MSG.status_msg.reply_text(text=fn_txt)

        except Exception as e:
            logger.error("File list send error: %s", e)
            try:
                await MSG.status_msg.reply_text(text=f"<b>❌ Log Error:</b> <code>{e}</code>")
            except Exception:
                pass

    BOT.State.started = False
    BOT.State.task_going = False
