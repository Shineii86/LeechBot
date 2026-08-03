# 📖 LeechBot — Complete User Guide

Everything you need to set up, configure, and use LeechBot from scratch.

---

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Getting Credentials](#-getting-credentials)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Bot](#-running-the-bot)
- [Web Dashboard](#-web-dashboard)
- [Commands Reference](#-commands-reference)
- [Settings Menu](#-settings-menu)
- [Supported Sites](#-supported-sites)
- [Google Drive Setup](#-google-drive-setup)
- [YouTube Authentication](#-youtube-authentication)
- [Demos](#-demos)
- [Troubleshooting](#-troubleshooting)

---

## 🔧 Prerequisites

Before you start, make sure you have:

| Requirement | Why You Need It |
|-------------|----------------|
| **Python 3.10+** | Runtime environment |
| **Telegram Account** | To create a bot and get API keys |
| **A Server or VPS** | To run the bot 24/7 (or use Google Colab) |
| **libtorrent** | Magnet/torrent downloads (DHT, resume) |
| **ffmpeg** | Video/audio processing |
| **7zip / p7zip** | Archive handling |
| **unrar** | RAR extraction |
| **megatools** | Mega.nz downloads |

### System Dependencies (Ubuntu/Debian)

```bash
sudo apt update && sudo apt install -y ffmpeg aria2 p7zip-full unrar unzip python3-libtorrent megatools python3 python3-pip
```

### System Dependencies (Arch)

```bash
sudo pacman -S ffmpeg aria2 p7zip unrar python python-pip libtorrent-rasterbar megatools
```

### System Dependencies (macOS)

```bash
brew install ffmpeg aria2 p7zip megatools python
```

---

## 🔐 Getting Credentials

You need **5 values** to run the bot. Here's how to get each one:

### 1. API_ID & API_HASH

1. Go to [https://my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Click **"API development tools"**
4. Fill in the form (App title can be anything, e.g., "My LeechBot")
5. Click **"Create Application"**
6. Copy `api_id` (number) and `api_hash` (string)

> ⚠️ **Keep these secret.** Anyone with your API keys can access your Telegram account.

### 2. BOT_TOKEN

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose a display name for your bot (e.g., "My Leech Bot")
4. Choose a username ending in `bot` (e.g., `my_leech_bot`)
5. BotFather will send you a token like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
6. Copy the entire token

> 💡 You can create multiple bots with BotFather. Use `/mybots` to manage them.

> ℹ️ **Note:** Bot commands are **auto-registered** on startup — you don't need to set them manually via BotFather. The bot registers all 34 commands with Telegram automatically when it starts.

### 3. OWNER_ID

This is **your personal Telegram user ID** (not your phone number).

1. Open Telegram and search for [@userinfobot](https://t.me/userinfobot)
2. Send `/start`
3. It will reply with your numeric ID (e.g., `123456789`)

### 4. DUMP_ID

This is a **Telegram channel or group** where the bot sends download logs and task history.

1. Create a new Telegram channel (or use an existing one)
2. **Make the bot an admin** of that channel (it needs to send messages)
3. Get the channel ID:
   - Forward any message from the channel to [@userinfobot](https://t.me/userinfobot)
   - It will show the channel ID (e.g., `-1001234567890`)
   - Channel IDs always start with `-100`

> 💡 **Private channels work fine.** The bot just needs to be an admin with "Post Messages" permission.

---

## 📦 Installation

### Option A: Standard Setup

```bash
# Clone the repository
git clone https://github.com/Shineii86/LeechBot.git
cd LeechBot

# Install Python dependencies
pip install -r requirements.txt

# Create your config file
cp .env.example .env
```

Now edit `.env` with your credentials (see [Configuration](#-configuration)).

### Option B: Google Colab (No Server Needed)

1. Open `notebooks/LeechBot.ipynb` in Google Colab
2. Add your credentials to Colab Secrets (recommended) or fill in the form
3. Run **📦 Setup LeechBot** (Cell 2) — clones repo, installs dependencies, saves config
4. Run **🚀 Deploy LeechBot** (Cell 3) — starts bot with keep-alive, interact via Telegram

> 💡 The Deploy cell starts the bot and keeps the session alive. All interaction is via Telegram — no tunnel or web dashboard needed.

### Option C: Docker

```bash
git clone https://github.com/Shineii86/LeechBot.git
cd LeechBot
cp .env.example .env
nano .env
docker compose up -d
```

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## ⚙️ Configuration

Edit the `.env` file in the project root. Here's every option explained:

### Required Settings

```env
# Your Telegram API credentials (from my.telegram.org)
API_ID=12345
API_HASH=your_api_hash_here

# Your bot token (from @BotFather)
BOT_TOKEN=your_bot_token_here

# Your personal Telegram user ID
OWNER_ID=123456789

# Channel ID for logs and task history (bot must be admin)
DUMP_ID=-1001234567890
```

### Optional Settings

```env
# --- Paths ---
LEECHBOT_BASE_DIR=/tmp/leechbot

# --- Download Settings ---
AUTO_RETRY_COUNT=3
DEFAULT_UPLOAD_MODE=media
BANDWIDTH_LIMIT=

# --- Web Dashboard ---
WEB_PORT=8080
WEB_TOKEN=

# --- Multi-User Support ---
ALLOWED_USERS=

# --- YouTube Cookies (optional) ---
# YTDL_COOKIES_FILE=/path/to/cookies.txt

# --- Google Drive (optional) ---
TOKEN_PICKLE_PATH=
```

> 💡 **Full reference:** See [.env.example](.env.example) for all options with inline comments.

---

## 🚀 Running the Bot

### Start the bot

```bash
cd LeechBot
python3 leechbot.py
# or
python3 -m leechbot
```

### First run

On first start:
1. The bot creates a session file in `sessions/` directory
2. It resolves your DUMP_ID and OWNER_ID peers
3. You'll see "LeechBot started successfully" in the console
4. Send `/start` to your bot in Telegram

### Keep it running

**Option 1: Screen (simple)**
```bash
screen -S leechbot
python3 leechbot.py
# Press Ctrl+A, then D to detach
# Re-attach with: screen -r leechbot
```

**Option 2: tmux**
```bash
tmux new -s leechbot
python3 leechbot.py
# Press Ctrl+B, then D to detach
# Re-attach with: tmux attach -t leechbot
```

**Option 3: systemd (recommended for VPS)**

Create `/etc/systemd/system/leechbot.service`:
```ini
[Unit]
Description=LeechBot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/LeechBot
ExecStart=/usr/bin/python3 leechbot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable leechbot
sudo systemctl start leechbot
sudo systemctl status leechbot
sudo journalctl -u leechbot -f
```

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 🌐 Web Dashboard

LeechBot includes a **real-time web dashboard** that runs alongside the bot. Monitor queue, stats, settings, and active tasks from your browser.

### How It Works

```
Bot (Kurigram) ←→ Web Server (aiohttp) ←→ Browser Dashboard
     ↕                    ↕
  Telegram API        REST + WebSocket
```

The dashboard starts automatically when the bot starts. You'll see this in the logs:

```
🌐 Web dashboard running on http://0.0.0.0:8080
📊 Dashboard URL: http://0.0.0.0:8080/dashboard
🔑 Dashboard token: xK9f2mNp...
```

### Access the Dashboard

**Option 1: GitHub Pages (Recommended for Colab)**

The dashboard is hosted at **https://shineii86.github.io/LeechBot/** — no setup needed.

1. Deploy the bot using the notebook → Setup + Deploy cells
2. The bot runs on Colab with the web dashboard active in the background
3. For remote access, use a VPS or self-hosted deployment (see Option 2)

**Option 2: Local Dashboard (VPS / Self-hosted)**

1. Start the bot: `python3 leechbot.py` (or `python3 -m leechbot`)
2. Open `http://your-server-ip:8080` in your browser
3. Enter the token from the bot logs

**Option 3: Colab Built-in (No GitHub Pages)**

1. Run **🚀 Deploy LeechBot** (Cell 3) — bot starts with keep-alive
2. Interact entirely via Telegram — all commands work without the web dashboard
3. The web dashboard runs in the background but is not accessible without a tunnel

**Behind a reverse proxy (nginx):**

```nginx
location /dashboard/ {
    proxy_pass http://127.0.0.1:8080/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WEB_PORT` | `8080` | Port for the web dashboard |
| `WEB_TOKEN` | Auto-generated | Auth token for dashboard access |

Set them in your `.env` file or environment:

```bash
WEB_PORT=8080
WEB_TOKEN=my_secret_token_here
```

### Dashboard Features

| Feature | Description |
|---------|-------------|
| 🔐 **Login** | Token-based auth (saved in browser localStorage) |
| 📊 **Status Cards** | Idle/active, total downloads, uploads, task count |
| 🔄 **Active Task** | Mode, progress bar, speed, ETA, elapsed, total size, current file |
| 📋 **Queue** | View pending downloads, clear queue |
| 📁 **Files** | Recent uploaded files list |
| ⚙️ **Settings** | View current bot settings |
| 💻 **System** | CPU, RAM, disk usage bars |
| 📖 **Commands** | Quick reference for all bot commands |
| 🟢 **WebSocket** | Real-time updates every 3 seconds (REST fallback when WS is down) |

### API Endpoints

For advanced users or custom integrations:

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/health` | GET | No | Health check |
| `/api/status` | GET | Yes | Full bot state |
| `/api/queue` | GET | Yes | Queue details |
| `/api/stats` | GET | Yes | Statistics + system |
| `/api/settings` | GET | Yes | Current settings |
| `/api/cancel` | POST | Yes | Cancel current task |
| `/api/queue/clear` | POST | Yes | Clear queue |
| `/ws` | WebSocket | Yes | Real-time updates |

**Auth:** Pass token as `Authorization: Bearer <token>` header or `?token=<token>` query param.

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8080/api/status
```

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 📥 Commands Reference

### Download Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Show welcome message and main menu | `/start` |
| `/tupload` | Download files and upload to Telegram | `/tupload` → send link(s) |
| `/gdupload` | Download files and mirror to Google Drive | `/gdupload` → send link(s) |
| `/drupload` | Upload a local directory to Telegram | `/drupload` → send path |
| `/ytupload` | Download using YT-DLP (YouTube, etc.) | `/ytupload` → send URL |
| `/glupload` | Download image galleries via gallery-dl | `/glupload` → send URL |
| `/formats <url>` | List available yt-dlp formats (resolution/codec/size) for a video URL | `/formats https://youtu.be/...` |
| `/preview <url>` | Dry-run a gallery URL to see what would be downloaded, without downloading | `/preview https://imgur.com/a/...` |

### Queue & Control

| Command | Description |
|---------|-------------|
| `/queue` | View download queue and session stats |
| `/cancel` | Cancel the current running task |
| `/cancel_all` | Cancel task and clear the queue |

### Settings

| Command | Description |
|---------|-------------|
| `/settings` | Open interactive settings menu |
| `/setname <name>` | Set custom filename for next download |
| `/zipaswd <pass>` | Set password for zip compression |
| `/unzipaswd <pass>` | Set password for extraction |
| `/format` | Choose YT-DLP quality (1080p/720p/480p/audio) |
| `/speed` | Set bandwidth limit |

### Authentication

| Command | Description |
|---------|-------------|
| `/cookies` | Check YouTube authentication status |
| `/setcookies` | Upload a cookies.txt file |
| `/clearcookies` | Delete stored cookies file |

### Screenshot

| Command | Description |
|---------|-------------|
| `/screenshot [count]` | Manual screenshot generation (backup command) |
| Auto-SS | Enable via Settings → 📸 Auto-SS (extracts after upload) |

### Admin

| Command | Description |
|---------|-------------|
| `/admin` | Manage allowed users |
| `/admin add <id>` | Allow a user |
| `/admin remove <id>` | Remove a user |
| `/admin list` | Show allowed users |
| `/broadcast <ids>` | Send last file to multiple chats |
| `/stats` | Show lifetime task totals + system resource info (CPU, RAM, disk) |
| `/ping` | Check Telegram round-trip latency + bot uptime |
| `/status` | Show active task detail + download queue + transfer stats |
| `/restart` | Gracefully restart the bot (wrapper will respawn) |
| `/logs [N]` | Show last N log lines (default 30, max 100) |
| `/update` | Check for bot updates |
| `/help` | **Category-button help menu** (7 categories, 37 commands). Try `/help ytupload` for direct command help. |

---

## ⚙️ Settings Menu

Access via `/settings`. Here's what each option does:

### Upload Mode
- **Media** — Files stream inline (videos play in chat, photos display)
- **Document** — Files sent as raw downloads

### Video Settings
- **Split** — Split large videos into parts (Telegram 2GB limit)
- **Zip** — Archive videos instead of splitting
- **Convert** — Convert videos to MP4/MKV before upload
- **Quality** — High (slow, better quality) or Low (fast, smaller size)

### Caption
Choose the caption style for uploaded files:
- **Code** — Monospace `<code>filename</code>`
- **Bold** — `**filename**`
- **Italic** — `*filename*`
- **Underline** — `__filename__`
- **Regular** — Plain text

### Prefix / Suffix
Add custom text before/after the filename in captions.
Example: Set prefix to `🎬` → caption becomes `🎬 filename.mp4`

### Thumbnail
- Send any photo to the bot to set it as the default thumbnail
- Thumbnails apply to video and document uploads
- Use "Delete Thumbnail" to remove it

### Photo Upload Mode
- **Group** — Sends photos in batches of 10 (faster, uses media groups)
- **Single** — Sends photos one by one (slower, individual messages)

### Auto-Delete
- Automatically deletes the bot's status messages after a delay
- Set delay between 5-300 seconds
- Useful for keeping chats clean

### Auto-Screenshot
- Extracts screenshots from video after upload completes
- Enable/disable via toggle
- Set count (1-20 screenshots)
- Set watermark text (overlaid on each screenshot)
- Sent as media group (batch) to dump channel
- No re-download — extracts from local file before cleanup

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 🌐 Supported Sites

### Direct Downloads (aria2c)
Any HTTP/FTP link works. Examples:
- Direct file URLs: `https://example.com/file.zip`
- FTP links: `ftp://files.example.com/data.tar.gz`

### Torrent / Magnet Links (libtorrent)
Full torrent support via python-libtorrent:
- Magnet links: `magnet:?xt=urn:btih:...`
- Torrent files: `.torrent` uploads
- DHT peer discovery with 15 built-in trackers
- Resume data persists across restarts
- Real-time progress: speed, ETA, peers, seeds

### HLS / DASH Streams
Live and on-demand streaming protocols are fully supported via yt-dlp:
- HLS streams: `https://example.com/live/index.m3u8`
- DASH manifests: `https://example.com/video/manifest.mpd`
- Authenticated streams with tokens in URL
- Live streams (records until stream ends)

> 💡 **How it works:** yt-dlp downloads all `.ts` segments from the m3u8 playlist, merges them into a single `.mp4` file, then uploads to Telegram with streaming support.

### Video Platforms (YT-DLP)
2000+ sites including:
- YouTube (videos, shorts, playlists, live)
- Facebook, Twitter/X, TikTok
- Reddit, Vimeo, Dailymotion, Streamable
- Twitch, Kick, Rumble, Bilibili
- Crunchyroll, Funimation, TubiTV
- SoundCloud, Spotify, Bandcamp
- Odysee, PeerTube, Rutube, VK
- Pornhub, XVideos, XHamster, SpankBang
- And thousands more → [full list](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

### File Hosters
| Site | Notes |
|------|-------|
| Google Drive | Files and folders, shared links |
| Mega.nz | Requires `megatools` installed |
| Terabox | Direct links |
| Pixeldrain | Single files and lists |
| Mediafire | Automatic direct link extraction |
| GoFile.io | Free hosting, API-based, multi-file folders |
| Catbox.moe / Litterbox | Direct file links |
| StreamTape | Video hosting, direct extraction |

### Photo Galleries (gallery-dl)
| Site | Content |
|------|---------|
| Twitter / X | Timelines, likes, bookmarks |
| Pinterest | Boards, pins |
| Pixiv | Artworks, user galleries |
| DeviantArt | Art galleries |
| ArtStation | Portfolios |
| Flickr | Albums, photostreams |
| Reddit | Image subreddits |
| Tumblr | Blogs, tags |
| TikTok | Image posts |
| Bluesky | Posts with images |
| Danbooru, Gelbooru, Yande.re | Anime image boards |
| Furaffinity, Weasyl | Art communities |
| 100+ more | [full list](https://github.com/mikf/gallery-dl/blob/master/docs/supportedsites.md) |

### Telegram

| Link Type | Example | Bot Membership Required? |
|-----------|---------|--------------------------|
| **Public channel** | `https://t.me/MaximXStickers/1281` | ❌ No — works without joining |
| **Public group** | `https://t.me/publicgroup/12345` | ❌ No — works without joining |
| **Public slug** (new in 3.1.33) | `https://t.me/s/TelegramTips/123` | ❌ No — works without joining |
| **Private channel** | `https://t.me/c/1234567890/421` | ✅ Yes — bot must be a member |
| **Private group** | `https://t.me/c/1234567890/421` | ✅ Yes — bot must be a member |
| **Discussion thread** (new in 3.1.33) | `https://t.me/c/1234567890/421/789` | ✅ Yes — bot must be a member |

> 💡 **Public links** use the channel username (e.g., `t.me/username/msg`). **Private links** use numeric IDs (e.g., `t.me/c/123456/msg`). The bot can download from any public channel/group without being a member.

> 💡 **Slug form** (`t.me/s/...`) and **discussion thread** links (`t.me/c/.../msg/thread`) are now supported as of 3.1.33. The parser was ported from [xditya/GetRestrictedMessages](https://github.com/xditya/GetRestrictedMessages) and adapted to Pyrogram. `http://` and `telegram.me` mirrors are also accepted.

---

- You need a **separate Telegram API ID & hash** for the user client (same ones work, but some users prefer a separate app)
- Your Telegram account must be a member of the private channels you want to download from

> ⚠️ **Important:** Using a user session with automated tools may violate Telegram's ToS. Use at your own risk. The session is equivalent to logging in on a new device.

---

## ☁️ Google Drive Setup

To mirror files to Google Drive:

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the **Google Drive API**
4. Create **OAuth 2.0 credentials** (Desktop app)
5. Download the `credentials.json` file

### Step 2: Generate Token

Run this once to generate `token.pickle`:

```python
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os

SCOPES = ['https://www.googleapis.com/auth/drive']

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

with open('token.pickle', 'wb') as f:
    pickle.dump(creds, f)
```

### Step 3: Configure

```env
TOKEN_PICKLE_PATH=/path/to/token.pickle
```

### Step 4: Mount in Colab (if using Colab)

Check the "Mount Google Drive" option in the notebook, or mount manually:
```python
from google.colab import drive
drive.mount('/content/drive')
```

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 🎬 YouTube Authentication

YouTube may block downloads with "Sign in to confirm you're not a bot." Here's how to fix it:

### Method 1: PO Token Plugin (Automatic)

This is already included in `requirements.txt`. No setup needed — it generates tokens automatically.

### Method 2: Cookies File (Manual Fallback)

If PO tokens stop working:

1. Install a browser extension: [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) (Chrome) or [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) (Firefox)
2. Go to `youtube.com` (make sure you're logged in)
3. Click the extension icon → **Export** → saves `cookies.txt`
4. Upload the file to the bot:
   - Send `/setcookies`
   - Upload the `cookies.txt` file as a document

### Method 3: Browser Cookie Extraction

> ⚠️ **Browser cookie extraction has been removed** in v3.1.45. Use PO tokens (auto-generated) or upload `cookies.txt` manually via `/setcookies`.

### Check Status

Send `/cookies` to see which authentication method is active.

---

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 🎬 Demos

Real-world examples showing exactly what you send and what the bot does.

### Demo 1: Download a Single File

The simplest use case — download a file and upload it to Telegram.

```
You:   /tupload

Bot:   ⚡ Send Download Link(s) 🔗
       📋 Follow The Pattern Below:
       https://example.com/file1.mp4
       https://example.com/file2.mp4
       [Custom Name.mp4]
       {Zip Password}
       (Unzip Password)
       💡 Tips:
       • Multiple Links Supported
       • Use [] For Custom Filename
       • Use {} For Zip Password
       • Use () For Extract Password

You:   https://example.com/big-video.mp4

Bot:   🎯 Select Upload Type For Leech
       📄 Regular - Normal File Upload
       🗜️ Compress - Zip File Upload
       📂 Extract - Extract Archive Before Upload
       🔄 Unzip+Zip - Extract Then Compress

You:   [📄 Regular ✨]

Bot:   🚀 Initializing Task...
       Please Wait While I Prepare Your Download

       📥 Downloading
       ████████░░░░ 67% | 45.2 MB/s | ETA: 00:12 | 156 MB / 234 MB
       Engine: aria2c 🚀

       ... (download completes) ...

       📤 Uploading
       ████████████ 100% | 52.1 MB/s | Done: 234 MB
       Engine: Telegram 📤

       ✅ Task Complete
       📛 Name: big-video.mp4
       📦 Size: 234 MB
       📋 Files: 1
       ⏱️ Time: 00:45
```

### Demo 2: Download Multiple Files with Custom Name

Send multiple links at once. Use `[Custom Name]` to rename the file.

```
You:   /tupload

Bot:   ⚡ Send Download Link(s) 🔗
       ...

You:   https://site.com/episode01.mp4
       https://site.com/episode02.mp4
       https://site.com/episode03.mp4
       [My Anime S01]

Bot:   🎯 Select Upload Type For Leech

You:   [📄 Regular ✨]

Bot:   🚀 Initializing Task...

       📥 Downloading link 1/3
       ████████░░░░ 78% | 12.3 MB/s
       ...

       📥 Downloading link 2/3
       ████████░░░░ 45% | 11.8 MB/s
       ...

       📥 Downloading link 3/3
       ████████░░░░ 92% | 13.1 MB/s
       ...

       ✅ Task Complete
       📦 Size: 1.2 GB
       📋 Files: 3
       ⏱️ Time: 02:15
```

### Demo 3: Download YouTube Video

Use `/ytupload` for YouTube and other video platforms. Choose quality with `/format` first.

```
You:   /format

Bot:   🎬 YT-DLP Format Selection
       Current: bestvideo+bestaudio/best
       Choose the quality for video downloads:
       💡 Tip: Lower quality = faster download & smaller size

       [📺 1080p] [📺 720p]
       [📱 480p]  [📱 360p]
       [🎵 Audio Only]
       [❰ Back]

You:   [📺 720p]

Bot:   (callback acknowledged)

You:   /ytupload

Bot:   ⚡ Send Yt-Dlp Link(s) 🔗
       📋 Follow The Pattern Below:
       https://youtube.com/watch?v=xxxxx
       https://youtu.be/xxxxx
       [Custom Name.mp4]
       {Zip Password}
        💡 Supported Sites:
        • Youtube, Facebook
        • Twitter, Tiktok, And More...

You:   https://www.youtube.com/watch?v=dQw4w9WgXcQ

Bot:   🚀 Initializing Task...

       📥 Downloading
       ████████░░░░ 85% | 8.4 MB/s | ETA: 00:05
       Engine: YT-DLP 🏮

       ⏳ Please Wait...
       Merging YT-DLP Video...

       📤 Uploading
       ████████████ 100% | 45.2 MB/s
       Engine: Telegram 📤

       ✅ Task Complete
       📛 Name: Rick Astley - Never Gonna Give You Up.mp4
       📦 Size: 48.3 MB
       ⏱️ Time: 00:32
```

### Demo 4: Download Photo Gallery

Use `/glupload` for Twitter, Pinterest, Pixiv, and 100+ gallery sites.

```
You:   /glupload

Bot:   📸 Send Gallery Link(s) 🖼️
       ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
       📋 Follow The Pattern Below:
       https://twitter.com/username
       https://pinterest.com/user/board
       https://pixiv.net/users/123456
       [Custom Name]
       {Zip Password}
       ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
       🖼️ Supported Sites:
       ┣ Twitter / X, Pinterest
       ┣ Pixiv, DeviantArt, ArtStation, Flickr
       ┣ Reddit, Tumblr, Imgur, TikTok
       ┗ And 100+ more gallery sites

You:   https://www.pixiv.net/en/users/123456

Bot:   🚀 Initializing Gallery Download...
       Please Wait While I Prepare Your Download

       📸 Downloading Gallery Link 01
       ┏「████████░░░░」 » 67.2%
       ┠⚡ Speed: 5.2 MiB/s
       ┠🔧 Engine: gallery-dl 📸
       ┠⏳ ETA: —
       ┠⏱️ Elapsed: 00:12
       ┠✅ Done: 16 files (98.4 MiB)
       ┗📦 Total: 📥 image_016.jpg

       ✅ Task Complete
       📦 Size: 156 MiB
       📋 Files: 24
       ⏱️ Time: 00:28
```

### Demo 5: Download and Compress (Zip)

Download files and upload them as a zip archive. Set a password for encryption.

```
You:   /zipaswd mySecret123

Bot:   🔐 Zip Password Set Successfully

You:   /tupload

Bot:   ⚡ Send Download Link(s) 🔗
       ...

You:   https://site.com/project-files.tar.gz

Bot:   🎯 Select Upload Type For Leech

You:   [🗜️ Compress]

Bot:   🚀 Initializing Task...

       📥 Downloading
       ████████████ 100% | 15.6 MB/s
       Engine: aria2c 🚀

       🗜️ Zipping
       project-files.tar.gz
       ████████████ 100%

       📤 Uploading
       ████████████ 100% | 52.1 MB/s
       Engine: Telegram 📤

       ✅ Task Complete
       📦 Size: 89.2 MB
       ⏱️ Time: 00:18
```

### Demo 6: Extract Archive Before Upload

Download a zip/rar/7z file and extract it before uploading the contents.

```
You:   /tupload

Bot:   ⚡ Send Download Link(s) 🔗
       ...

You:   https://site.com/archive.zip

Bot:   🎯 Select Upload Type For Leech

You:   [📂 Extract]

Bot:   🚀 Initializing Task...

       📥 Downloading
       ████████████ 100% | 22.4 MB/s
       Engine: aria2c 🚀

       📂 Extracting
       archive.zip
       ████████████ 100%

       📤 Uploading
       📤 Uploading Split 1/5
       ████████████ 100% | 48.2 MB/s

       📤 Uploading Split 2/5
       ████████████ 100% | 51.3 MB/s
       ...

       ✅ Task Complete
       📋 Files: 5
       📦 Size: 234 MB
       ⏱️ Time: 00:42
```

### Demo 7: Download from Telegram

Download files from Telegram message links. **Public channels work without the bot being a member.**

**Public channel (no membership needed):**
```
You:   /tupload

Bot:   ⚡ Send Download Link(s) 🔗
       ...

You:   https://t.me/MaximXStickers/1281

Bot:   🎯 Select Upload Type For Leech

You:   [📄 Regular ✨]

Bot:   🚀 Initializing Task...

       📥 Downloading Link 01
       sticker.webm
       ████████░░░░ 56% | 34.7 MB/s
       Engine: Telegram 💬

       📤 Uploading
       ████████████ 100% | 48.9 MB/s
       Engine: Telegram 📤

       ✅ Task Complete
       📛 Name: sticker.webm
       📦 Size: 2.3 MB
       ⏱️ Time: 00:03
```

**Private channel (bot must be a member):**
```
You:   https://t.me/c/3780084791/421

Bot:   (same flow — works if bot is a member of that private channel)

       ❌ Error: Could Not Identify Telegram Media
       (if bot is NOT a member)
```

> ⚠️ **Private links** (`t.me/c/...`) require the bot to be a member of the channel/group. There is no workaround — this is enforced by Telegram's API. **Public links** (`t.me/username/...`) work without any membership.

### Demo 8: Mirror to Google Drive

Download a file and upload it to your Google Drive instead of Telegram.

```
You:   /gdupload

Bot:   ⚡ Send Download Link(s) 🔗
       📋 Follow The Pattern Below:
       https://example.com/file1.mp4
       ...
       💡 Tips:
       • Multiple Links Supported
       • Files Will Be Mirrored To Your Gdrive
       • Make Sure Gdrive Is Mounted

You:   https://site.com/big-backup.zip

Bot:   🎯 Select Upload Type For Mirror

You:   [📄 Regular ✨]

Bot:   🚀 Initializing Task...

       📥 Downloading
       ████████████ 100% | 18.3 MB/s
       Engine: aria2c 🚀

       ♻️ Uploading to Google Drive...
       ████████████ 100%

       ✅ Task Complete
       📛 Name: big-backup.zip
       📦 Size: 4.2 GB
       ⏱️ Time: 04:12
```

### Demo 9: Upload a Local Directory

Upload an entire folder from the server to Telegram.

```
You:   /drupload

Bot:   ⚡ Send Folder Path 📁
       📋 Example:
       /home/user/Downloads/myfolder
       💡 Note:
       • Provide Absolute Path To The Folder
       • Ensure The Bot Has Read Permissions

You:   /home/user/Downloads/my-photos

Bot:   🚀 Initializing Task...

       📤 Uploading photo 1/15
       ████████████ 100% | 52.1 MB/s

       📤 Uploading photo 2/15
       ████████████ 100% | 48.3 MB/s
       ...

       ✅ Task Complete
       📋 Files: 15
       📦 Size: 67.8 MB
       ⏱️ Time: 00:08
```

### Demo 10: Queue Multiple Tasks

Queue several download batches without waiting for each to finish.

```
You:   /tupload

Bot:   ⚡ Send Download Link(s) 🔗
       ...

You:   https://site.com/video1.mp4

Bot:   🎯 Select Upload Type For Leech

You:   [📄 Regular ✨]

Bot:   🚀 Initializing Task...
       (task starts downloading)

You:   /tupload

Bot:   ⚡ Send Download Link(s) 🔗
       ...

You:   https://site.com/video2.mp4

Bot:   🎯 Select Upload Type For Leech

You:   [📄 Regular ✨]

Bot:   (added to queue — will start after current task finishes)

       ... (first task completes) ...

       (second task starts automatically)

You:   /queue

Bot:   📋 Download Queue
       🔄 Active: video2.mp4
       📦 Links: 1
       📭 Queue is empty

       📈 Session Stats:
       • Completed: 1
       • Failed: 0
       • Downloaded: 450 MB
       • Uploaded: 450 MB
```

### Demo 11: Set Custom Thumbnail

Send a photo to set it as the default thumbnail for all uploads.

```
You:   (sends a photo)

Bot:   🖼️ Processing Thumbnail...
       ✅ Thumbnail Set Successfully

You:   /tupload

Bot:   ⚡ Send Download Link(s) 🔗
       ...

You:   https://site.com/movie.mp4

Bot:   🎯 Select Upload Type For Leech

You:   [📄 Regular ✨]

Bot:   🚀 Initializing Task...
       ...
       ✅ Task Complete
       (uploads now show your custom thumbnail)
```

### Demo 12: Set Prefix and Suffix

Customize how filenames appear in captions.

```
You:   /settings

Bot:   ⚙️ Bot Settings
       ┏📤 Upload: Media
       ┠✂️ Split: Split
       ┠🔄 Convert: Yes
       ┠📝 Caption: Regular
       ┠➕ Prefix: ❎
       ┠➕ Suffix: ❎
       ┠🖼️ Thumb: ❎
       ┠📸 Photos: Group
       ┠⏳ Auto-Delete: Off
       ┗📸 Auto-SS: OFF

       [📤 Media] [🎬 Video]
       [📝 Caption] [🖼️ Thumb]
       [➕ Prefix] [➕ Suffix]
       [📸 Photos: Group]
       [⏳ Auto-Delete: OFF]
       [📸 Auto-SS: OFF]
       [🔒 Close]

You:   [➕ Prefix]

Bot:   📝 Send prefix text:
       (This will be added before every filename)

You:   🎬

Bot:   ✅ Prefix Set: 🎬

You:   /settings

Bot:   ⚙️ Bot Settings
       ...
       ┠➕ Prefix: ✅
       ...

You:   [➕ Suffix]

Bot:   📝 Send suffix text:
       (This will be added after every filename)

You:   @MyChannel

Bot:   ✅ Suffix Set: @MyChannel

You:   /tupload → send link → select Regular
       ...
       (uploads now show: 🎬 filename.mp4 @MyChannel)
```

### Demo 13: Bandwidth Limiting

Limit download speed to avoid saturating your connection.

```
You:   /speed

Bot:   ⚡ Bandwidth Limiter
       Current Limit: Unlimited
       Set maximum download speed to avoid saturating your connection.
       This applies to aria2c and YT-DLP downloads.

       [🚀 Unlimited] [💨 50 MB/s]
       [⚡ 20 MB/s]   [🔌 10 MB/s]
       [🐢 5 MB/s]    [🐌 1 MB/s]
       [❰ Back]

You:   [🐢 5 MB/s]

Bot:   (callback acknowledged — speed limited to 5 MB/s)

You:   /tupload → send link
       ...
       (downloads now capped at 5 MB/s)
```

### Demo 14: Multi-User Setup

Allow friends or team members to use your bot.

```
You:   /admin

Bot:   👥 Admin Panel
       Allowed Users:
       None

       Commands:
       /admin add <user_id> — Allow a user
       /admin remove <user_id> — Deny a user
       /admin list — Show allowed users

You:   /admin add 987654321

Bot:   ✅ User 987654321 added to allowed list.

You:   /admin add 111222333

Bot:   ✅ User 111222333 added to allowed list.

You:   /admin list

Bot:   👥 Allowed Users:
       • 987654321
       • 111222333

(Now these users can also send commands to the bot)
```

### Demo 15: Broadcast Last Upload

Send the last uploaded file to multiple Telegram chats at once.

```
You:   /broadcast -1001234567890, -1009876543210, -100555444333

Bot:   📢 Broadcasting to 3 chats...

       📢 Broadcast Complete
       ✅ Success: 2
       ❌ Failed: 1
       📊 Total: 3
```

### Demo 16: Update the Bot

Check for new versions and update with one click.

```
You:   /update

Bot:   🔄 Checking for updates...

       🔄 Update Available!
       Current: abc1234
       Latest: def5678
       Behind: 3 commits

       📋 Changes:
       fix: batch photo upload parameter
       feat: add /glupload command
       docs: add comprehensive GUIDE.md

       [✅ Update Now] [❌ Cancel]

You:   [✅ Update Now]

Bot:   🔄 Updating...
       Pulling latest changes...
       Restarting bot...
       ✅ Update complete!
```

### Demo 17: YouTube Cookie Authentication

Fix "Sign in to confirm you're not a bot" errors.

```
You:   /cookies

Bot:   🍪 YT-DLP Authentication Status
       ❌ PO Token Plugin — not installed
       ⚠️ Cookies — not configured (fallback)

       How it works:
       1. PO Token Plugin (auto) — generates tokens in the background
       2. Cookies (manual fallback) — only needed if PO tokens stop working

       If YouTube still fails:
       Upload a cookies.txt file here as a backup...

You:   /setcookies

Bot:   🍪 Upload Cookies File
       Send me your cookies.txt file as a document (not as text).

       How to get it:
       Chrome / Edge / Brave:
       1. Install extension: Get cookies.txt LOCALLY
       2. Go to https://www.youtube.com (logged in)
       3. Click extension → Export → saves cookies.txt
       4. Upload that file here

You:   (uploads cookies.txt as document)

Bot:   🍪 Downloading cookies file...
       ✅ Cookies file saved!
       YouTube downloads should now work.
       Use /cookies to verify status.

You:   /cookies

Bot:   🍪 YT-DLP Authentication Status
       ✅ PO Token Plugin — auto-generating tokens (primary)
       ✅ Cookies file (uploaded) — /tmp/leechbot/sessions/cookies.txt
```

### Demo 18: Cancel a Running Task

Stop a download that's taking too long.

```
You:   /tupload → send huge link → select Regular

Bot:   🚀 Initializing Task...
       📥 Downloading
       ████░░░░░░░░ 32% | 2.1 MB/s | ETA: 45:00

You:   /cancel

Bot:   🚫 Task Cancelled

       🚫 Task Cancelled
       🔗 Source: Here
       🎯 Mode: Leech
       ⚠️ Reason: User cancelled the task
       ⏱️ Elapsed: 05:23
```

### Demo 19: Auto-Delete Status Messages

Keep your chat clean by auto-deleting bot messages.

```
You:   /settings

Bot:   ⚙️ Bot Settings
       ...
       ┗⏳ Auto-Delete: Off
       ...

You:   [⏳ Auto-Delete: OFF]

Bot:   ⏳ Auto-Delete Settings
       Status: OFF
       Delay: 30s

       [🔄 Toggle ON/OFF]
       [⏱️ Set Delay]
       [❰ Back]

You:   [🔄 Toggle ON/OFF]

Bot:   ✅ Auto-Delete: ON

You:   [⏱️ Set Delay]

Bot:   ⏱️ Enter delay in seconds (5-300):

You:   60

Bot:   ✅ Auto-delete delay set to 60 seconds.

(All bot status messages now auto-delete after 60 seconds)
```

### Demo 20: Error Recovery

The bot automatically retries failed downloads.

```
You:   /tupload → send link → select Regular

Bot:   🚀 Initializing Task...

       📥 Downloading
       ████░░░░░░░░ 23% | 5.2 MB/s

       (connection drops)

       ⚠️ Download failed, retrying... (attempt 2/3)

       📥 Downloading
       ████████░░░░ 67% | 4.8 MB/s

       (completes successfully)

       📤 Uploading
       ████████████ 100% | 52.1 MB/s

       ✅ Task Complete
        📦 Size: 234 MB
        ⏱️ Time: 01:12
```

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## ❓ Troubleshooting

### Bot doesn't respond to commands

- **Check credentials:** Make sure `API_ID`, `API_HASH`, `BOT_TOKEN`, `OWNER_ID`, and `DUMP_ID` are correct
- **Check bot is running:** Look for "LeechBot started successfully" in console
- **Check permissions:** The bot needs to be able to send messages to you and the DUMP_ID channel
- **Session file:** Delete `sessions/leechbot_session.session` and restart (forces fresh login)

### "Peer id invalid" error

- Make sure the bot is a **member** of the DUMP_ID channel/group
- Make sure the bot has **admin permissions** (at minimum: "Post Messages")
- Restart the bot — it resolves peers on startup

### YouTube downloads fail

- Run `/cookies` to check authentication status
- Try uploading a `cookies.txt` file via `/setcookies`
- Update yt-dlp: `pip install -U yt-dlp`

### "Flood wait" errors

- Telegram rate-limits bots that send too many messages too fast
- The bot handles this automatically (waits and retries)

### Google Drive upload fails

- Verify `token.pickle` exists and is valid
- Re-generate the token if it's expired (tokens expire after ~7 days of inactivity)

### gallery-dl unsupported URL

- Not all sites are supported. Check the [full list](https://github.com/mikf/gallery-dl/blob/master/docs/supportedsites.md)
- Manga/manhwa sites (Asura Scans, MangaDex, etc.) load images via JavaScript — gallery-dl can't handle those
- For unsupported sites, try `/tupload` with direct image URLs instead

### Upload fails with "request entity too large"

- Telegram has a **2GB file size limit**
- Enable video splitting in `/settings` → Video → Split
- Or use Document mode instead of Media mode

### Bot crashes on startup

- Check Python version: `python3 --version` (need 3.10+)
- Install missing dependencies: `pip install -r requirements.txt`
- Check the console output for specific error messages

---

## 📂 Project Structure

```
LeechBot/
├── leechbot.py             # Simple entry point: python3 leechbot.py
├── main.py                 # Colab deployer (Google Colab only)
├── config.py               # Central configuration (loads .env)
├── requirements.txt        # Python dependencies
├── .env                    # Your configuration (create from .env.example)
├── .env.example            # Example configuration
├── CHANGELOG.md            # Version history
├── GUIDE.md                # This file
├── README.md               # Project overview
├── leechbot/
│   ├── __init__.py         # Pyrogram client setup
│   ├── __main__.py         # Entry point (run with: python3 -m leechbot)
│   ├── aliases.py          # Command alias pre-processor
│   ├── commands/           # /command handlers (38 commands)
│   │   ├── __init__.py
│   │   ├── admin.py        # Admin & control commands
│   │   ├── autorename.py   # Auto-rename template commands
│   │   ├── downloads.py    # Download / upload commands
│   │   ├── options.py      # Quick option commands + aliases
│   │   ├── rss.py          # RSS subscription commands
│   │   ├── screenshot.py   # Video/PDF screenshot generator
│   │   ├── settings.py     # Settings / format / speed commands
│   │   ├── start_help.py   # /start and /help commands
│   │   └── status.py       # Status / stats / queue commands
│   ├── callbacks/          # Inline keyboard callback handlers
│   │   ├── __init__.py
│   │   ├── common.py       # Shared callback utilities
│   │   ├── dispatcher.py   # Main callback router
│   │   ├── navigation.py   # Help / about / start navigation
│   │   ├── settings.py     # Settings menus
│   │   ├── system.py       # System info callbacks
│   │   ├── update.py       # Update callback
│   │   └── upload.py       # Upload type / YT-DLP callbacks
│   ├── handlers.py         # Message handlers (URL, photo, text)
│   ├── updater.py          # Auto-update from GitHub
│   ├── debug.py            # Error reporting to Telegram
│   ├── downloader/
│   │   ├── aria2.py        # HTTP/FTP downloads
│   │   ├── torrent.py      # Magnet/torrent (libtorrent)
│   │   ├── gallery.py      # Photo galleries (gallery-dl)
│   │   ├── gdrive.py       # Google Drive downloads
│   │   ├── manager.py      # Download router & orchestrator
│   │   ├── mega.py         # Mega.nz downloads
│   │   ├── mediafire.py    # Mediafire downloads
│   │   ├── pixeldrain.py   # Pixeldrain downloads
│   │   ├── terabox.py      # Terabox downloads
│   │   ├── ytdl.py         # YouTube/video platform downloads
│   │   └── __init__.py
│   ├── uploader/
│   │   ├── telegram.py     # Telegram uploads (single + batch)
│   │   └── __init__.py
│   └── utility/
│       ├── converters.py   # Video conversion, archive handling
│       ├── handler.py      # Task handlers (leech, zip, unzip, logs)
│       ├── helper.py       # Utilities (settings, status bar, link detection)
│       ├── task_manager.py # Task scheduler & orchestrator
│       ├── variables.py    # Global state (BOT, Transfer, Queue, etc.)
│       └── __init__.py
├── notebooks/
│   └── LeechBot.ipynb      # Google Colab notebook
└── public/
    └── index.html           # Web dashboard (real-time monitoring)
```

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 🤝 Credits

- **Developer:** [Shinei Nouzen](https://t.me/Shineii86)
- **GitHub:** [Shineii86/LeechBot](https://github.com/Shineii86/LeechBot)
- **Updates:** [MaximXBots](https://t.me/MaximXBots)
- **Support:** [MaximXGroup](https://t.me/MaximXGroup)

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
