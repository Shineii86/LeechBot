# =============================================================================
#  LeechBot - Advanced Telegram File Transloader
#  Copyright (c) 2026 Shinei Nouzen | GitHub: https://github.com/Shineii86
# =============================================================================
# @title **🚀 LeechBot Colab Deployer**
#@markdown <div align="center">
#@markdown   <img src="https://user-images.githubusercontent.com/125879861/255391401-371f3a64-732d-4954-ac0f-4f093a6605e1.png" width="600px">
#@markdown </div>
#@markdown 
#@markdown **✨ Features**: Secrets Support • Auto-Recovery • GPU Optimization • Health Checks
#@markdown 
#@markdown ---
#@markdown ## 🔐 **Credentials**
#@markdown 
#@markdown | Field | Secret Key Name | Required |
#@markdown |-------|----------------|----------|
#@markdown | API_ID | `LEECHBOT_API_ID` | ✅ |
#@markdown | API_HASH | `LEECHBOT_API_HASH` | ✅ |
#@markdown | BOT_TOKEN | `LEECHBOT_BOT_TOKEN` | ✅ |
#@markdown | USER_ID | `LEECHBOT_USER_ID` | ✅ |
#@markdown | DUMP_ID | `LEECHBOT_DUMP_ID` | ✅ |

# Fallback inputs (if not using Secrets)
API_ID = 0  # @param {type:"integer"}
API_HASH = ""  # @param {type:"string"}
BOT_TOKEN = ""  # @param {type:"string"}
USER_ID = 0  # @param {type:"integer"}
DUMP_ID = 0  # @param {type:"integer"}

#@markdown ---
#@markdown ## ⚙️ **Deployment Options**
MOUNT_DRIVE = False  # @param {type:"boolean"}
USE_GPU = True       # @param {type:"boolean"}
ENABLE_LOGS = True   # @param {type:"boolean"}
AUTO_RESTART = True  # @param {type:"boolean"}
REPO_BRANCH = "main"  # @param ["main"]

#@markdown ---
#@markdown > 💡 **Tip**: Click **Runtime → Run all** or press **Ctrl+F9** after filling credentials.

# =============================================================================
#  📦 Imports & Setup
# =============================================================================
import subprocess, sys, os, json, time, shutil, signal
from pathlib import Path
from IPython.display import clear_output, display, HTML, Markdown, Javascript
from google.colab import auth, drive, files
import ipywidgets as widgets
from tqdm.notebook import tqdm, trange
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO if ENABLE_LOGS else logging.WARNING,
    format='[%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("LeechBot")

# =============================================================================
#  🎨 UI Components
# =============================================================================
class ColabUI:
    """Enhanced Colab UI with progress tracking."""
    
    @staticmethod
    def banner():
        return """
╔═════════════════════════════════════════╗
║  🚀 𝗟𝗲𝗲𝗰𝗵𝗕𝗼𝘁 - 𝗔𝗱𝘃𝗮𝗻𝗰𝗲𝗱 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗙𝗶𝗹𝗲 𝗧𝗿𝗮𝗻𝘀𝗹𝗼𝗮𝗱𝗲𝗿  ║
╠═════════════════════════════════════════╣
║  👤 Dev: Shinei Nouzen                         ║
║  📂 GitHub: Shineii86/LeechBot                 ║
║  💬 Telegram: https://t.me/Shineii86           ║
╚═════════════════════════════════════════╝
"""

    @staticmethod
    def progress_bar(description: str, total: int):
        return tqdm(total=total, desc=description, leave=True, colour='#4CAF50')

    @staticmethod
    def status(emoji: str, msg: str, level: str = "info"):
        colors = {"info": "#2196F3", "success": "#4CAF50", "error": "#F44336", "warning": "#FF9800"}
        display(Markdown(f'<font color="{colors.get(level, "#999")}">[{emoji}] {msg}</font>'))

