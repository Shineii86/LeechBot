# =============================================================================
# Telegram Leech Bot - Central Configuration
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================
# License   : MIT License
# =============================================================================

"""
Central configuration module.

All settings are loaded from environment variables with sensible defaults.
Create a .env file in the project root to override defaults.
"""

import os
import logging
import warnings
from pathlib import Path

# Suppress harmless moviepy/ALSA SyntaxWarnings in Colab
warnings.filterwarnings("ignore", category=SyntaxWarning, module="moviepy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv is optional; env vars still work

logger = logging.getLogger(__name__)

# =============================================================================
# Base Paths (configurable via LEECHBOT_BASE_DIR env var)
# =============================================================================
# Detect Colab environment and set appropriate base dir
_default_base = "/tmp/leechbot"
if os.path.exists("/content"):
    _default_base = "/content/leechbot/BOT_WORK"

BASE_DIR = Path(os.getenv("LEECHBOT_BASE_DIR", _default_base))
WORK_PATH = BASE_DIR / "work"
DOWNLOADS_PATH = WORK_PATH / "downloads"
TEMP_PATH = BASE_DIR / "temp"
THUMBNAIL_PATH = BASE_DIR / "thumbnails"
SESSIONS_PATH = BASE_DIR / "sessions"
LOGS_PATH = BASE_DIR / "logs"

# Create all directories on import
for _p in [WORK_PATH, DOWNLOADS_PATH, TEMP_PATH, THUMBNAIL_PATH, SESSIONS_PATH, LOGS_PATH]:
    _p.mkdir(parents=True, exist_ok=True)

# =============================================================================
# Telegram Credentials
# Priority: 1) Env vars  2) .env file  3) credentials.json
# =============================================================================
def _load_credentials_json() -> dict:
    """Fallback: load from credentials.json (used by Colab notebook)."""
    for path in ["credentials.json", "/content/leechbot/credentials.json", "/content/tgdl/credentials.json"]:
        if os.path.exists(path):
            try:
                import json
                with open(path, "r") as f:
                    data = json.load(f)
                logger.info("Loaded credentials from %s", path)
                return data
            except Exception as e:
                logger.warning("Failed to load %s: %s", path, e)
    return {}

_creds = _load_credentials_json()

API_ID = int(os.getenv("API_ID", "0") or _creds.get("API_ID", 0))
API_HASH = os.getenv("API_HASH", "") or _creds.get("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "") or _creds.get("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0") or _creds.get("USER_ID", 0))
DUMP_ID = int(os.getenv("DUMP_ID", "0") or _creds.get("DUMP_ID", 0))

# Auto-format DUMP_ID if needed
if DUMP_ID and len(str(abs(DUMP_ID))) == 10 and not str(DUMP_ID).startswith("-100"):
    DUMP_ID = int(f"-100{DUMP_ID}")

# Validate critical credentials
if not API_ID or not API_HASH or not BOT_TOKEN:
    logger.warning(
        "API_ID, API_HASH, or BOT_TOKEN not set. "
        "Set them in .env, environment variables, or credentials.json."
    )

# =============================================================================
# Feature Flags & Limits
# =============================================================================
# Feature Flags & Limits
# =============================================================================
MAX_FILE_SIZE = 2097152000  # 2GB Telegram limit
MAX_VIDEO_SPLIT_SIZE = 1992294400  # 1.9GB for safe splitting
AUTO_RETRY_COUNT = int(os.getenv("AUTO_RETRY_COUNT", "3"))
DEFAULT_UPLOAD_MODE = os.getenv("DEFAULT_UPLOAD_MODE", "media")  # media or document
BANDWIDTH_LIMIT = os.getenv("BANDWIDTH_LIMIT", "")  # e.g., "10M" for aria2c
WEB_PORT = int(os.getenv("WEB_PORT", "8080"))
WEB_TOKEN = os.getenv("WEB_TOKEN", "")

# =============================================================================
# Google Drive
# =============================================================================
TOKEN_PICKLE_PATH = os.getenv("TOKEN_PICKLE_PATH", str(BASE_DIR / "token.pickle"))

# =============================================================================
# YT-DLP Cookie Authentication
# =============================================================================
# Option 1: Path to a Netscape-format cookies.txt file
#   Export from your browser using a cookies editor extension.
#   Set env: YTDL_COOKIES_FILE=/path/to/cookies.txt
YTDL_COOKIES_FILE = os.getenv("YTDL_COOKIES_FILE", "")

# =============================================================================
# Multi-User Support
# =============================================================================
ALLOWED_USERS = [
    int(x.strip())
    for x in os.getenv("ALLOWED_USERS", "").split(",")
    if x.strip()
]

# =============================================================================
# Version Info
# =============================================================================
VERSION = "3.3.0"
BUILD_DATE = "2026-06-30"
