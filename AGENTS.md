# AGENTS.md — AI Agent Instructions for LeechBot

> **Read this file before making any changes to the codebase.**

---

## Project Overview

LeechBot is a **Kurigram-based (Pyrogram fork) Telegram bot** for downloading files from various sources (direct links, YouTube, Google Drive, Mega, galleries, etc.) and uploading them to Telegram or Google Drive. ~8000 lines of Python.

**Language:** Python 3.10+  
**Framework:** Kurigram (actively maintained Pyrogram fork)  
**License:** MIT

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    __main__.py                       │
│              (entry point, startup)                  │
├───────────┬───────────┬─────────────┬───────────────┤
│ commands/ │ callbacks/│  handlers.py│  (Kurigram    │
│  /cmd     │  buttons  │  messages   │   handlers)   │
├───────────┴───────────┴─────────────┴───────────────┤
│              utility/task_manager.py                 │
│           (orchestrates download → upload)           │
├─────────────────────┬───────────────────────────────┤
│  downloader/        │  uploader/                     │
│  ├ manager.py       │  └ telegram.py                 │
│  ├ aria2.py         │    (single + batch upload)     │
│  ├ ytdl.py          ├───────────────────────────────┤
│  ├ gallery.py       │  utility/                      │
│  ├ gdrive.py        │  ├ handler.py (Leech, Zip...)  │
│  ├ mega.py          │  ├ helper.py (UI, links)       │
│  ├ terabox.py       │  ├ converters.py               │
│  ├ pixeldrain.py    │  ├ variables.py (global state) │
│  ├ mediafire.py     │  ├ rss_manager.py              │
│  └ __init__.py      │  └ task_manager.py             │
├─────────────────────┴───────────────────────────────┤
│  web/server.py  ←→  public/index.html               │
│  (aiohttp REST + WebSocket dashboard)               │
├─────────────────────────────────────────────────────┤
│  config.py          │  debug.py  │  updater.py       │
│  (env vars, paths)  │  (logging) │  (git auto-update)│
└─────────────────────────────────────────────────────┘
```

---

## Key Files & Responsibilities

| File | Purpose |
|------|---------|
| `config.py` | All env vars, paths, feature flags, credentials loading |
| `leechbot/__init__.py` | Pyrogram `app` client creation, exports |
| `leechbot/__main__.py` | Entry point, handler imports, web server startup |
| `leechbot/aliases.py` | Command alias pre-processor (built-in shortcuts + custom aliases) |
| `leechbot/commands/` | `/command` handler package (admin, downloads, options, settings, start_help, status) |
| `leechbot/callbacks/` | Inline keyboard callback package (dispatcher, navigation, settings, system, update, upload) |
| `leechbot/handlers.py` | Message handlers (URL, photo, text, reply) |
| `leechbot/utility/variables.py` | **ALL global mutable state** — single source of truth |
| `leechbot/utility/helper.py` | Link detection, UI builders, file utils, status bar |
| `leechbot/utility/handler.py` | `Leech()`, `Zip_Handler()`, `Unzip_Handler()`, `SendLogs()`, `send_auto_screenshots()` |
| `leechbot/utility/task_manager.py` | `task_starter()` — orchestrates download→upload pipeline |
| `leechbot/utility/converters.py` | Video conversion, archive/extract, size checking |
| `leechbot/downloader/manager.py` | Download router — dispatches to correct downloader |
| `leechbot/uploader/telegram.py` | File upload with progress, batch photo upload |
| `leechbot/web/server.py` | aiohttp REST API + WebSocket for dashboard |
| `public/index.html` | Dashboard frontend (vanilla JS + Tailwind CSS) |
| `leechbot/debug.py` | Error reporting to Telegram DUMP channel |
| `leechbot/updater.py` | GitHub-based auto-update mechanism |

---

## Global State Model

**All mutable state lives in `leechbot/utility/variables.py`.** Import the class you need and mutate attributes directly.

Key state classes:
- **`BOT`** — Settings, Options, Mode, State (nested classes)
- **`Queue`** — Download queue (deque-based)
- **`Transfer`** — File transfer stats (bytes, sent files)
- **`BotTimes`** — Timing for progress calculations
- **`BotStats`** — Cumulative stats (total tasks, downloaded, uploaded)
- **`Messages`** — Dynamic message content
- **`MSG`** — Pyrogram Message object references
- **`Paths`** — All file system paths

---

## Data Flow

```
User sends /tupload + link
  → leechbot/commands/downloads.py: task_starter()
  → task_manager.py: orchestrates pipeline
    → downloader/manager.py: routes to correct downloader
      → aria2.py / ytdl.py / gallery.py / etc.
    → utility/handler.py: Leech() processes files
      → converters.py: video conversion, zip/extract
      → uploader/telegram.py: upload with progress
      → send_auto_screenshots() if enabled (extract from local file, send as batch)
    → handler.py: SendLogs() completion summary