# =============================================================================
#  🔐 Credential Management
# =============================================================================
def get_credentials():
    """Load credentials from Colab Secrets (preferred) or fallback inputs."""
    creds = {}
    
    # Try Colab Secrets first [[6]]
    try:
        from google.colab import userdata
        secrets_map = {
            'API_ID': 'LEECHBOT_API_ID',
            'API_HASH': 'LEECHBOT_API_HASH', 
            'BOT_TOKEN': 'LEECHBOT_BOT_TOKEN',
            'USER_ID': 'LEECHBOT_USER_ID',
            'DUMP_ID': 'LEECHBOT_DUMP_ID'
        }
        
        for key, secret_name in secrets_map.items():
            try:
                value = userdata.get(secret_name)
                creds[key] = int(value) if key in ['API_ID', 'USER_ID', 'DUMP_ID'] else value
                ColabUI.status("🔐", f"Loaded {key} from Colab Secrets", "success")
            except userdata.SecretNotFoundError:
                creds[key] = None
    except ImportError:
        ColabUI.status("ℹ️", "Colab Secrets not available; using manual inputs", "info")
    
    # Fallback to manual inputs
    fallbacks = {
        'API_ID': API_ID, 'API_HASH': API_HASH, 'BOT_TOKEN': BOT_TOKEN,
        'USER_ID': USER_ID, 'DUMP_ID': DUMP_ID
    }
    
    for key in creds:
        if creds[key] is None:
            creds[key] = fallbacks.get(key)
    
    return creds

def validate_credentials(creds: dict) -> bool:
    """Validate all required credentials are present."""
    required = ['API_ID', 'API_HASH', 'BOT_TOKEN', 'USER_ID', 'DUMP_ID']
    missing = [k for k in required if not creds.get(k)]
    
    if missing:
        ColabUI.status("❌", f"Missing credentials: {', '.join(missing)}", "error")
        return False
    
    # Format DUMP_ID if needed
    dump_str = str(creds['DUMP_ID'])
    if len(dump_str) == 10 and not dump_str.startswith('-100'):
        creds['DUMP_ID'] = int("-100" + dump_str)
        ColabUI.status("🔄", "Auto-formatted DUMP_ID", "info")
    
    return True

# =============================================================================
#  🛠️ Setup Functions
# =============================================================================
def run_command(cmd: str, description: str, retries: int = 3) -> bool:
    """Execute shell command with retry logic and progress tracking."""
    for attempt in range(retries):
        try:
            ColabUI.status("⏳", f"{description} (attempt {attempt+1}/{retries})")
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, check=True,
                timeout=300  # 5 min timeout
            )
            ColabUI.status("✅", f"{description} completed", "success")
            return True
        except subprocess.CalledProcessError as e:
            logger.warning(f"Command failed: {e.stderr[:200]}")
            if attempt == retries - 1:
                ColabUI.status("❌", f"{description} failed after {retries} attempts", "error")
                return False
            time.sleep(2 ** attempt)  # Exponential backoff
        except subprocess.TimeoutExpired:
            ColabUI.status("⚠️", f"{description} timed out", "warning")
            if attempt == retries - 1:
                return False
    return False

def clone_repo(branch: str = "main") -> bool:
    """Clone repository with branch selection."""
    repo_url = f"https://github.com/Shineii86/LeechBot.git"
    target = "/content/leechbot"
    
    # Clean previous install
    if os.path.exists(target):
        shutil.rmtree(target)
        ColabUI.status("🧹", "Cleaned previous installation")
    
    return run_command(
        f"git clone -b {branch} --depth 1 {repo_url} {target}",
        f"📥 Cloning repo (branch: {branch})"
    )

def install_dependencies() -> bool:
    """Install system and Python dependencies."""
    # System packages
    if not run_command(
        "apt-get update -qq && apt-get install -y -qq ffmpeg aria2 megatools p7zip-full unzip",
        "🔧 Installing system packages"
    ):
        return False
    
    # Python packages with cache
    return run_command(
        "pip3 install -q --no-cache-dir -r /content/leechbot/requirements.txt",
        "🐍 Installing Python dependencies"
    )

