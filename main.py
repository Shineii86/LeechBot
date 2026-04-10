# =============================================================================
# LeechBot Pro - Google Colab Deployment Script
# =============================================================================
# Project   : Telegram Leech Bot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

# @title <font color="#00ff00">🚀 LeechBot - Colab Launcher</font>
# @markdown <div align="center"><h1>🚀 LeechBot Pro</h1></div>
# @markdown <div align="center"><b>Advanced Telegram Leeching Bot</b></div>
# @markdown <br>
# @markdown <div align="center">Developed by <a href="https://github.com/Shineii86">Shinei Nouzen</a></div>
# @markdown <br><br>

# =============================================================================
# CONFIGURATION
# =============================================================================
# @markdown ### 🔑 Enter Your Credentials:
API_ID = 0  # @param {type: "integer"}
API_HASH = ""  # @param {type: "string"}
BOT_TOKEN = ""  # @param {type: "string"}
USER_ID = 0  # @param {type: "integer"}
DUMP_ID = 0  # @param {type: "integer"}

# @markdown ### 📁 Optional Settings:
AUTO_MOUNT_DRIVE = True  # @param {type: "boolean"}
CLEAN_INSTALL = False  # @param {type: "boolean"}

import subprocess
import time
import json
import shutil
import os
from IPython.display import clear_output, display, HTML
from threading import Thread

# =============================================================================
# ANIMATION & KEEP-ALIVE
# =============================================================================
Working = True

def keep_alive(url):
    """Keep Colab session alive with silent audio."""
    display(HTML(f'<audio src="{url}" controls autoplay style="display:none"></audio>'))

def loading_animation():
    """Show loading animation."""
    white = 37
    black = 0
    while Working:
        print("\r" + "░" * white + "▒▒" + "▓" * black + "▒▒" + "░" * white, end="")
        black = (black + 2) % 75
        white = white - 1 if white != 0 else 37
        time.sleep(0.5)
    clear_output()

# Start keep-alive
audio_url = "https://raw.githubusercontent.com/KoboldAI/KoboldAI-Client/main/colab/silence.m4a"
audio_thread = Thread(target=keep_alive, args=(audio_url,))
audio_thread.start()

# Start loading animation
loading_thread = Thread(target=loading_animation, name="Loading")
loading_thread.start()

# =============================================================================
# SETUP DIRECTORIES
# =============================================================================
# Fix DUMP_ID format
if DUMP_ID and len(str(DUMP_ID)) == 10 and "-100" not in str(DUMP_ID):
    DUMP_ID = int("-100" + str(DUMP_ID))

# Clean previous installation if requested
if CLEAN_INSTALL:
    for path in ["/content/leechbot", "/content/sample_data"]:
        if os.path.exists(path):
            shutil.rmtree(path)

# Create directories
os.makedirs("/content/leechbot", exist_ok=True)
os.makedirs("/content/leechbot/BOT_WORK", exist_ok=True)

# =============================================================================
# INSTALL DEPENDENCIES
# =============================================================================
print("\n📦 Installing dependencies...")

# Install system packages
subprocess.run("apt-get update -qq && apt-get install -y -qq ffmpeg aria2 megatools p7zip-full", 
               shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Clone repository
if not os.path.exists("/content/leechbot/bot"):
    subprocess.run(
        "git clone -q https://github.com/Shineii86/LeechBot.git /tmp/leechbot && "
        "cp -r /tmp/leechbot/* /content/leechbot/",
        shell=True
    )

# Install Python packages
requirements = """
pyrogram>=2.0.106
tgcrypto>=1.2.5
asyncio>=3.4.3
uvloop>=0.19.0
aiohttp>=3.9.1
google-api-python-client>=2.115.0
google-auth-httplib2>=0.2.0
google-auth-oauthlib>=1.2.0
yt-dlp>=2024.1.1
pymegatools>=1.0.0
moviepy>=1.0.3
opencv-python>=4.9.0.80
Pillow>=10.2.0
psutil>=5.9.8
GPUtil>=1.4.0
natsort>=8.4.0
pytz>=2024.1
requests>=2.31.0
"""

with open("/tmp/requirements.txt", "w") as f:
    f.write(requirements)

subprocess.run("pip install -q -r /tmp/requirements.txt", shell=True)

# =============================================================================
# MOUNT GOOGLE DRIVE
# =============================================================================
if AUTO_MOUNT_DRIVE:
    print("☁️ Mounting Google Drive...")
    from google.colab import drive
    try:
        drive.mount('/content/drive', force_remount=True)
        print("✅ Google Drive mounted successfully!")
    except Exception as e:
        print(f"⚠️ Drive mount failed: {e}")

# =============================================================================
# SAVE CREDENTIALS
# =============================================================================
credentials = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "USER_ID": USER_ID,
    "DUMP_ID": DUMP_ID,
}

with open('/content/leechbot/credentials.json', 'w') as f:
    json.dump(credentials, f)

# Remove old session
if os.path.exists("/content/leechbot/leechbot_pro.session"):
    os.remove("/content/leechbot/leechbot_pro.session")

# =============================================================================
# START BOT
# =============================================================================
Working = False
clear_output()

print("""
╔══════════════════════════════════════════════╗
║                                                      ║
║                    🚀 LeechBot Pro                   ║
║                                                      ║
║  Developer : Shinei Nouzen                           ║
║  GitHub    : https://github.com/Shineii86            ║
║  Telegram  : https://telegram.me/Shineii86           ║
║  Updates   : https://telegram.me/MaximXBots          ║
║  Support   : https://telegram.me/MaximXGroup         ║ 
║                                                      ║
║       © 2026 Shinei Nouzen All Rights Reserved       ║                 ║
╚══════════════════════════════════════════════╝
""")

print("✅ Setup complete!")
print("🚀 Starting bot...")
print("-" * 60)

# Change to bot directory and run
os.chdir("/content/leechbot")
os.system("python -m bot")
