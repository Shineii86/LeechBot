<div align="center">

<!-- Animated Logo Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=8B5CF6,06B6D4&height=200&section=header&text=LeechBot&fontSize=70&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Advanced%20Telegram%20File%20Transloader&descSize=20" />

<p align="center">
  <strong>A Pyrogram‑based Telegram Bot to transfer files / folders to Telegram and Google Drive, powered by Google Colab</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.2-8B5CF6?style=for-the-badge&logo=semver&logoColor=white" alt="Version" />
  <img src="https://img.shields.io/badge/License-MIT-06B6D4?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License" />

![Last Commit](https://img.shields.io/github/last-commit/Shineii86/LeechBot?style=for-the-badge)
![Repo Size](https://img.shields.io/github/repo-size/Shineii86/LeechBot?style=for-the-badge)
[![GitHub Stars](https://img.shields.io/github/stars/Shineii86/LeechBot?style=for-the-badge)](https://github.com/Shineii86/LeechBot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Shineii86/LeechBot?style=for-the-badge)](https://github.com/Shineii86/LeechBot/fork)

</div>

---

## 📑 **Table of Contents**

- [✨ What's New?](#-whats-new)
- [🚀 Features](#-features)
- [🔗 Supported Links](#-supported-links)
- [💡 Benefits](#-benefits)
- [🛠️ Technology Stack](#️-technology-stack)
- [📥 How to Deploy](#-how-to-deploy)
- [📋 Commands & Usage](#-commands--usage)
- [🆚 Changelog – Old vs New](#-changelog--old-vs-new)
- [🙏 Acknowledgements](#-acknowledgements)
- [📄 License & Disclaimer](#-license--disclaimer)
- [👤 Developer & Credits](#-developer--credits)

---

## ✨ **What's New?**

This version of **LeechBot** is a complete rewrite with a focus on **clean code, professional UI, and enhanced reliability**.

- 🧹 **Removed Custom Styling** – No more Unicode small‑caps; messages now use standard Telegram Markdown for maximum compatibility and readability.
- ⏳ **Auto‑Delete Messages** – Optional automatic deletion of bot messages after a configurable delay, keeping your chat clean.
- ⚡ **Refactored Codebase** – Clean, modular, and well‑documented Python code for easy customisation.
- 📦 **Expanded Link Support** – YT‑DLP, Terabox, Mega (coming soon) and improved Google Drive handling.
- 🧠 **Smarter Progress Bars** – Real‑time speed, ETA, and percentage tracking for both downloads and uploads.

---

## 🚀 **Features**

| Feature                          | Description                                                                                     |
| -------------------------------- | ----------------------------------------------------------------------------------------------- |
| 📤 **Telegram Upload**           | Upload any file / folder to Telegram (supports streaming videos, documents, audio, photos).      |
| ☁️ **Google Drive Mirror**       | Mirror downloads directly to your Google Drive (mounted drive).                                  |
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
| ⏳ **Auto‑Delete Messages**      | Automatically delete bot messages after a set delay (configurable in settings).                  |

---

## 🔗 **Supported Links**

| Source              | Status        | Notes                                                       |
| ------------------- | ------------- | ----------------------------------------------------------- |
| Direct HTTP/HTTPS   | ✅ Full       | Resume supported via aria2c                                 |
| Google Drive        | ✅ Full       | Files, folders, shared drives (auto‑auth)                   |
| Telegram            | ✅ Full       | Public / private channel messages (requires bot in channel) |
| YouTube / YT‑DLP    | ✅ Full       | 2000+ sites (YouTube, Facebook, Instagram, Twitter, etc.)   |
| Terabox             | ✅ Full       | Using third‑party API                                       |
| Mega.nz             | 🔜 Planned    | Coming soon                                                 |
| Torrent / Magnet    | ❌ Disabled   | Against Google Colab ToS                                    |

---

## 💡 **Benefits**

- ☁️ **No VPS Needed** – Runs entirely on **Google Colab** free tier.
- 🌐 **Blazing Speeds** – Google’s backbone delivers up to **200 MiB/s download** and **30 MiB/s upload**.
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

<a href="https://colab.research.google.com/drive/12hdEqaidRZ8krqj7rpnyDzg1dkKmvdvp?usp=sharing">
  <img src="https://user-images.githubusercontent.com/125879861/255389999-a0d261cf-893a-46a7-9a3d-2bb52811b997.png" alt="Open In Colab" width="200px">
</a>

### 2️⃣ **Manual Setup (Local / VPS)**

```bash
git clone https://github.com/Shineii86/LeechBot.git
cd LeechBot
pip install -r requirements.txt
```

Create a `credentials.json` file with your API details:

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

### 3️⃣ **Detailed Instructions**

- 📘 [Full Deployment Guide](https://github.com/XronTrix10/Telegram-Leecher/wiki/INSTRUCTIONS) (original base)
- 🎥 [YouTube Tutorial](https://www.youtube.com/watch?v=6LvYd-oO3U0)

---

## 📋 **Commands & Usage**

| Command       | Description                                                |
| ------------- | ---------------------------------------------------------- |
| `/start`      | Show welcome message and main menu                         |
| `/tupload`    | Leech files/folders to Telegram                            |
| `/gdupload`   | Mirror files/folders to Google Drive                       |
| `/drupload`   | Upload a local directory (provide absolute path)           |
| `/ytupload`   | Download using YT‑DLP (YouTube, etc.)                      |
| `/settings`   | Open interactive settings menu (owner only)                |
| `/setname`    | Set a custom filename for downloads                        |
| `/zipaswd`    | Set password for ZIP archives                              |
| `/unzipaswd`  | Set password for extracting archives                       |
| `/stats`      | Show system resource usage                                 |
| `/cancel`     | Cancel the current running task                            |
| `/help`       | Display all commands                                       |

**Inline Options:**  
When sending links, you can append:

- `[custom_name.mp4]` → Override filename  
- `{zip_password}` → Password for ZIP creation  
- `(unzip_password)` → Password for archive extraction

---

## 🆚 **Changelog – Old vs New**

| **Aspect**             | **Telegram Leecher**                 | **LeechBot**                                         |
| ---------------------- | ------------------------------------ | ---------------------------------------------------- |
| **UI / UX**            | Plain text messages                  | Clean, professional Markdown with inline menus       |
| **Auto‑Delete**        | None                                 | Configurable auto‑delete for bot messages            |
| **Code Structure**     | Monolithic, less documented          | Modular, fully typed, clean docstrings               |
| **Video Converter**    | Basic FFmpeg                         | GPU‑accelerated FFmpeg + MoviePy fallback            |
| **Archive Support**    | Limited to ZIP                       | Full 7z, RAR, TAR, GZ, multipart extraction          |
| **Settings Menu**      | None                                 | Interactive inline menu with toggle switches         |
| **Thumbnail**          | Manual only                          | Auto‑generate from video, YT‑DLP thumb support       |
| **Link Support**       | HTTP, GDrive, YT, Telegram           | Added Terabox, improved GDrive folder handling       |
| **Progress Updates**   | Basic text                           | Real‑time speed, ETA, percentage, system stats       |
| **License**            | GPL‑3.0                              | MIT (more permissive)                                |

---

## 🙏 **Acknowledgements**

This project stands on the shoulders of giants:

- **Original Base:** [XronTrix10/Telegram‑Leecher](https://github.com/XronTrix10/Telegram-Leecher)  
- **Minor Fixes & Enhancements:** [kjeymax/Telegram‑Leecher](https://github.com/kjeymax/Telegram-Leecher)  
- **Forked Inspiration:** [ehraz786/tgdl](https://github.com/ehraz786/tgdl)  

> [!NOTE]
> Special thanks to the developers of **Pyrogram**, **aria2**, **yt‑dlp**, and **Google Colab** for making this possible.
> This project is a community‑driven enhancement of the original Telegram Leecher.

---

## 📄 **License & Disclaimer**

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

> [!IMPORTANT]  
> Using this bot for downloading copyrighted content without permission may violate laws.  
> **You should NOT use it in a way that goes against Google Colab's Terms of Service**, such as running torrents, hosting web services, or engaging in bulk compute.  
> The developer assumes no liability for misuse.

---

## 💕 Loved My Work?

🚨 [Follow me on GitHub](https://github.com/Shineii86)

⭐ [Give a star to this project](https://github.com/Shineii86/LeechBot)

<div align="center">

<a href="https://github.com/Shineii86/LeechBot">
<img src="https://github.com/Shineii86/AniPay/blob/main/Source/Banner6.png" alt="Banner">
</a>
  
  *For inquiries or collaborations*
     
[![Telegram Badge](https://img.shields.io/badge/-Telegram-2CA5E0?style=flat&logo=Telegram&logoColor=white)](https://telegram.me/Shineii86 "Contact on Telegram")
[![Instagram Badge](https://img.shields.io/badge/-Instagram-C13584?style=flat&logo=Instagram&logoColor=white)](https://instagram.com/ikx7.a "Follow on Instagram")
[![Pinterest Badge](https://img.shields.io/badge/-Pinterest-E60023?style=flat&logo=Pinterest&logoColor=white)](https://pinterest.com/ikx7a "Follow on Pinterest")
[![Gmail Badge](https://img.shields.io/badge/-Gmail-D14836?style=flat&logo=Gmail&logoColor=white)](mailto:ikx7a@hotmail.com "Send an Email")

  <sup><b>Copyright © 2026 <a href="https://telegram.me/Shineii86">Shinei Nouzen</a> All Rights Reserved</b></sup>

![Last Commit](https://img.shields.io/github/last-commit/Shineii86/LeechBot?style=for-the-badge)

<sub>Pull Requests And Contributions Are Warmly Welcomed</sub>

</div>
