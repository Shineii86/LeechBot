# =============================================================================
# LeechBot Pro - Aria2c Downloader
# =============================================================================
# Project   : LeechBot Pro v3.0
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://t.me/Shineii86
# =============================================================================

import re
import os
import logging
import subprocess
from datetime import datetime
from colab_leecher.utility.helper import format_size, update_status_bar
from colab_leecher.utility.variables import BOT, Aria2c, Paths, Messages, BotTimes

# =============================================================================
# TRACKER SETUP
# =============================================================================
ARIA2_DIR = os.path.expanduser("~/.aria2")
TRACKER_SOURCES = [
    ("best_aria2.txt", "https://cf.trackerslist.com/best_aria2.txt"),
    ("all_aria2.txt", "https://cf.trackerslist.com/all_aria2.txt"),
    ("http_aria2.txt", "https://cf.trackerslist.com/http_aria2.txt"),
]

# Initialize trackers
os.makedirs(ARIA2_DIR, exist_ok=True)
all_trackers = []

for fname, url in TRACKER_SOURCES:
    fpath = os.path.join(ARIA2_DIR, fname)
    if not os.path.exists(fpath):
        try:
            subprocess.run(["wget", "-q", "-O", fpath, url], check=False)
        except Exception:
            pass
    try:
        with open(fpath, "r") as f:
            all_trackers.append(f.read().strip().replace('\n', ','))
    except Exception:
        pass

TRACKER_STRING = ",".join(filter(None, all_trackers))


# =============================================================================
# LINK PARSING
# =============================================================================
def is_torrent_or_magnet(link: str) -> bool:
    """Check if link is a torrent file or magnet link."""
    return link.endswith(".torrent") or link.startswith("magnet:")


def parse_link_options(link: str) -> tuple:
    """
    Parse download link for custom options.
    
    Supports:
        --header "Header-Name: Value"
        --out "custom_filename.ext"
    
    Args:
        link: Download link with optional parameters
        
    Returns:
        tuple: (url, headers_list, output_filename)
    """
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


