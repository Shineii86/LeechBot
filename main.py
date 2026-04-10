# =============================================================================
#  ʟᴇᴇᴄʜʙᴏᴛ - ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ᴛʀᴀɴsʟᴏᴀᴅᴇʀ
# =============================================================================
#  ᴄᴏᴘʏʀɪɢʜᴛ © 2024-2025 sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ
#  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86
#  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86
# =============================================================================

"""
ɢᴏᴏɢʟᴇ ᴄᴏʟᴀʙ sᴇᴛᴜᴘ sᴄʀɪᴘᴛ ғᴏʀ ʟᴇᴇᴄʜʙᴏᴛ

ᴛʜɪs sᴄʀɪᴘᴛ sᴇᴛs ᴜᴘ ᴀɴᴅ ʀᴜɴs ʟᴇᴇᴄʜʙᴏᴛ ɪɴ ɢᴏᴏɢʟᴇ ᴄᴏʟᴀʙ.
ғɪʟʟ ɪɴ ʏᴏᴜʀ ᴄʀᴇᴅᴇɴᴛɪᴀʟs ʙᴇʟᴏᴡ ᴀɴᴅ ʀᴜɴ ᴛʜᴇ ᴄᴇʟʟ.
"""

# @title **🚀 ʟᴇᴇᴄʜʙᴏᴛ - ɢᴏᴏɢʟᴇ ᴄᴏʟᴀʙ sᴇᴛᴜᴘ**
# @markdown **ᴅᴇᴠᴇʟᴏᴘᴇʀ:** [sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ](https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86)
# @markdown **ʀᴇᴘᴏsɪᴛᴏʀʏ:** [ʟᴇᴇᴄʜʙᴏᴛ](https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86/ʟᴇᴇᴄʜʙᴏᴛ)

# @markdown ---
# @markdown **🔐 ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴄʀᴇᴅᴇɴᴛɪᴀʟs:**

API_ID = 0  # @param {type: "integer"}
API_HASH = ""  # @param {type: "string"}
BOT_TOKEN = ""  # @param {type: "string"}
USER_ID = 0  # @param {type: "integer"}
DUMP_ID = 0  # @param {type: "integer"}

# @markdown ---
# @markdown **💡 ɴᴏᴛᴇs:**
# @markdown - ɢᴇᴛ **ᴀᴘɪ_ɪᴅ** ᴀɴᴅ **ᴀᴘɪ_ʜᴀsʜ** ғʀᴏᴍ [ᴍʏ.ᴛᴇʟᴇɢʀᴀᴍ.ᴏʀɢ](https://ᴍʏ.ᴛᴇʟᴇɢʀᴀᴍ.ᴏʀɢ)
# @markdown - ɢᴇᴛ **ʙᴏᴛ_ᴛᴏᴋᴇɴ** ғʀᴏᴍ [@ʙᴏᴛғᴀᴛʜᴇʀ](https://ᴛ.ᴍᴇ/ʙᴏᴛғᴀᴛʜᴇʀ)
# @markdown - **ᴜsᴇʀ_ɪᴅ** ɪs ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀ ɪᴅ
# @markdown - **ᴅᴜᴍᴘ_ɪᴅ** ɪs ᴛʜᴇ ᴄʜᴀɴɴᴇʟ/ɢʀᴏᴜᴘ ɪᴅ ғᴏʀ ʟᴏɢs

import subprocess
import time
import json
import shutil
import os
from IPython.display import clear_output, display, HTML
from threading import Thread

Working = True

def keep_alive(url):
    """ᴋᴇᴇᴘ ᴄᴏʟᴀʙ ᴀʟɪᴠᴇ ᴡɪᴛʜ sɪʟᴇɴᴛ ᴀᴜᴅɪᴏ"""
    display(HTML(f'<audio src="{url}" controls autoplay style="display:none"></audio>'))

def Loading():
    """ʟᴏᴀᴅɪɴɢ ᴀɴɪᴍᴀᴛɪᴏɴ"""
    white = 37
    black = 0
    while Working:
        print("\r" + "░" * white + "▒▒" + "▓" * black + "▒▒" + "░" * white, end="")
        black = (black + 2) % 75
        white = (white - 1) if white != 0 else 37
        time.sleep(2)
    clear_output()

