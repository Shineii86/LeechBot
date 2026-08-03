# 🏗️ ARCHITECTURE.md — Technical Deep Dive

This document provides a detailed technical overview of LeechBot's internals for developers and AI agents.

---

## Table of Contents

- [System Architecture](#system-architecture)
- [Module Dependency Graph](#module-dependency-graph)
- [State Management](#state-management)
- [Request Lifecycle](#request-lifecycle)
- [Download Pipeline](#download-pipeline)
- [Upload Pipeline](#upload-pipeline)
- [Web Dashboard](#web-dashboard)
- [Error Handling Strategy](#error-handling-strategy)
- [Configuration System](#configuration-system)
- [Threading Model](#threading-model)

---

## System Architecture

LeechBot is a single-process, async Python application built on Kurigram (Pyrogram fork, Telegram MTProto client). It runs as a long-lived bot that processes download/upload tasks sequentially with a queue.

```
                    ┌──────────────────────────┐
                    │     Telegram Servers      │
                    └────────┬────────┬─────────┘
                             │        │
                    MTProto  │        │  MTProto
                    (recv)   │        │  (send)
                             │        │
┌────────────────────────────┼────────┼────────────────────────────┐
│                            ▼        ▼                            │
│  ┌──────────┐    ┌─────────────────────────┐    ┌─────────────┐ │
│  │ Handlers │───▶│    Task Manager          │───▶│  Uploaders  │ │
│  │ (input)  │    │    (orchestrator)        │    │  (output)   │ │
│  └──────────┘    └────────┬────────────────┘    └─────────────┘ │
│                           │                                     │
│                    ┌──────▼──────┐                               │
│                    │ Downloaders │                               │
│                    │ (adapters)  │                               │
│                    └─────────────┘                               │
│                                                                  │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│  │  Config   │    │   Variables  │    │   Web Server         │   │
│  │ (static)  │    │ (mutable     │    │   (aiohttp, REST+WS) │   │
│  │           │    │  state)      │    │                      │   │
│  └──────────┘    └──────────────┘    └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Dependency Graph

```
__main__.py
  ├── imports: commands, callbacks, handlers  (registers Pyrogram handlers)
  ├── imports: web.server                     (starts dashboard)
  └── runs: app.start() + idle()

commands/  ──────────────────────────────────────────────┐
  │ admin.py / downloads.py / options.py / settings.py    │
  │ start_help.py / status.py / screenshot.py             │
  ├── imports: app, OWNER                                │
  ├── imports: variables.BOT, Queue, BotStats            │
  ├── imports: task_manager.task_starter                  │
  └── imports: handler.cancelTask, helper.*               │
                                                          │
callbacks/ ──────────────────────────────────────────────┤
  │ common.py / dispatcher.py / navigation.py             │
  │ settings.py / system.py / update.py / upload.py       │
  ├── imports: app, OWNER                                │
  ├── imports: variables.BOT, MSG, BotTimes, Paths       │
  └── imports: handler.cancelTask, helper.*               │
                                                          │
handlers.py ─────────────────────────────────────────────┤
  ├── imports: app, OWNER                                │
  ├── imports: variables.BOT, Paths, MSG, BotTimes       │
  └── imports: helper.isLink, setThumbnail, etc.          │
                                                          │
task_manager.py ◄────────────────────────────────────────┘
  ├── imports: OWNER, app, DUMP_ID
  ├── imports: downloader.manager.*
  ├── imports: utility.handler.*
  └── imports: variables.* (heavy usage)

utility/handler.py
  ├── imports: OWNER, app
  ├── imports: uploader.telegram.{upload_file, upload_photos_batch}
  ├── imports: utility.converters.*
  └── imports: variables.*, helper.*

utility/helper.py
  ├── imports: app (Pyrogram client)
  ├── imports: variables.BOT, MSG, BotTimes, Messages, Paths
  └── pyrogram.types: InlineKeyboardButton, InputMediaPhoto

downloader/manager.py
  ├── imports: variables.BOT, Transfer, MSG, Messages, BotTimes, BotStats
  ├── imports: helper.* (link detection)
  └── dispatches to: aria2, ytdl, gallery, gdrive, mega, etc.

uploader/telegram.py
  ├── imports: variables.BOT, Transfer, BotTimes, Messages, MSG, Paths
  └── imports: helper.{sizeUnit, fileType, getTime, status_bar, ...}
```

---

## State Management

**All mutable global state lives in `leechbot/utility/variables.py`.**

There is no database. State is held in Python class attributes and persists for the lifetime of the process.

### State Classes

| Class | Scope | Reset |
|-------|-------|-------|
| `BOT.Setting` | Persistent preferences | Survives across tasks |
| `BOT.Options` | Per-task options | Reset each task |
| `BOT.Mode` | Current task mode | Reset each task |
| `BOT.State` | Control flags | Manual reset |
| `Queue` | Download queue | Manual clear |
| `Transfer` | Current transfer stats | Reset each task |
| `BotTimes` | Timing | Reset each task |
| `BotStats` | Cumulative stats | Never reset |
| `Messages` | Dynamic text | Reset each task |
| `MSG` | Message references | Updated each task |
| `Paths` | File paths | Static |

### Import Pattern

```python
# Direct import — these are class-level attributes, not instances
from leechbot.utility.variables import BOT, Transfer, MSG

# Mutate directly
BOT.Setting.prefix = "🎬"
Transfer.up_bytes.append(file_size)
MSG.sent_msg = new_message
```

---

## Request Lifecycle

### 1. User sends a command

```
Telegram → Pyrogram event loop → @app.on_message handler
```

### 2. Command handlers (`leechbot/commands/` package)

```python
@app.on_message(filters.command("tupload"))
async def tupload_cmd(client, message):
    # Validate user access
    # Set BOT.Mode
    # Call task_starter() → sends instruction text
    # User sends link(s) in next message
```

### 3. Link handler (`handlers.py`)

```python
@app.on_message(filters.text & filters.private & ~filters.command([...]))
async def handle_text(client, message):
    # Detect links in message text
    # Add to Queue
    # If no active task → trigger task_manager
```

### 4. Task orchestration (`task_manager.py`)

```python
async def task_starter(message, text):
    # Initialize BOT state
    # Call downloadManager() → download files
    # Call Leech() → process and upload
    # Call SendLogs() → completion summary
```

### 5. Download (`downloader/manager.py`)

```python
async def downloadManager(links):
    # For each link:
    #   Detect type (YouTube, GDrive, Mega, etc.)
    #   Dispatch to appropriate downloader
    #   Track progress
```

### 6. Upload (`utility/handler.py` → `uploader/telegram.py`)

```python
async def Leech(folder_path, remove):
    # Separate photos from other files
    # Photos → upload_photos_batch() or upload_file()
    # Others → upload_file() with progress
    # Auto-screenshot: if enabled, extract from local file before cleanup
    #   → send as media group to dump channel
```

---

## Download Pipeline

```
Link URL
  │
  ▼
downloader/manager.py::downloadManager()
  │
  ├─ is_ytdl_link()     → ytdl.py         (yt-dlp, 2000+ sites)
  ├─ is_google_drive()   → gdrive.py       (Google Drive API)
  ├─ is_mega()           → mega.py         (megatools CLI)
  ├─ is_telegram()       → telegram.py     (Kurigram media download)
  ├─ is_terabox()        → terabox.py      (direct link extraction)
  ├─ is_pixeldrain()     → pixeldrain.py   (API)
  ├─ is_mediafire()      → mediafire.py    (scraping)
  ├─ is_gallery()        → gallery.py      (gallery-dl, 100+ sites)
  ├─ is_torrent()        → torrent.py      (magnet/libtorrent)
  └─ default             → aria2.py        (HTTP/FTP direct)

```

Each downloader:
1. Downloads files to `Paths.down_path` (`/tmp/leechbot/work/downloads/`)
2. Returns downloaded file paths
3. Reports progress via `Messages.status_head` + `status_bar()`

---

## Upload Pipeline

### Single File Upload

```
upload_file(file_path, real_name)
  │
  ├─ Determine type: video / audio / photo / document
  ├─ Apply caption with prefix/suffix
  ├─ Call reply_video / reply_audio / reply_photo / reply_document
  │   with progress=progress_bar callback
  └─ Track in Transfer.sent_file
```

### Batch Photo Upload (v3.1.1+)

```
upload_photos_batch(photo_paths)
  │
  ├─ For each photo (up to 10 per batch):
  │   ├─ _upload_photo_with_progress()
  │   │   ├─ reply_photo(progress=progress_bar)  ← shows progress
  │   │   ├─ Capture file_id from response
  │   │   └─ Delete temporary message
  │   └─ Collect file_ids
  │
  ├─ reply_media_group(media=[InputMediaPhoto(file_id)...])
  │   └─ Instant — files already on Telegram servers
  │
  └─ Track in Transfer.sent_file
```

**Why this approach?** `reply_media_group()` does NOT support `progress` callback (Telegram Bot API limitation). Uploading individually first gives full progress tracking, and grouping via `file_id` avoids re-uploading.

---

## Web Dashboard

### Backend (`web/server.py`)

- **Framework:** aiohttp
- **Auth:** Bearer token in `Authorization` header
- **Endpoints:** 7 REST + 1 WebSocket
- **Broadcast:** Auto-pushes state to all WS clients every 3 seconds
- **CORS:** Enabled (`*`) for cross-origin access

### Frontend (`public/index.html`)

- **Framework:** Vanilla JS + Tailwind CSS (CDN)
- **No build step** — single HTML file
- **Real-time:** WebSocket with REST fallback (5s polling)
- **Tabs:** Queue, Files, Settings, System, Commands
- **Auth:** Token saved in `localStorage`

### Data Flow

```
Browser ←→ WebSocket ←→ server.py ←→ variables.py (BOT, Transfer, etc.)
                ↕
         REST API (fallback)
```

---

## Error Handling Strategy

### Layer 1: Try/Except in Handlers

```python
try:
    await some_operation()
except FloodWait as e:
    await sleep(e.value + 1)  # +1s safety margin
    # retry (max 10 times to prevent stack overflow)
except Exception as e:
    logger.error(f"Operation failed: {e}")
```

### Layer 2: Retry Wrapper (`downloader/manager.py`)

```python
async def _with_retry(coro_factory, link, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await coro_factory()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await sleep(3)
```

### Layer 2b: FloodWait Retry (uploader)

```python
# upload_file() handles Telegram FloodWait with bounded retry depth
# Max 10 retries — prevents stack overflow from recursive calls
await upload_file(file_path, real_name, _retry_depth=retry + 1)
```

### Layer 3: Debug Reporting (`debug.py`)

- `TelegramLogHandler` — sends ERROR/CRITICAL logs to DUMP channel
- `setup_error_reporting()` — installs asyncio + Pyrogram exception hooks
- All unhandled exceptions get reported to Telegram

### Layer 4: Task Cancellation

```python
async def cancelTask(reason):
    # Cancel asyncio task
    # Clean up temp files
    # Reset BOT.State
    # Notify user
```

---

## Configuration System

### Priority Order (highest → lowest)

1. **Environment variables** (`os.getenv()`)
2. **`.env` file** (loaded by `python-dotenv`)
3. **`credentials.json`** (Colab notebook fallback)
4. **Defaults in `config.py`**

### Key Config Values

| Variable | Default | Purpose |
|----------|---------|---------|
| `API_ID` | (required) | Telegram API ID |
| `API_HASH` | (required) | Telegram API hash |
| `BOT_TOKEN` | (required) | Bot token from BotFather |
| `OWNER_ID` | (required) | Admin user ID |
| `DUMP_ID` | (required) | Log channel ID |
| `DEFAULT_UPLOAD_MODE` | media | media or document |
| `BANDWIDTH_LIMIT` | (empty) | Download speed limit |
| `WEB_PORT` | 8080 | Dashboard port |
| `WEB_TOKEN` | auto | Dashboard auth token |

---

## Threading Model

```
Main Thread (asyncio event loop)
  │
  ├─ Pyrogram handlers (async) ← all bot logic
  ├─ aiohttp web server (async) ← dashboard API
  ├─ Background broadcast task (async) ← WS push every 3s
  └─ Subprocess calls (async, via asyncio.create_subprocess_exec)
      ├─ aria2c (HTTP/FTP/torrent)
      ├─ yt-dlp (YouTube, 2000+ sites)
      ├─ gallery-dl (photo galleries)
      ├─ megatools (Mega.nz)
      └─ ffmpeg (video conversion)
```

Everything runs in a single asyncio event loop. External tools (aria2c, yt-dlp, megatools, ffmpeg) are invoked via `asyncio.create_subprocess_exec()` which does NOT block the event loop — stdout/stderr are read line-by-line with `await` so progress updates flow in real-time.

---

## File Size Limits

| Limit | Value | Source |
|-------|-------|--------|
| Telegram upload | 2 GB | `config.MAX_FILE_SIZE` |
| Safe split target | 1.9 GB | `config.MAX_VIDEO_SPLIT_SIZE` |
| Media group | 10 photos | Telegram API limit |

---

## Session Management

- Pyrogram session stored in `sessions/leechbot_session.session`
- SQLite-backed (Pyrogram default)
- First run requires interactive phone verification
- Colab notebook cleans session on each deploy
- Session persists across bot restarts