# =============================================================================
# MAIN DOWNLOAD FUNCTION
# =============================================================================
async def aria2_download(link: str, num: int):
    """
    Download file using aria2c.
    
    Args:
        link: Download URL
        num: Download number for display
    """
    BotTimes.task_start = datetime.now()
    
    # Parse link options
    url, headers, out = parse_link_options(link)
    if not url:
        logging.error("No valid URL found in link")
        return
    
    # Get display name
    name = out if out else get_aria2_name(url)
    Messages.status_head = f"<b>📥 DOWNLOADING</b> <code>Link {num:02d}</code>\n\n<b>🏷️ Name:</b> <code>{name}</code>\n"
    
    # Build command
    if is_torrent_or_magnet(url):
        command = build_torrent_command(url, headers, out)
    else:
        command = build_http_command(url, headers, out)
    
    logging.info(f"Aria2c command: {' '.join(command)}")
    
    # Start download
    proc = subprocess.Popen(
        command,
        bufsize=0,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Process output
    while True:
        output = proc.stdout.readline()
        if output == "" and proc.poll() is not None:
            break
        if output:
            logging.debug(f"Aria2c: {output.strip()}")
            await process_output(output.strip())
    
    # Handle exit code
    exit_code = proc.wait()
    if exit_code != 0:
        stderr = proc.stderr.read()
        logging.error(f"Aria2c failed with code {exit_code}: {stderr}")
        handle_exit_code(exit_code, link)


def build_torrent_command(url: str, headers: list, out: str = None) -> list:
    """Build aria2c command for torrent/magnet downloads."""
    cmd = [
        "aria2c",
        "--enable-dht=true",
        "--enable-peer-exchange=true",
        "--bt-enable-lpd=true",
        "--bt-max-peers=100",
        "--bt-request-peer-speed-limit=0",
        "--bt-tracker-connect-timeout=10",
        "--bt-tracker-interval=60",
        "--bt-tracker-timeout=10",
        "--max-connection-per-server=16",
        "--max-concurrent-downloads=5",
        "--seed-time=0",
        "--summary-interval=1",
        "--console-log-level=notice",
        f"--bt-tracker={TRACKER_STRING}",
        "-d", Paths.down_path,
    ]
    
    for h in headers:
        cmd.extend(["--header", h])
    if out:
        cmd.extend(["-o", out])
    cmd.append(url)
    
    return cmd


def build_http_command(url: str, headers: list, out: str = None) -> list:
    """Build aria2c command for HTTP downloads."""
    cmd = [
        "aria2c",
        "-x16", "-s10",
        "--seed-time=0",
        "--summary-interval=1",
        "--max-tries=3",
        "--console-log-level=notice",
        "-d", Paths.down_path,
    ]
    
    # Apply speed limit if set
    if BOT.Setting.speed_limit > 0:
        cmd.extend(["--max-download-limit", f"{BOT.Setting.speed_limit}K"])
    
    for h in headers:
        cmd.extend(["--header", h])
    if out:
        cmd.extend(["-o", out])
    cmd.append(url)
    
    return cmd


def handle_exit_code(code: int, link: str):
    """Handle aria2c exit codes."""
    errors = {
        3: "Resource not found",
        9: "Not enough disk space",
        13: "File already exists",
        24: "HTTP authorization failed",
    }
    error_msg = errors.get(code, f"Download failed with code {code}")
    logging.error(f"{error_msg} for {link}")


# =============================================================================
# OUTPUT PROCESSING
# =============================================================================
async def process_output(output: str):
    """
    Parse aria2c output and update status.
    
    Args:
        output: Line of aria2c output
    """
    if "ETA:" not in output:
        return
    
    try:
        parts = output.split()
        total = parts[1].split("/")[1].split("(")[0].strip()
        percent = parts[1][parts[1].find("(") + 1:parts[1].find(")")]
        downloaded = parts[1].split("/")[0].strip()
        eta = parts[4].split(":")[1].strip() if len(parts) > 4 else "N/A"
        
        # Parse percentage
        percent_val = float(re.findall(r"[\d.]+", percent)[0]) if re.findall(r"[\d.]+", percent) else 0
        
        # Parse downloaded size
        down_val = re.findall(r"[\d.]+", downloaded)[0] if re.findall(r"[\d.]+", downloaded) else "0"
        down_unit = re.findall(r"[KMGT]?i?B", downloaded)[0] if re.findall(r"[KMGT]?i?B", downloaded) else "B"
        
        # Convert to bytes for speed calculation
        unit_multipliers = {"B": 0, "KiB": 1, "MiB": 2, "GiB": 3, "TiB": 4}
        multiplier = unit_multipliers.get(down_unit, 0)
        down_bytes = float(down_val) * (1024 ** multiplier)
        
        # Calculate speed
        elapsed = (datetime.now() - BotTimes.task_start).seconds
        if elapsed > 0 and down_bytes > 0:
            speed = down_bytes / elapsed
            speed_str = f"{format_size(speed)}/s"
        else:
            speed_str = "N/A"
        
        Aria2c.link_info = True
        
        await update_status_bar(
            Messages.status_head,
            speed_str,
            percent_val,
            eta,
            downloaded,
            total,
            "Aria2c 🚀",
        )
        
    except Exception as e:
        logging.debug(f"Output parse error: {e}")


# =============================================================================
# GET DOWNLOAD NAME
# =============================================================================
def get_aria2_name(link: str) -> str:
    """
    Get filename from URL using aria2c dry-run.
    
    Args:
        link: Download URL
        
    Returns:
        str: Filename or "Unknown"
    """
    if BOT.Options.custom_name:
        return BOT.Options.custom_name
    
    try:
        cmd = f'aria2c -x4 --dry-run --file-allocation=none "{link}"'
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                               shell=True, text=True, timeout=10)
        
        if "complete:" in result.stdout:
            filename = result.stdout.split("complete:")[-1].split("\n")[0].strip()
            name = filename.split("/")[-1]
            return name if name else "Unknown Download"
        
        # Try to extract from URL
        from urllib.parse import urlparse, unquote
        parsed = urlparse(link)
        path = unquote(parsed.path)
        name = path.split("/")[-1]
        return name if name and "." in name else "Unknown Download"
        
    except Exception as e:
        logging.error(f"Get name error: {e}")
        return "Unknown Download"
