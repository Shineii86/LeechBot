# =============================================================================
#  LeechBot - Advanced Telegram File Transloader
# =============================================================================
#  Copyright (c) 2026 Shinei Nouzen
#  GitHub: https://github.com/Shineii86
#  Telegram: https://telegram.me/Shineii86
# =============================================================================

"""
Google Colab Setup Script for LeechBot

This script sets up and runs LeechBot in Google Colab.
Fill in your credentials below and run the cell.
"""

# @title **🚀 LeechBot - Google Colab Setup**
# @markdown <div align="center">
# @markdown   <img src="https://user-images.githubusercontent.com/125879861/255391401-371f3a64-732d-4954-ac0f-4f093a6605e1.png" width="600px">
# @markdown </div>
# @markdown 
# @markdown **Developer:** [Shinei Nouzen](https://github.com/Shineii86)  
# @markdown **Repository:** [LeechBot](https://github.com/Shineii86/LeechBot)
# @markdown 
# @markdown ---
# @markdown ## 🔐 **Enter Your Credentials:**
# @markdown 
# @markdown | Field | Description |
# @markdown |-------|-------------|
# @markdown | **API_ID** | Get from [my.telegram.org](https://my.telegram.org) |
# @markdown | **API_HASH** | Get from [my.telegram.org](https://my.telegram.org) |
# @markdown | **BOT_TOKEN** | Get from [@BotFather](https://t.me/BotFather) |
# @markdown | **USER_ID** | Your Telegram user ID |
# @markdown | **DUMP_ID** | Channel/group ID for logs (e.g., `-1001234567890`) |

API_ID = 0  # @param {type: "integer"}
API_HASH = ""  # @param {type: "string"}
BOT_TOKEN = ""  # @param {type: "string"}
USER_ID = 0  # @param {type: "integer"}
DUMP_ID = 0  # @param {type: "integer"}

# @markdown ---
# @markdown ## ⚙️ **Additional Options**
MOUNT_DRIVE = False  # @param {type:"boolean"}
USE_GPU = True       # @param {type:"boolean"}

# @markdown ---
# @markdown ## 🚀 **Run Setup**
# @markdown Click **Runtime → Run all** or press **Ctrl+F9** to execute all cells.

# =============================================================================
#  Setup Script - Emoji-Only UI (Braille Spinner)
# =============================================================================

import subprocess
import time
import json
import shutil
import os
import sys
from IPython.display import clear_output, display, HTML, Markdown
from threading import Thread

# =============================================================================
#  Global Variables
# =============================================================================
Working = True

def print_banner():
    """Display a simple banner using plain text with emojis."""
    banner = """

██╗░░░░░███████╗███████╗░█████╗░░█████╗░██╗░░██╗
██║░░░░░██╔════╝██╔════╝██╔══██╗██╔══██╗██║░░██║
██║░░░░░█████╗░░█████╗░░███████║██║░░╚═╝███████║
██║░░░░░██╔══╝░░██╔══╝░░██╔══██║██║░░██╗██╔══██║
███████╗███████╗███████╗██║░░██║╚█████╔╝██║░░██║
╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
╔════════════════════════════════════════════════════════╗
║                                                                  ║
║           🚀 𝗔𝗗𝗩𝗔𝗡𝗖𝗘𝗗 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗙𝗜𝗟𝗘 𝗧𝗥𝗔𝗡𝗦𝗟𝗢𝗔𝗗𝗘𝗥           vb ║
║                                                                  ║
╠════════════════════════════════════════════════════════╣
║   👤 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿: 𝖲𝗁𝗂𝗇𝖾𝗂 𝖭𝗈𝗎𝗓𝖾𝗇                                      ║
║   📂 𝗚𝗶𝘁𝗛𝘂𝗯: https://github.com/Shineii86/LeechBot               ║
║   💬 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺: https://telegram.me/Shineii86                      ║
╚═════════════════════════════════════════════════════════╝
"""
    print(banner)

def print_step(emoji, text):
    """Print a step with emoji."""
    print(f"[{emoji}] {text}")

def print_success(text):
    """Print a success message."""
    print(f"[✅] {text}")

def print_error(text):
    """Print an error message."""
    print(f"[❌] {text}")

def print_info(text):
    """Print an info message."""
    print(f"[ℹ️] {text}")

def keep_alive(url):
    """Keep Colab alive with silent audio."""
    display(HTML(f'<audio src="{url}" controls autoplay style="display:none"></audio>'))

def loading_animation():
    """Display a braille spinner (Unicode)."""
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    idx = 0
    while Working:
        sys.stdout.write(f"\r⏳ Setting up LeechBot... {spinner[idx]} ")
        sys.stdout.flush()
        idx = (idx + 1) % len(spinner)
        time.sleep(0.15)
    sys.stdout.write("\r" + " " * 40 + "\r")
    sys.stdout.flush()

def mount_google_drive():
    """Mount Google Drive."""
    from google.colab import drive
    print_step("☁️", "Mounting Google Drive...")
    drive.mount('/content/drive')
    print_success("Google Drive mounted successfully!")

# =============================================================================
#  Start Setup
# =============================================================================
clear_output()
print_banner()

# Validate credentials
if API_ID == 0 or not API_HASH or not BOT_TOKEN or USER_ID == 0 or DUMP_ID == 0:
    print_error("Please fill in all credentials before running!")
    raise ValueError("Missing credentials")

