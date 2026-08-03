> [!IMPORTANT]
> **🧪 This repository is currently in BETA / Active Development.**
>
> Things may break, features may change, and bugs may appear. If you deploy this bot and run into an error, a crash, or unexpected behavior:
>
> 1. **Open an Issue** → [github.com/Shineii86/LeechBot/issues/new](https://github.com/Shineii86/LeechBot/issues/new) (please paste `/logs 50` output and the failing link)
> 2. **Join the Telegram Support Group** → [MaximXGroup](https://t.me/MaximXGroup)
> 3. **DM the Developer** → [Shinei Nouzen](https://t.me/Shineii86)
>
> Bug reports with logs get fixed fastest. Feature requests go to [GitHub Discussions](https://github.com/Shineii86/LeechBot/discussions) 💡.
>

<div align="center">

<!-- Animated Logo Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&height=300&color=gradient&text=𝙇𝙚𝙚𝙘𝙝%20𝘽𝙤𝙩&fontAlignY=30&fontSize=100&desc=𝖠𝖽𝗏𝖺𝗇𝖼𝖾𝖽%20𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆%20𝖥𝗂𝗅𝖾%20𝖳𝗋𝖺𝗇𝗌𝗅𝑜𝖺𝖽𝖾𝗋&descSize=30" />

<p align="center">
  <strong>A Pyrogram‑based Telegram Bot to transfer files / folders to Telegram and Google Drive, powered by Google Colab</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.4.0-8B5CF6?style=for-the-badge&logo=semver&logoColor=white" alt="Version" />
  <img src="https://img.shields.io/badge/License-MIT-06B6D4?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License" />

![Last Commit](https://img.shields.io/github/last-commit/Shineii86/LeechBot?style=for-the-badge)
![Repo Size](https://img.shields.io/github/repo-size/Shineii86/LeechBot?style=for-the-badge)
[![GitHub Stars](https://img.shields.io/github/stars/Shineii86/LeechBot?style=for-the-badge)](https://github.com/Shineii86/LeechBot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Shineii86/LeechBot?style=for-the-badge)](https://github.com/Shineii86/LeechBot/fork)

</div>

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 📑 **Table of Contents**

- [📖 Complete User Guide](GUIDE.md) ← **Start here if you're new**
- [🗺️ Roadmap](ROADMAP.md)
- [✨ What's New?](#-whats-new-in-v340)
- [🚀 Features](#-features)
- [🔗 Supported Sources](#-supported-sources)
- [🌐 Web Dashboard](#-web-dashboard)
- [📥 How to Deploy](#-how-to-deploy)
- [📋 Commands](#-commands)
- [🛠️ Technology Stack](#️-technology-stack)
- [⚠️ Disclaimer](#-disclaimer)
- [🙏 Acknowledgements](#-acknowledgements)
- [📄 License](#-license)
- [🫂 Updates & Support](#-updates--support)
- [👤 Developer & Credits](#-developer--credits)

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## ✨ What's New in v3.4.0

### 🎬 Anime Downloader Removed
- Complete removal of anime downloading subsystem (MiruroAPI, /anime command, inline keyboard UI)
- Removed ANIME_API_URL configuration
- Cleaned all anime references from codebase and documentation

### 🔧 Dependency Fixes
- Resolved Pillow/moviepy version conflict (Pillow>=12.3.0 vs moviepy requires <12.0)
- Upgraded all dependencies to latest versions (kurigram, yt-dlp, curl_cffi, gallery-dl, aiohttp)

## 📸 Auto-Screenshot After Upload
- Screenshots extracted from local file after video upload — no re-download
- Enable via Settings → 📸 Auto-SS: ON/OFF
- Configurable count (1-20) and watermark text
- Sent as media group (batch) to dump channel
- Works for all upload sources (aria2, ytdl, gallery-dl, etc.)

### 📖 Shinobu-style Help Menu
- `/start` → random photo + welcome text + category grid
- `/help` → random photo + category navigation with smooth photo transitions
- Module details with `❖` command formatting

### 📊 Permanent System Info
- CPU, RAM, Disk, Network, Uptime always visible in progress bar

### ✏️ Auto-Rename Templates
- `/autorename <template>` — set custom filename templates with placeholders
- Supports `{season}`, `{episode}`, `{quality}`, `{audio}`, `{title}`, `{chapter}`

> 📋 **Full history:** [CHANGELOG.md](CHANGELOG.md) • **37 commands across 7 categories**

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 📤 **Telegram Upload** | Upload any file/folder to Telegram (video, audio, document, photo) |
| ☁️ **Google Drive Mirror** | Mirror downloads directly to Google Drive |
| 📡 **HLS/DASH Streams** | Download `.m3u8` and `.mpd` streaming URLs |
| 📁 **Directory Leech** | Upload entire local directories recursively |
| 🎬 **Video Converter** | Convert to MP4/MKV with FFmpeg (GPU accelerated) |
| ✂️ **Smart Splitting** | Split files >2GB into chunks |
| 🗜️ **Archive Handling** | Create/extract ZIP, RAR, 7z, TAR, GZ with password support |
| 🖼️ **Auto Thumbnail** | Generate from video or use custom images |
| 📸 **Photo Upload Mode** | Group (batch of 10) or Single (one by one) |
| 📋 **Download Queue** | Queue multiple downloads, process sequentially |
| 🎬 **Format Selection** | Choose YT-DLP quality per-session |
| ⚡ **Bandwidth Control** | Limit download speed |
| 📢 **Broadcast** | Send files to multiple chats |
| 👥 **Multi-User** | Admin panel to allow/deny users |
| 🔄 **Auto-Retry** | Automatic retry on download failures |
| 🔒 **Password Protection** | ZIP/unzip passwords |
| 🏷️ **Custom Filename** | `/setname`, `/autorename` templates, or inline `[name]` syntax |
| ⏳ **Auto-Delete** | Configurable auto-delete for bot messages |
| 🎬 **YouTube PO Tokens** | Auto-generated — no manual cookie setup |
| 📸 **Photo Galleries** | Twitter, Pinterest, Pixiv via gallery-dl |
| 🌐 **Web Dashboard** | Real-time browser monitoring and control |
| 📸 **Auto-Screenshot** | Extract screenshots from video after upload, send as batch to dump channel |

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 🔗 Supported Sources

### 📥 Download From

| Source | Method | Status |
|--------|--------|--------|
| Direct HTTP/HTTPS/FTP | aria2c | ✅ Full — resume supported |
| Torrent / Magnet | libtorrent | ✅ Full — DHT, resume, progress |
| HLS / DASH (`.m3u8` / `.mpd`) | yt-dlp | ✅ Full — live + VOD |
| YouTube, Facebook | yt-dlp | ✅ 2000+ sites |
| Kick, Rumble, Bilibili, Twitch | yt-dlp | ✅ |
| SoundCloud, Spotify, Bandcamp | yt-dlp | ✅ |
| Crunchyroll, TubiTV, Odysee | yt-dlp | ✅ |
| Reddit, VK, Dailymotion, Vimeo | yt-dlp | ✅ |
| Google Drive | GDrive API | ✅ Files, folders, shared drives |
| Twitter, Pinterest | gallery-dl | ✅ 100+ gallery sites |
| Pixiv, DeviantArt, ArtStation | gallery-dl | ✅ Art galleries |
| Mega.nz | megatools | ✅ Files + folders, async |
| Terabox | API | ✅ |
| Pixeldrain | API | ✅ Single files + lists |
| Mediafire | Scraping | ✅ Auto-extracted direct links |
| GoFile.io | API | ✅ Folders, multi-file |
| Catbox.moe / Litterbox | Direct | ✅ Direct download |
| StreamTape | Extraction | ✅ Video links |

### 📤 Upload To

| Destination | Method |
|-------------|--------|
| Telegram | Pyrogram (single + batch photo) |
| Google Drive | GDrive API |

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 🌐 Web Dashboard

Real-time browser dashboard runs alongside the bot on port `8080`.

| Feature | Description |
|---------|-------------|
| 📊 Status Cards | Idle/active, downloads, uploads, tasks |
| 🔄 Active Task | Mode, engine, progress, speed, ETA, total size |
| 📋 Queue | View pending, clear queue |
| 📁 Files | Recent uploads list |
| ⚙️ Settings | Current bot configuration |
| 💻 System | CPU, RAM, disk usage |
| 📖 Commands | Quick reference for all 37 commands |
| 🟢 WebSocket | Real-time updates every 3s |

```bash
# Access
http://your-server:8080/dashboard

# API
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8080/api/status
```

📖 [Full dashboard guide](GUIDE.md#-web-dashboard)

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 📥 How to Deploy

### 1️⃣ One‑Click Colab

<a href="https://colab.research.google.com/github/Shineii86/LeechBot/blob/main/notebooks/LeechBot.ipynb">
  <img src="https://user-images.githubusercontent.com/125879861/255389999-a0d261cf-893a-46a7-9a3d-2bb52811b997.png" alt="Open In Colab" width="200px">
</a>

1. Open notebook → fill credentials (or use Colab Secrets)
2. **Runtime → Run all** — bot starts automatically
3. Send `/start` on Telegram

### 2️⃣ Docker

```bash
git clone https://github.com/Shineii86/LeechBot.git
cd LeechBot

# Create .env with your credentials
cp .env.example .env
nano .env

# Build and run
docker compose up -d
```

### 3️⃣ Railway (One-Click)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/Shineii86/LeechBot)

1. Click the button above → set environment variables → deploy
2. Bot starts automatically, web dashboard on port 8080

### 4️⃣ Fly.io

```bash
# Install flyctl: https://fly.io/docs/hands-on/install-flyctl/
fly launch --copy-config --name leechbot
fly secrets set API_ID=xxx API_HASH=xxx BOT_TOKEN=xxx OWNER_ID=xxx DUMP_ID=xxx
fly scale memory 512
fly deploy
```

### 5️⃣ Render

1. Push repo to GitHub
2. Go to [render.com](https://render.com) → New → Blueprint Instance
3. Select your repo → it auto-detects `render.yaml`
4. Add environment variables → Deploy

### 6️⃣ VPS / Local

```bash
git clone https://github.com/Shineii86/LeechBot.git
cd LeechBot
pip install -r requirements.txt

# Create .env with your credentials
cp .env.example .env
nano .env

# Either run command works
python3 leechbot.py
# or
python3 -m leechbot
```

### 7️⃣ Oracle Cloud Free Tier (Free Forever)

1. Create a free ARM instance at [cloud.oracle.com](https://cloud.oracle.com) (4 cores, 24GB RAM)
2. SSH into the instance
3. Follow the **VPS / Local** steps above
4. Run with `screen` or `tmux` to keep it alive

### 8️⃣ Heroku

```bash
heroku create leechbot
heroku buildpacks:add heroku/python
heroku config:set API_ID=xxx API_HASH=xxx BOT_TOKEN=xxx OWNER_ID=xxx DUMP_ID=xxx
git push heroku main
heroku ps:scale worker=1
```

### System Dependencies

```bash
# Ubuntu/Debian
sudo apt install -y ffmpeg aria2 p7zip-full unrar unzip python3-libtorrent megatools

# macOS
brew install ffmpeg aria2 p7zip megatools

# Conda (libtorrent)
conda install -c conda-forge libtorrent
```

> 💡 Docker users: all dependencies (including libtorrent and megatools) are included in the image — no manual install needed.

📖 [Full setup guide](GUIDE.md#-installation)

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 📋 Commands

All bot commands are organized into categories in the **interactive `/help`** menu.

| Category | Commands | Usage |
|----------|----------|-------|
| **📥 Downloads** | 10 | `tupload`, `gdupload`, `drupload`, `ytupload`, `glupload`, `setname`, `format`, `formats`, `preview`, `speed` |
| **🗂 Files** | 5 | `zipaswd`, `unzipaswd`, `queue`, `cancel`, `cancel_all` |
| **⚙️ Status & Settings** | 7 | `settings`, `status`, `stats`, `logs`, `ping`, `restart`, `update` |
| **🍪 Cookies** | 3 | `cookies`, `setcookies`, `clearcookies` |
| **📸 Screenshot** | 2 | `screenshot`, `setwm` |
| **🛠 Admin** | 2 | `admin`, `broadcast` |
| **📰 RSS** | 4 | `rss_add`, `rss_list`, `rss_remove`, `rss_check` |

> 💡 **Try it on Telegram:** Send `/help` — the bot will show category buttons.
> Type `/help <command>` (e.g. `/help ytupload`) for direct help without navigating the menu.

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | [Kurigram](https://github.com/KurimuzonAkworker) (Pyrogram fork) |
| Downloads | [aria2c](https://aria2.github.io/) + [yt-dlp](https://github.com/yt-dlp/yt-dlp) + [gallery-dl](https://github.com/mikf/gallery-dl) |
| YouTube Auth | [bgutil-ytdlp-pot-provider](https://github.com/Brainicism/bgutil-ytdlp-pot-provider) |
| Video Processing | FFmpeg, MoviePy, GPUtil |
| Archives | 7z, unrar, zip, tar |
| Cloud | Google Colab / VPS |
| Dashboard | aiohttp (REST + WebSocket) + Tailwind CSS |
| Google Drive | google-api-python-client |
| Images | PIL / Pillow |

### 📁 Project Structure

```
LeechBot/
├── leechbot.py              # Simple entry point: python3 leechbot.py
├── main.py                  # Colab deployer
├── config.py                # Configuration (env vars, paths)
├── requirements.txt         # Dependencies
├── AGENTS.md                # AI agent instructions
├── ARCHITECTURE.md          # Technical deep dive
├── CONTRIBUTING.md          # Contribution guide
├── GUIDE.md                 # Complete user guide
├── CHANGELOG.md             # Version history
├── .github/
│   └── copilot-instructions.md
├── .cursorrules / .clinerules / .windsurfrules
├── pyproject.toml           # Tooling config
├── .editorconfig            # Formatting rules
├── leechbot/
│   ├── __init__.py          # Pyrogram client
│   ├── __main__.py          # Entry point
│   ├── aliases.py           # Command alias pre-processor
│   ├── commands/            # /command handlers (38 commands)
│   │   ├── __init__.py
│   │   ├── admin.py         # Admin & control commands
│   │   ├── autorename.py    # Auto-rename template commands
│   │   ├── downloads.py     # Download / upload commands
│   │   ├── options.py       # Quick option commands + aliases
│   │   ├── rss.py           # RSS subscription commands
│   │   ├── screenshot.py    # Video/PDF screenshot generator
│   │   ├── settings.py      # Settings / format / speed commands
│   │   ├── start_help.py    # /start and /help commands
│   │   └── status.py        # Status / stats / queue commands
│   ├── callbacks/           # Button callbacks
│   │   ├── __init__.py
│   │   ├── common.py        # Shared callback utilities
│   │   ├── dispatcher.py    # Main callback router
│   │   ├── navigation.py    # Help / about / start navigation
│   │   ├── settings.py      # Settings menus
│   │   ├── system.py        # System info callbacks
│   │   ├── update.py        # Update callback
│   │   └── upload.py        # Upload type / YT-DLP callbacks
│   ├── handlers.py          # Message handlers
│   ├── debug.py             # Error reporting
│   ├── updater.py           # Auto-update
│   ├── downloader/
│   │   ├── aria2.py         # HTTP/FTP downloads
│   │   ├── torrent.py       # Magnet/torrent (libtorrent)
│   │   ├── ytdl.py          # YouTube, 2000+ sites
│   │   ├── gallery.py       # Photo galleries (100+ sites)
│   │   ├── gdrive.py        # Google Drive
│   │   ├── mega.py          # Mega.nz
│   │   ├── terabox.py       # Terabox
│   │   ├── pixeldrain.py    # Pixeldrain
│   │   ├── mediafire.py     # Mediafire
│   │   ├── gofile.py        # GoFile.io
│   │   ├── catbox.py        # Catbox.moe
│   │   ├── streamtape.py    # StreamTape
│   │   └── manager.py       # Download router
│   ├── uploader/
│   │   └── telegram.py      # Upload with progress
│   ├── web/
│   │   └── server.py        # Dashboard API + WebSocket
│   └── utility/
│       ├── variables.py     # Global state
│       ├── handler.py       # Task handlers
│       ├── helper.py        # UI, links, formatting
│       ├── converters.py    # Video/archive conversion
│       ├── rss_manager.py   # RSS subscription manager
│       └── task_manager.py  # Task orchestrator
└── notebooks/
    └── LeechBot.ipynb        # Colab notebook
```

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## ⚠️ Disclaimer

> [!WARNING]
> **You Should NOT use it as it goes against Google Colab's Policy**
> Resources in Colab are prioritized for interactive use cases. We prohibit actions associated with `bulk compute`, actions that negatively impact others, as well as actions associated with bypassing our policies. The following are disallowed from Colab runtime:
> - [X] File Hosting, Media Serving, Or Other Web Service Offerings Not Related To Interactive Compute With Colab
> - [X] Downloading Torrents Or Engaging In Peer-to-peer File-sharing
> - [X] Using A Remote Desktop Or Ssh
> - [X] Connecting To Remote Proxies
> - [X] Mining Cryptocurrency
> - [X] Running Denial-of-service Attacks
> - [X] Password Cracking
> 
> <sub>Source: [Colab FAQ](https://research.google.com/colaboratory/faq.html) </sub>


## 🙏 Acknowledgements

- **Original Base:** [XronTrix10/Telegram‑Leecher](https://github.com/XronTrix10/Telegram-Leecher)
- **Minor Fixes:** [kjeymax/Telegram‑Leecher](https://github.com/kjeymax/Telegram-Leecher)
- **Forked Inspiration:** [ehraz786/tgdl](https://github.com/ehraz786/tgdl)

> [!NOTE]
> Special thanks to **Pyrogram**, **aria2**, **yt-dlp**, **gallery-dl**, and **Google Colab**.

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

> [!IMPORTANT]
> Using this bot for downloading copyrighted content without permission may violate laws.
> Do not violate Google Colab's Terms of Service.
> The developer assumes no liability for misuse.

<p align="center">
  <img src="assets/divider.svg" width="600" alt="---divider---"/>
</p>

## 🫂 Updates & Support

<div align="center">

##### Updates Channel
<a href="https://t.me/MaximXBots"><img src="https://telegramcard.vercel.app/?username=MaximXBots&theme=light" alt="Channel"></a>

##### Support Group
<a href="https://t.me/MaximXGroup"><img src="https://telegramcard.vercel.app/?username=MaximxGroup&theme=light" alt="Group"></a>

</div>

## 💕 Loved My Work?

🚨 [Follow me on GitHub](https://github.com/Shineii86)

⭐ [Give a star to this Project](https://github.com/Shineii86/LeechBot)

<div align="center">

<a href="https://github.com/Shineii86/LeechBot">
<img src="https://github.com/Shineii86/AniPay/blob/main/Source/Banner6.png" alt="Banner">
</a>

<i>~ For inquiries or collaborations</i>

[![Telegram Badge](https://img.shields.io/badge/-Telegram-2CA5E0?style=flat&logo=Telegram&logoColor=white)](https://telegram.me/Shineii86 "Contact on Telegram")
[![Instagram Badge](https://img.shields.io/badge/-Instagram-C13584?style=flat&logo=Instagram&logoColor=white)](https://instagram.com/ikx7.a "Follow on Instagram")
[![Pinterest Badge](https://img.shields.io/badge/-Pinterest-E60023?style=flat&logo=Pinterest&logoColor=white)](https://pinterest.com/ikx7a "Follow on Pinterest")
[![Gmail Badge](https://img.shields.io/badge/-Gmail-D14836?style=flat&logo=Gmail&logoColor=white)](mailto:ikx7a@hotmail.com "Send an Email")

<sup><b>Copyright © <a href="https://telegram.me/Shineii86">Shinei Nouzen</a> All Rights Reserved</b></sup>

![Last Commit](https://img.shields.io/github/last-commit/Shineii86/LeechBot?style=for-the-badge)

<sub>Pull Requests And Contributions Are Warmly Welcomed</sub>

</div>