def check_gpu() -> dict:
    """Detect and report GPU availability."""
    info = {"available": False, "name": None, "memory": None}
    
    if not USE_GPU:
        ColabUI.status("ℹ️", "GPU usage disabled by user", "info")
        return info
    
    try:
        # Try nvidia-smi first
        result = subprocess.run("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader", 
                              shell=True, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        if lines:
            name, memory = lines[0].split(', ')
            info.update({"available": True, "name": name.strip(), "memory": memory.strip()})
            ColabUI.status("🎮", f"GPU detected: {name} ({memory} VRAM)", "success")
    except:
        # Fallback to GPUtil
        try:
            import GPUtil
            gpus = GPUtil.getAvailable(order='memory', limit=1)
            if gpus:
                info["available"] = True
                ColabUI.status("🎮", f"GPU acceleration enabled", "success")
        except ImportError:
            pass
    
    if not info["available"]:
        ColabUI.status("ℹ️", "Using CPU fallback (no GPU detected)", "info")
    
    return info

def save_config(creds: dict, path: str = "/content/leechbot/credentials.json"):
    """Save configuration securely."""
    # Don't save raw tokens to disk if using secrets
    safe_creds = creds.copy()
    if os.environ.get('COLAB_SECRETS_AVAILABLE'):
        safe_creds['BOT_TOKEN'] = "***REDACTED***"
    
    with open(path, 'w') as f:
        json.dump(safe_creds, f, indent=2)
    os.chmod(path, 0o600)  # Restrict permissions
    ColabUI.status("💾", "Configuration saved securely", "success")

# =============================================================================
#  🚀 Main Deployment
# =============================================================================
def deploy():
    """Main deployment orchestration."""
    clear_output(wait=True)
    print(ColabUI.banner())
    
    # Step 1: Load & validate credentials
    ColabUI.status("🔐", "Loading credentials...")
    creds = get_credentials()
    if not validate_credentials(creds):
        ColabUI.status("❌", "Deployment aborted: invalid credentials", "error")
        return
    
    # Step 2: Clone repository
    if not clone_repo(REPO_BRANCH):
        return
    
    # Step 3: Install dependencies
    if not install_dependencies():
        return
    
    # Step 4: Check hardware
    gpu_info = check_gpu()
    
    # Step 5: Save configuration
    save_config(creds)
    
    # Step 6: Mount Drive if requested
    if MOUNT_DRIVE:
        try:
            from google.colab import drive
            drive.mount('/content/drive')
            ColabUI.status("☁️", "Google Drive mounted", "success")
        except Exception as e:
            ColabUI.status("⚠️", f"Drive mount failed: {e}", "warning")
    
    # Step 7: Final preparation
    ColabUI.status("✨", "Finalizing setup...")
    
    # Clean old sessions
    session_files = [
        "/content/leechbot/my_bot.session",
        "/content/leechbot/my_bot.session-journal"
    ]
    for sf in session_files:
        if os.path.exists(sf):
            os.remove(sf)
    
    # Display completion message
    clear_output(wait=True)
    print(ColabUI.banner())
    
    display(Markdown("""
### ✅ **Deployment Successful!** 🎉

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot & show menu |
| `/tupload` | Upload files to Telegram |
| `/gdupload` | Mirror to Google Drive |
| `/ytupload` | Download via yt-dlp |
| `/settings` | Configure preferences |
| `/help` | Show all available commands |

> ⚠️ **Keep this tab open** while the bot runs. Use [ngrok](https://ngrok.com) for 24/7 deployment.
"""))
    
    # Step 8: Launch bot
    ColabUI.status("🚀", "Starting LeechBot...", "success")
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        ColabUI.status("🛑", "Received shutdown signal, cleaning up...")
        sys.exit(0)
    
    if AUTO_RESTART:
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
    
    # Execute bot
    os.chdir("/content/leechbot")
    get_ipython().system('python3 -m leechbot')

# =============================================================================
#  🎯 Execution Entry Point
# =============================================================================
if __name__ == "__main__":
    try:
        deploy()
    except KeyboardInterrupt:
        ColabUI.status("👋", "Deployment cancelled by user", "warning")
    except Exception as e:
        ColabUI.status("💥", f"Unexpected error: {e}", "error")
        if ENABLE_LOGS:
            logger.exception("Full traceback:")