# Start keep-alive audio (silent)
audio_url = "https://raw.githubusercontent.com/KoboldAI/KoboldAI-Client/main/colab/silence.m4a"
audio_thread = Thread(target=keep_alive, args=(audio_url,))
audio_thread.start()

# Start loading animation
loading_thread = Thread(target=loading_animation)
loading_thread.start()

# Fix DUMP_ID format
if len(str(DUMP_ID)) == 10 and "-100" not in str(DUMP_ID):
    DUMP_ID = int("-100" + str(DUMP_ID))

# =============================================================================
#  Clean Existing Installation
# =============================================================================
if os.path.exists("/content/sample_data"):
    shutil.rmtree("/content/sample_data")
    print_info("Removed sample_data directory")

if os.path.exists("/content/leechbot"):
    shutil.rmtree("/content/leechbot")
    print_info("Removed old installation")

# =============================================================================
#  Clone Repository
# =============================================================================
Working = False
loading_thread.join()
Working = True
loading_thread = Thread(target=loading_animation)
loading_thread.start()

print_step("📥", "Cloning LeechBot repository...")
result = subprocess.run(
    "git clone https://github.com/Shineii86/LeechBot.git /content/leechbot",
    shell=True,
    capture_output=True,
    text=True
)
if result.returncode == 0:
    print_success("Repository cloned successfully!")
else:
    print_error(f"Clone failed: {result.stderr}")
    raise RuntimeError("Git clone failed")

# =============================================================================
#  Install System Dependencies
# =============================================================================
print_step("🔧", "Installing system dependencies...")
packages = "ffmpeg aria2 megatools p7zip-full unzip"
result = subprocess.run(
    f"apt-get update -qq && apt-get install -y -qq {packages}",
    shell=True,
    capture_output=True,
    text=True
)
if result.returncode == 0:
    print_success("System dependencies installed!")
else:
    print_error(f"Installation failed: {result.stderr}")

# =============================================================================
#  Install Python Dependencies
# =============================================================================
print_step("🐍", "Installing Python packages...")
result = subprocess.run(
    "pip3 install -q -r /content/leechbot/requirements.txt",
    shell=True,
    capture_output=True,
    text=True
)
if result.returncode == 0:
    print_success("Python packages installed!")
else:
    print_error(f"Pip install failed: {result.stderr}")

# =============================================================================
#  Save Credentials
# =============================================================================
credentials = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "USER_ID": USER_ID,
    "DUMP_ID": DUMP_ID,
}

with open("/content/leechbot/credentials.json", "w") as f:
    json.dump(credentials, f, indent=4)
print_success("Credentials saved!")

# =============================================================================
#  Mount Google Drive (if selected)
# =============================================================================
if MOUNT_DRIVE:
    mount_google_drive()

# =============================================================================
#  GPU Check
# =============================================================================
if USE_GPU:
    try:
        import GPUtil
        gpus = GPUtil.getAvailable()
        if gpus:
            print_success(f"GPU acceleration enabled! Found {len(gpus)} GPU(s)")
        else:
            print_info("No GPU found; using CPU fallback")
    except ImportError:
        print_info("GPUtil not installed; using CPU fallback")

# =============================================================================
#  Stop Loading Animation
# =============================================================================
Working = False
loading_thread.join()
clear_output()
print_banner()

# Remove old session files
if os.path.exists("/content/leechbot/my_bot.session"):
    os.remove("/content/leechbot/my_bot.session")
    if os.path.exists("/content/leechbot/my_bot.session-journal"):
        os.remove("/content/leechbot/my_bot.session-journal")
    print_info("Cleaned old session files")

# =============================================================================
#  Final Success Message (using Markdown for formatting)
# =============================================================================
display(Markdown("""
---
### ✅ **Setup Complete!**  
Your LeechBot is now starting. Use the following commands in Telegram:

| Command | Description |
|---------|-------------|
| `/start` | Show welcome message |
| `/tupload` | Upload files to Telegram |
| `/gdupload` | Mirror to Google Drive |
| `/ytupload` | Download with YT-DLP |
| `/settings` | Configure bot settings |
| `/help` | Show all commands |

---
"""))

print("""

██╗░░░░░███████╗███████╗░█████╗░░█████╗░██╗░░██╗
██║░░░░░██╔════╝██╔════╝██╔══██╗██╔══██╗██║░░██║
██║░░░░░█████╗░░█████╗░░███████║██║░░╚═╝███████║
██║░░░░░██╔══╝░░██╔══╝░░██╔══██║██║░░██╗██╔══██║
███████╗███████╗███████╗██║░░██║╚█████╔╝██║░░██║
╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
╔════════════════════════════════════════════════════════╗
║                    🚀 LeechBot Is Starting...                    ║
╠════════════════════════════════════════════════════════╣
║   👤 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿: 𝖲𝗁𝗂𝗇𝖾𝗂 𝖭𝗈𝗎𝗓𝖾𝗇                                       ║
║   📂 𝗚𝗶𝘁𝗛𝘂𝗯: https://github.com/Shineii86/LeechBot                ║
║   💬 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺: https://telegram.me/Shineii86                      ║
╚════════════════════════════════════════════════════════╝
""")

# =============================================================================
#  Run the Bot
# =============================================================================
get_ipython().system('cd /content/leechbot && python3 -m leechbot')
