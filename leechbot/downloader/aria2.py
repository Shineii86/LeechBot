# =============================================================================
# Telegram Leech Bot - Aria2c Downloader
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
Aria2c downloader module.

Handles downloads using aria2c, including HTTP/HTTPS links, torrents, and magnet links.
Provides real-time progress updates.
"""

import re
import logging
import subprocess
import os
from datetime import datetime
from leechbot.utility.helper import sizeUnit, status_bar
from leechbot.utility.variables import BOT, Aria2c, Paths, Messages, BotTimes

logger = logging.getLogger(__name__)

ARIA2_DIR = os.path.expanduser("~/.aria2")
TRACKER_FILES = [
    ("best_aria2.txt", "https://cf.trackerslist.com/best_aria2.txt"),
    ("all_aria2.txt", "https://cf.trackerslist.com/all_aria2.txt"),
    ("http_aria2.txt", "https://cf.trackerslist.com/http_aria2.txt"),
    ("nohttp_aria2.txt", "https://cf.trackerslist.com/nohttp_aria2.txt"),
]

os.makedirs(ARIA2_DIR, exist_ok=True)
trackers = []
for fname, url in TRACKER_FILES:
    fpath = os.path.join(ARIA2_DIR, fname)
    if not os.path.exists(fpath):
        subprocess.run(["wget", "-q", "-O", fpath, url])
    try:
        with open(fpath, "r") as f:
            trackers.append(f.read().replace("\n", ","))
    except Exception:
        pass
TRACKER_STRING = ",".join(trackers)

def is_torrent_or_magnet(link: str) -> bool:
    return link.endswith(".torrent") or link.startswith("magnet:")

def parse_link_options(link: str):
    import shlex
    parts = shlex.split(link)
    url = None
    headers = []
    out = None
    i = 0
    while i < len(parts):
        part = parts[i]
        if part == "--header" and i + 1 < len(parts):
            headers.append(parts[i + 1])
            i += 2
        elif part == "--out" and i + 1 < len(parts):
            out = parts[i + 1]
            i += 2
        elif part.startswith("--"):
            i += 1
        else:
            if url is None:
                url = part
            i += 1
    return url, headers, out

async def aria2_Download(link: str, num: int, resume: bool = False):
    global BotTimes, Messages
    url, headers, out = parse_link_options(link)
    if url is None:
        logger.error("No valid URL found in link")
        return
    name_d = get_Aria2c_Name(url if out is None else out)
    BotTimes.task_start = datetime.now()
    Messages.status_head = f"**📥 Downloading** `Link {str(num).zfill(2)}`\n\n**🏷️ Name:** `{name_d}`\n"
    command = []
    if is_torrent_or_magnet(url):
        command = [
            "aria2c", "--enable-dht=true", "--enable-peer-exchange=true", "--bt-enable-lpd=true",
            "--bt-max-peers=100", "--bt-request-peer-speed-limit=0", "--bt-tracker-connect-timeout=10",
            "--bt-tracker-interval=60", "--bt-tracker-timeout=10", "--max-connection-per-server=16",
            "--max-concurrent-downloads=5", "--seed-time=0", "--summary-interval=1",
            "--console-log-level=notice", f"--bt-tracker={TRACKER_STRING}", "-d", Paths.down_path,
        ]
    else:
        command = [
            "aria2c", "-x16", "-s16", "--seed-time=0", "--summary-interval=1", "--max-tries=3",
            "--console-log-level=notice", "--optimize-concurrent-downloads=true", "--file-allocation=prealloc",
            "-d", Paths.down_path,
        ]
    # Session management
    if resume and os.path.exists(Paths.ARIA2_SESSION):
        command += ["--input-file", Paths.ARIA2_SESSION]
    command += ["--save-session", Paths.ARIA2_SESSION]
    # Speed limit
    if BOT.Setting.download_speed_limit > 0:
        limit_k = int(BOT.Setting.download_speed_limit / 1024)
        command += [f"--max-overall-download-limit={limit_k}K"]
    for h in headers:
        command += ["--header", h]
    if out:
        command += ["-o", out]
    command.append(url)
    logger.info(f"Aria2c command: {' '.join(command)}")
    proc = subprocess.Popen(command, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = proc.stdout.readline()
        if output == b"" and proc.poll() is not None:
            break
        if output:
            await on_output(output.decode("utf-8"))
    exit_code = proc.wait()
    error_output = proc.stderr.read()
    if exit_code != 0:
        logger.error(f"Aria2c stderr: {error_output.decode('utf-8').strip()}")
        if exit_code == 3:
            logger.error(f"Resource not found: {link}")
        elif exit_code == 9:
            logger.error("Insufficient disk space")
        elif exit_code == 24:
            logger.error("HTTP authorization failed")
        else:
            logger.error(f"Aria2c failed with code {exit_code}")
    # Clear session on success
    if exit_code == 0 and os.path.exists(Paths.ARIA2_SESSION):
        os.remove(Paths.ARIA2_SESSION)

def get_Aria2c_Name(link: str) -> str:
    if BOT.Options.custom_name:
        return BOT.Options.custom_name
    cmd = f'aria2c -x10 --dry-run --file-allocation=none "{link}"'
    result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    stdout_str = result.stdout.decode("utf-8")
    try:
        filename = stdout_str.split("complete: ")[-1].split("\n")[0]
        name = filename.split("/")[-1]
    except Exception:
        name = "Unknown"
    return name if name else "Unknown"

async def on_output(output: str):
    if not hasattr(Aria2c, "link_info"):
        Aria2c.link_info = False
    total_size = "0B"
    progress_percentage = "0B"
    downloaded_bytes = "0B"
    eta = "0s"
    try:
        if "ETA:" in output:
            parts = output.split()
            total_size = parts[1].split("/")[1].split("(")[0]
            progress_percentage = parts[1][parts[1].find("(") + 1:parts[1].find(")")]
            downloaded_bytes = parts[1].split("/")[0]
            eta = parts[4].split(":")[1][:-1]
    except Exception as e:
        logger.error(f"Parsing error: {e}")
    try:
        percentage = float(re.findall(r"\d+\.\d+|\d+", progress_percentage)[0])
    except Exception:
        percentage = 0
    try:
        down = float(re.findall(r"\d+\.\d+|\d+", downloaded_bytes)[0])
        down_unit = re.findall(r"[a-zA-Z]+", downloaded_bytes)[0]
    except Exception:
        down, down_unit = 0, "B"
    spd_map = {"G": 3, "M": 2, "K": 1}
    spd = spd_map.get(down_unit[0], 0) if down_unit else 0
    elapsed = (datetime.now() - BotTimes.task_start).seconds
    if elapsed >= 270 and not Aria2c.link_info:
        logger.error("Failed to get download info - possible dead link")
    if total_size != "0B":
        Aria2c.link_info = True
        current_speed = (down * (1024 ** spd)) / max(elapsed, 1)
        speed_string = f"{sizeUnit(current_speed)}/s"
        await status_bar(Messages.status_head, speed_string, int(percentage), eta, downloaded_bytes, total_size, "Aria2c ⚡")
