# =============================================================================
# Telegram Leech Bot - Advanced Telegram File Transloder
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================
# License   : MIT License
# You may use, modify, and distribute this code under the MIT License.
# Please retain this header when using or modifying the code.
# =============================================================================

"""
LeechBot main module initialization

This module handles the pyrogram client initialization and configuration loading.
It sets up the bot instance with the required API credentials and logging.
"""

import asyncio
import logging
import json
import os
from pyrogram import Client

# =============================================================================
# Logging Configuration
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# =============================================================================
# Credentials Loading
# =============================================================================
def load_credentials():
    """
    Load bot credentials from the credentials.json file.
    
    Returns:
        dict: containing api_id, api_hash, bot_token, owner, and dump_id
    """
    credentials_path = "/content/tgdl/credentials.json"
    
    # Check if running in local mode
    if not os.path.exists(credentials_path):
        credentials_path = "credentials.json"
    
    with open(credentials_path, "r") as file:
        return json.load(file)

# =============================================================================
# Global Configuration Variables
# =============================================================================
credentials = load_credentials()

API_ID = credentials["API_ID"]
API_HASH = credentials["API_HASH"]
BOT_TOKEN = credentials["BOT_TOKEN"]
OWNER = credentials["USER_ID"]
DUMP_ID = credentials["DUMP_ID"]

# =============================================================================
# Event Loop Setup
# =============================================================================
def setup_event_loop():
    """
    Ensure an event loop exists before using pyrogram.
    This is necessary for certain environments like Google Colab.
    """
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

setup_event_loop()

# =============================================================================
# Pyrogram Client Creation
# =============================================================================
leechbot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=100,
    max_concurrent_transmissions=5
)

logger.info("LeechBot client initialized successfully")