# sᴛᴀʀᴛ ᴋᴇᴇᴘ-ᴀʟɪᴠᴇ ᴀᴜᴅɪᴏ
audio_url = "https://raw.githubusercontent.com/KoboldAI/KoboldAI-Client/main/colab/silence.m4a"
audio_thread = Thread(target=keep_alive, args=(audio_url,))
audio_thread.start()

# sᴛᴀʀᴛ ʟᴏᴀᴅɪɴɢ ᴀɴɪᴍᴀᴛɪᴏɴ
loading_thread = Thread(target=Loading, name="ʟᴏᴀᴅɪɴɢ", args=())
loading_thread.start()

# ғɪx ᴅᴜᴍᴘ ɪᴅ ғᴏʀᴍᴀᴛ
if len(str(DUMP_ID)) == 10 and "-100" not in str(DUMP_ID):
    DUMP_ID = int("-100" + str(DUMP_ID))

# ᴄʟᴇᴀɴ ᴇxɪsᴛɪɴɢ ɪɴsᴛᴀʟʟᴀᴛɪᴏɴ
if os.path.exists("/content/sample_data"):
    shutil.rmtree("/content/sample_data")

if os.path.exists("/content/tgdl"):
    shutil.rmtree("/content/tgdl")

# ᴄʟᴏɴᴇ ʀᴇᴘᴏsɪᴛᴏʀʏ
print("\n📥 ᴄʟᴏɴɪɴɢ ʀᴇᴘᴏsɪᴛᴏʀʏ...")
subprocess.run("git clone https://github.com/Shineii86/LeechBot.git /content/tgdl", shell=True)

# ɪɴsᴛᴀʟʟ sʏsᴛᴇᴍ ᴅᴇᴘᴇɴᴅᴇɴᴄɪᴇs
print("🔧 ɪɴsᴛᴀʟʟɪɴɢ sʏsᴛᴇᴍ ᴅᴇᴘᴇɴᴅᴇɴᴄɪᴇs...")
subprocess.run("apt-get update -qq && apt-get install -y -qq ffmpeg aria2 megatools p7zip-full unzip", shell=True)

# ɪɴsᴛᴀʟʟ ᴘʏᴛʜᴏɴ ᴅᴇᴘᴇɴᴅᴇɴᴄɪᴇs
print("🐍 ɪɴsᴛᴀʟʟɪɴɢ ᴘʏᴛʜᴏɴ ᴅᴇᴘᴇɴᴅᴇɴᴄɪᴇs...")
subprocess.run("pip3 install -q -r /content/tgdl/requirements.txt", shell=True)

# sᴀᴠᴇ ᴄʀᴇᴅᴇɴᴛɪᴀʟs
credentials = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "USER_ID": USER_ID,
    "DUMP_ID": DUMP_ID,
}

with open("/content/tgdl/credentials.json", "w") as f:
    json.dump(credentials, f, indent=4)

# sᴛᴏᴘ ʟᴏᴀᴅɪɴɢ ᴀɴɪᴍᴀᴛɪᴏɴ
Working = False
loading_thread.join()
clear_output()

# ʀᴇᴍᴏᴠᴇ ᴏʟᴅ sᴇssɪᴏɴ
if os.path.exists("/content/tgdl/my_bot.session"):
    os.remove("/content/tgdl/my_bot.session")
    os.remove("/content/tgdl/my_bot.session-journal")

print("""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 ʟᴇᴇᴄʜʙᴏᴛ sᴛᴀʀᴛɪɴɢ...                    ║
╠══════════════════════════════════════════════════════════════╣
║  ᴅᴇᴠᴇʟᴏᴘᴇʀ: sʜɪɴᴇɪ ɴᴏᴜᴢᴇɴ (@sʜɪɴᴇɪɪ86)                      ║
║  ɢɪᴛʜᴜʙ: https://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/sʜɪɴᴇɪɪ86/ʟᴇᴇᴄʜʙᴏᴛ            ║
║  ᴛᴇʟᴇɢʀᴀᴍ: https://ᴛ.ᴍᴇ/sʜɪɴᴇɪɪ86                           ║
╚══════════════════════════════════════════════════════════════╝
""")

# ʀᴜɴ ᴛʜᴇ ʙᴏᴛ
!cd /content/tgdl && python3 -m leechbot
