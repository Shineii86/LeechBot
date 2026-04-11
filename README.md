<div align="center">

<!-- Animated Logo Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=8B5CF6,06B6D4&height=200&section=header&text=LeechBot&fontSize=70&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Advanced%20Telegram%20File%20Transloader&descSize=20" />

<p align="center">
  <strong>A Pyrogram‑based Telegram Bot to transfer files / folders to Telegram and Google Drive, powered by Google Colab</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.3-8B5CF6?style=for-the-badge&logo=semver&logoColor=white" alt="Version" />
  <img src="https://img.shields.io/badge/License-MIT-06B6D4?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License" />

![Last Commit](https://img.shields.io/github/last-commit/Shineii86/LeechBot?style=for-the-badge)
![Repo Size](https://img.shields.io/github/repo-size/Shineii86/LeechBot?style=for-the-badge)
[![GitHub Stars](https://img.shields.io/github/stars/Shineii86/LeechBot?style=for-the-badge)](https://github.com/Shineii86/LeechBot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Shineii86/LeechBot?style=for-the-badge)](https://github.com/Shineii86/LeechBot/fork)

</div>

---

## 📑 **Table of Contents**

- [✨ What's New?](#-whats-new?)
- [🚀 Features](#-features)
- [🔗 Supported Links](#-supported-links)
- [💡 Benefits](#-benefits)
- [🛠️ Technology Stack](#️-technology-stack)
- [📥 How to Deploy](#-how-to-deploy)
- [📋 Commands & Usage](#-commands--usage)
- [🙏 Acknowledgements](#-acknowledgements)
- [📄 License & Disclaimer](#-license--disclaimer)
- [👤 Developer & Credits](#-developer--credits)

---

## ✨ **What's New?**

This release is a complete overhaul focused on **reliability, performance, and user experience**.

- ⏳ **Task Queue System** – Submit multiple links while a task is running; they'll be processed sequentially. Use `/queue` to view pending tasks.
- 💾 **Persistent Settings** – All user preferences (upload mode, video options, auto‑delete, speed limits) are saved to `settings.json` and restored on restart.
- 🔁 **Duplicate Detection** – Files already uploaded to the dump channel are automatically skipped (based on MD5 hash + size) to save time and bandwidth.
- 🔄 **Resume Interrupted Downloads** – Aria2c sessions are saved; if Colab disconnects, use `/resume` to continue unfinished downloads.
- ⚡ **Speed Limiter** – Set global download/upload speed limits (e.g., `10M`, `500K`) to avoid hitting Telegram rate limits.
- 🧹 **Auto‑Delete Messages** – Optional automatic deletion of bot messages after a configurable delay (5–300 seconds).
- 📖 **`/about` Command** – Displays bot version, developer info, updates channel, support group, and license.
- 🎨 **Professional UI** – All messages now use clean Telegram Markdown without custom Unicode styling, ensuring maximum compatibility and readability.

---

## 🚀 **Features**

| Feature                          | Description                                                                                     |
| -------------------------------- | ----------------------------------------------------------------------------------------------- |
| 📤 **Telegram Upload**           | Upload any file / folder to Telegram (supports streaming videos, documents, audio, photos).      |
| ☁️ **Google Drive Mirror**       | Mirror downloads directly to your Google Drive (requires mounted drive and token).               |
| 📁 **Directory Leech**           | Upload entire local directories recursively.                                                     |
| 🎬 **Video Converter**           | Convert videos to MP4 / MKV with FFmpeg or MoviePy fallback. GPU acceleration supported.         |
| ✂️ **Smart Splitting**           | Split files >2GB into chunks or zip archives to bypass Telegram limits.                          |
| 🗜️ **Archive Handling**          | Create or extract ZIP, RAR, 7z, TAR, GZ archives with password support.                          |
| 🖼️ **Auto Thumbnail**            | Generate thumbnails from videos or use custom images.                                            |
| 🔗 **Multi‑Link Support**        | Send multiple links at once; batch processing.                                                   |
| 🎛️ **Interactive Settings**      | On‑the‑fly configuration via inline buttons (upload mode, video options, caption style, etc.).   |
| 📊 **Real‑time Stats**           | Live progress bars with speed, ETA, percentage, and system resource usage.                       |
| 🔒 **Password Protection**       | Set ZIP and unzip passwords directly from the bot.                                               |
| 🏷️ **Custom Filename**           | Override output filenames with the `/setname` command or inline `[name]` syntax.                 |
| ⏳ **Task Queue**                | Queue links when bot is busy; view with `/queue`.                                                |
| 💾 **Persistent Settings**       | All settings survive restarts.                                                                   |
| 🔁 **Duplicate Detection**       | Skips already uploaded files automatically.                                                      |
| 🔄 **Resume Downloads**          | Resume interrupted aria2c downloads with `/resume`.                                              |
| ⚡ **Speed Limiter**             | Throttle download/upload speeds globally.                                                        |
| 🧹 **Auto‑Delete Messages**      | Clean up bot messages after a set delay.                                                         |

---

## 🔗 **Supported Links**

| Source              | Status        | Notes                                                       |
| ------------------- | ------------- | ----------------------------------------------------------- |
| Direct HTTP/HTTPS   | ✅ Full       | Resume supported via aria2c                                 |
| Google Drive        | ✅ Full       | Files, folders, shared drives (requires token)              |
| Telegram            | ✅ Full       | Public / private channel messages (bot must be in channel)  |
| YouTube / YT‑DLP    | ✅ Full       | 2000+ sites (YouTube, Facebook, Instagram, Twitter, etc.)   |
| Terabox             | ✅ Full       | Using third‑party API                                       |
| Mega.nz             | 🔜 Planned    | Coming soon                                                 |
| Torrent / Magnet    | ❌ Disabled   | Against Google Colab ToS                                    |

---

## 💡 **Benefits**

- ☁️ **No VPS Needed** – Runs entirely on **Google Colab** free tier.
- 🌐 **Blazing Speeds** – Google's backbone delivers up to **200 MiB/s download** and **30 MiB/s upload**.
- ♾️ **Unlimited Storage** – Telegram provides free, unlimited cloud storage.
- 🔧 **Easy Setup** – One‑click Colab notebook, no complex configurations.
- 🎯 **User‑Friendly** – Fully interactive with buttons, menus, and clear progress messages.

---

## 🛠️ **Technology Stack**

| Component           | Technology                                                              |
| ------------------- | ----------------------------------------------------------------------- |
| Bot Framework       | [Pyrogram](https://docs.pyrogram.org/) (MTProto API)                    |
| Download Manager    | [aria2c](https://aria2.github.io/) + [yt‑dlp](https://github.com/yt-dlp/yt-dlp) |
| Video Processing    | FFmpeg, MoviePy, GPUtil (GPU acceleration)                              |
| Archive Handling    | 7z, unrar, zip, tar                                                    |
| Cloud Environment   | Google Colab (Python 3.10+, Ubuntu 22.04)                               |
| Google Drive API    | google‑api‑python‑client                                                |
| Thumbnail Generator | PIL / Pillow                                                            |

---

## 📥 **How to Deploy**

### 1️⃣ **One‑Click Colab**

<a href="https://colab.research.google.com/github/Shineii86/LeechBot/blob/main/notebooks/LeechBot.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" height="40">
</a>

> The notebook includes both **Google Drive Auth** and **Bot Deployment** cells. Run them in order.

### 2️⃣ **Manual Setup (Local / VPS)**

```bash
git clone https://github.com/Shineii86/LeechBot.git
cd LeechBot
pip install -r requirements.txt
```

Create a `leechbot/credentials.json` file:

```json
{
  "API_ID": 12345,
  "API_HASH": "your_api_hash",
  "BOT_TOKEN": "your_bot_token",
  "USER_ID": 123456789,
  "DUMP_ID": -1001234567890
}
```

Run the bot:

```bash
python -m leechbot
```

### 3️⃣ **Google Drive Setup (Colab)**

Before running the deployer, use the **Google Drive Auth** cell to:
- Mount Google Drive
- Generate `/content/token.pickle` (required for mirroring)

---

## 📋 **Commands & Usage**

| Command         | Description                                                |
| --------------- | ---------------------------------------------------------- |
| `/start`        | Show welcome message and main menu                         |
| `/tupload`      | Leech files/folders to Telegram                            |
| `/gdupload`     | Mirror files/folders to Google Drive                       |
| `/drupload`     | Upload a local directory (provide absolute path)           |
| `/ytupload`     | Download using YT‑DLP (YouTube, etc.)                      |
| `/settings`     | Open interactive settings menu (owner only)                |
| `/queue`        | View pending tasks in the queue                            |
| `/resume`       | Resume interrupted downloads from previous session         |
| `/clear_resume` | Clear the saved aria2 session                              |
| `/setname`      | Set a custom filename for downloads                        |
| `/zipaswd`      | Set password for ZIP archives                              |
| `/unzipaswd`    | Set password for extracting archives                       |
| `/stats`        | Show system resource usage                                 |
| `/about`        | Display bot information, developer, and support links      |
| `/cancel`       | Cancel the current running task                            |
| `/help`         | Display all commands                                       |

**Inline Options (when sending links):**

- `[custom_name.mp4]` → Override filename
- `{zip_password}` → Password for ZIP creation
- `(unzip_password)` → Password for archive extraction

---

## 🙏 **Acknowledgements**

This project builds upon the excellent work of:

- **Original Base:** [XronTrix10/Telegram‑Leecher](https://github.com/XronTrix10/Telegram-Leecher)
- **Minor Fixes & Enhancements:** [kjeymax/Telegram‑Leecher](https://github.com/kjeymax/Telegram-Leecher)
- **Forked Inspiration:** [ehraz786/tgdl](https://github.com/ehraz786/tgdl)

Special thanks to the developers of **Pyrogram**, **aria2**, **yt‑dlp**, and **Google Colab** for making this possible.

---

## 📄 **License & Disclaimer**

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

> [!IMPORTANT]
> Using this bot for downloading copyrighted content without permission may violate laws.
> **Do not use it in a way that goes against Google Colab's Terms of Service**, such as running torrents or hosting web services.
> The developer assumes no liability for misuse.

---

## 👤 **Developer & Credits**

**Shinei Nouzen**  
- GitHub: [Shineii86](https://github.com/Shineii86)
- Telegram: [@Shineii86](https://t.me/Shineii86)

**Updates & Support:**  
- Channel: [@MaximXBots](https://t.me/MaximXBots)
- Group: [@MaximXGroup](https://t.me/MaximXGroup)

---

<div align="center">

<a href="https://github.com/Shineii86/LeechBot">
  <img src="https://github.com/Shineii86/AniPay/blob/main/Source/Banner6.png" alt="Banner">
</a>

*For inquiries or collaborations*

[![Telegram Badge](https://img.shields.io/badge/-Telegram-2CA5E0?style=flat&logo=Telegram&logoColor=white)](https://telegram.me/Shineii86)
[![Instagram Badge](https://img.shields.io/badge/-Instagram-C13584?style=flat&logo=Instagram&logoColor=white)](https://instagram.com/ikx7.a)
[![Pinterest Badge](https://img.shields.io/badge/-Pinterest-E60023?style=flat&logo=Pinterest&logoColor=white)](https://pinterest.com/ikx7a)
[![Gmail Badge](https://img.shields.io/badge/-Gmail-D14836?style=flat&logo=Gmail&logoColor=white)](mailto:ikx7a@hotmail.com)

<sup><b>Copyright © 2026 <a href="https://telegram.me/Shineii86">Shinei Nouzen</a> All Rights Reserved</b></sup>

![Last Commit](https://img.shields.io/github/last-commit/Shineii86/LeechBot?style=for-the-badge)

<sub>Pull Requests and Contributions are warmly welcomed</sub>

</div>