```

---

## Conventions

### Code Style
- **Linter: ruff** (configured in `pyproject.toml`) — follow existing patterns
- Module-level docstrings with project header (see any file)
- `logger = logging.getLogger(__name__)` at module top
- Async everywhere — this is an asyncio application
- Type hints on function signatures (not always present, but preferred)

### File Headers
Every `.py` file starts with:
```python
# =============================================================================
# Telegram Leech Bot - [Module Name]
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================
# License   : MIT License
# =============================================================================
```

### Imports
- Standard lib → third-party → local
- `from leechbot import app, OWNER` for Pyrogram client access
- `from leechbot.utility.variables import BOT, MSG, ...` for state
- Circular imports avoided by using local imports inside functions

### Error Handling
- `try/except Exception as e: logger.error(...)` pattern
- FloodWait handled with `await sleep(e.value + 1)` + retry (max 10 times to prevent stack overflow)
- Errors reported to DUMP channel via `debug.py`

---

## Common Tasks

### Adding a New Command
1. Add handler in the appropriate `leechbot/commands/<module>.py` (e.g., `downloads.py`, `admin.py`) with `@app.on_message(filters.command("cmd"))`. If a new category is needed, create a module and import it in `leechbot/commands/__init__.py`.
2. Register command description in `__main__.py` `_register_commands()`
3. Add any new state to `leechbot/utility/variables.py`
4. Update `GUIDE.md` commands table

### Adding a New Downloader
1. Create `leechbot/downloader/newsite.py`
2. Add link detection pattern in `leechbot/utility/helper.py`
3. Add routing in `leechbot/downloader/manager.py`
4. Export in `leechbot/downloader/__init__.py`

### Modifying Upload Behavior
- Single file upload: `leechbot/uploader/telegram.py` → `upload_file()`
- Batch photo upload: same file → `upload_photos_batch()`
- Progress tracking: `progress_bar()` callback

### Changing Settings/Config
- Env vars: `config.py`
- Runtime state: `leechbot/utility/variables.py` → `BOT.Setting`
- Per-task options: `BOT.Options`

---

## Known Constraints

| Constraint | Reason |
|-----------|--------|
| Pyrogram 2.0.106 | No `style` on buttons, no `progress` on `reply_media_group()` |
| Telegram 2GB file limit | Handled by `sizeChecker()` splitting |
| Media group: max 10 photos | Batch upload splits into groups of 10 |
| `reply_media_group()` no progress | Workaround: upload individually with progress, group via `file_id` |
| YT-DLP may need cookies | PO token plugin (auto) or cookies.txt (manual) |

---

## Dependencies

```
pyrogram>=2.0.106    # Telegram client
tgcrypto>=1.2.5      # Encryption acceleration
yt-dlp               # Video platform downloads
gallery-dl            # Photo gallery downloads
aiohttp               # Web server
moviepy               # Video conversion
Pillow                # Image processing
psutil                # System monitoring
natsort               # Natural sorting
```

---

## Testing

Test suite in `tests/` (pytest + pytest-asyncio). Expand coverage. Manual testing:
1. Start bot: `python3 -m leechbot`
2. Send `/start` on Telegram
3. Test each command type with real links
4. Check DUMP channel for error logs
5. Verify dashboard at `http://localhost:8080`

---

## Changelog

Every change must be recorded in `CHANGELOG.md` with:
- Version number
- Date
- Description under Added/Changed/Fixed/Removed sections
- **New entries at the top** — never edit or delete existing entries

---

## Security Notes

- Never commit `.env`, `credentials.json`, `token.pickle`, or session files
- `API_ID`, `API_HASH`, `BOT_TOKEN` are secrets — load from env/Colab Secrets
- Dashboard auth token is auto-generated or set via `WEB_TOKEN` env var
- WebSocket auth is not enforced (REST is secured with Bearer token)
