# =============================================================================
# LeechBot Pro - Bot Module
# =============================================================================
# Project   : Telegram Leech Bot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

import os
import json
import logging
import asyncio
from pyrogram import Client

# =============================================================================
# LOGGING SETUP
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger("LeechBot")

# =============================================================================
# LOAD CREDENTIALS
# =============================================================================
def load_credentials():
    """Load credentials from environment or file."""
    # Try environment variables first
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    bot_token = os.environ.get("BOT_TOKEN")
    owner_id = os.environ.get("OWNER_ID")
    dump_id = os.environ.get("DUMP_ID")
    
    # Try credentials file if env vars not set
    if not all([api_id, api_hash, bot_token]):
        creds_paths = [
            "/content/leechbot/credentials.json",
            "credentials.json",
            "config/credentials.json",
        ]
        
        for path in creds_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        creds = json.load(f)
                        api_id = api_id or creds.get("API_ID")
                        api_hash = api_hash or creds.get("API_HASH")
                        bot_token = bot_token or creds.get("BOT_TOKEN")
                        owner_id = owner_id or creds.get("USER_ID") or creds.get("OWNER_ID")
                        dump_id = dump_id or creds.get("DUMP_ID")
                        break
                except Exception as e:
                    logger.error(f"Failed to load credentials from {path}: {e}")
    
    return api_id, api_hash, bot_token, owner_id, dump_id

# =============================================================================
# INITIALIZE CLIENT
# =============================================================================
API_ID, API_HASH, BOT_TOKEN, OWNER, DUMP_ID = load_credentials()

# Validate credentials
if not all([API_ID, API_HASH, BOT_TOKEN]):
    logger.error("Missing required credentials! Please set API_ID, API_HASH, and BOT_TOKEN")
    raise ValueError("Missing required credentials")

# Convert to proper types
API_ID = int(API_ID)
OWNER = int(OWNER) if OWNER else 0
DUMP_ID = int(DUMP_ID) if DUMP_ID else 0

# Fix DUMP_ID format
if DUMP_ID and len(str(DUMP_ID)) == 10 and not str(DUMP_ID).startswith("-100"):
    DUMP_ID = int("-100" + str(DUMP_ID))

# Ensure event loop
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Create client
colab_bot = Client(
    "leechbot_pro",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=100,
    parse_mode="html",
)

logger.info("LeechBot Pro initialized successfully!")
