<div align="center">

<img src="https://img.shields.io/badge/LeechBot-v3.0-9cf?style=for-the-badge&logo=telegram&logoColor=white" alt="LeechBot">

# 🚀 LeechBot Pro

**Advanced Telegram Leeching Bot with Multi-Source Download Support**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square)](https://www.python.org/)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.x-orange.svg?style=flat-square)](https://docs.pyrogram.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

</div>

---

## ✨ Features

### 🔥 Core Capabilities
- **Multi-Source Downloads**: Google Drive, YouTube, Mega.nz, Terabox, Direct Links, Telegram
- **Dual Upload Modes**: Upload to Telegram or Mirror to Google Drive
- **Smart Processing**: Auto-extract, Compress, Convert Videos
- **Batch Operations**: Process multiple links simultaneously
- **Progress Tracking**: Real-time download/upload progress with beautiful UI

### 🎛️ Advanced Settings
- **Video Conversion**: GPU/CPU accelerated with quality options
- **File Splitting**: Automatic splitting for large files (>2GB)
- **Custom Naming**: Prefix, Suffix, and Custom Filename support
- **Thumbnail Support**: Custom thumbnails for videos
- **Caption Styling**: Bold, Italic, Monospace, Underlined options
- **Password Protection**: Zip encryption and archive extraction passwords

### 🆕 New in v3.0
- **Enhanced UI/UX**: Modern message templates with animations
- **Speed Limiting**: Control download speeds
- **Queue System**: Smart task scheduling
- **Error Recovery**: Auto-retry failed downloads
- **Statistics Dashboard**: Track your usage
- **Multi-Language Support**: Coming soon

---

## 📋 Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize the bot and view welcome message |
| `/tupload` | Leech to Telegram |
| `/gdupload` | Mirror to Google Drive |
| `/drupload` | Upload local directory |
| `/ytupload` | YouTube/DL supported sites upload |
| `/settings` | Configure bot preferences |
| `/setname` | Set custom filename |
| `/zipaswd` | Set zip password |
| `/unzipaswd` | Set unzip password |
| `/help` | Display help information |
| `/stats` | View download statistics |
| `/cancel` | Cancel ongoing task |

---

## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- Telegram API credentials ([my.telegram.org](https://my.telegram.org))
- Bot Token from [@BotFather](https://t.me/BotFather)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/Shineii86/LeechBot.git
cd LeechBot

# Install dependencies
pip install -r requirements.txt

# Configure credentials
cp config/config.sample.py config/config.py
# Edit config.py with your credentials

# Run the bot
python -m bot
```

### Google Drive Setup (Optional)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable Google Drive API
3. Download `credentials.json` and place in config folder
4. Run auth script to generate `token.pickle`

---

## 📁 Project Structure

```
LeechBot/
├── bot/
│   ├── __init__.py          # Bot initialization
│   ├── __main__.py          # Entry point
│   ├── handlers.py          # Command handlers
│   └── callbacks.py         # Callback query handlers
├── downloader/
│   ├── aria2.py             # Aria2c downloader
│   ├── ytdl.py              # yt-dlp integration
│   ├── gdrive.py            # Google Drive downloader
│   ├── mega.py              # Mega.nz downloader
│   ├── telegram.py          # Telegram downloader
│   └── terabox.py           # Terabox downloader
├── utility/
│   ├── variables.py         # Global variables & classes
│   ├── helper.py            # Utility functions
│   ├── handler.py           # Leech/Mirror handlers
│   ├── converters.py        # File conversion & archiving
│   └── task_manager.py      # Task scheduling
├── uploader/
│   └── telegram.py          # Telegram uploader
├── config/
│   └── config.py            # Configuration file
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🎯 Usage Examples

### Basic Leech
```
/tupload
https://example.com/file.zip
```

### With Custom Name
```
/tupload
https://example.com/file.zip
[MyCustomFile.zip]
```

### With Password
```
/tupload
https://example.com/protected.zip
{zip_password}
(unzip_password)
```

### YouTube Download
```
/ytupload
https://youtube.com/watch?v=xxxxx
```

### Multiple Links
```
/tupload
https://link1.com/file1.zip
https://link2.com/file2.mp4
https://link3.com/file3.mkv
```

---

## ⚙️ Configuration Options

| Setting | Options | Description |
|---------|---------|-------------|
| Upload Mode | Media / Document | How files are sent |
| Video Convert | Yes / No | Auto-convert videos |
| Split Videos | Split / Zip | Handle large videos |
| Output Format | MP4 / MKV | Video output format |
| Quality | High / Low | Conversion quality |
| Caption Style | Bold / Italic / Mono / Underline / Regular | Text formatting |

---

## 🛡️ Safety & Limits

- Maximum file size: 2GB per file (Telegram limit)
- Auto-splitting for larger files
- Torrent/Magnet support with tracker auto-update
- Rate limiting to prevent bans
- Secure credential storage

---

## 🐛 Troubleshooting

### Common Issues

**Bot not responding?**
- Check API_ID, API_HASH, and BOT_TOKEN
- Ensure bot is started with correct credentials

**Download failures?**
- Verify link accessibility
- Check disk space
- Review logs for specific errors

**Google Drive errors?**
- Ensure token.pickle exists
- Check API quota limits
- Verify file sharing permissions

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

**Developer**: [Shinei Nouzen](https://github.com/Shineii86)  
**Telegram**: [@Shineii86](https://t.me/Shineii86)  
**Twitter/X**: [@Shineii86](https://x.com/Shineii86)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by Shinei Nouzen

</div>
