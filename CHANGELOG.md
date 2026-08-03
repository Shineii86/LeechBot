# Changelog

All notable changes to this project will be documented in this file.

---

## [3.4.0] - 2026-08-03

### Removed
- **🎬 Anime Downloader Feature** — complete removal of anime downloading subsystem
  - Removed `leechbot/downloader/anime.py` (MiruroAPI client, search, episodes, streaming)
  - Removed `leechbot/commands/anime.py` (/anime command handler, quick download, interactive search)
  - Removed `leechbot/callbacks/anime.py` (inline keyboard callbacks for anime UI)
  - Removed `ANIME_API_URL` from config.py and .env.example
  - Removed /anime BotCommand registration from __main__.py
  - Removed anime category and help entries from start_help.py
  - Removed anime callback routing from dispatcher.py
  - Removed anime imports from commands/__init__.py
  - Cleaned anime references from autorename.py, handler.py
  - Updated all documentation (AGENTS.md, ARCHITECTURE.md, README.md, GUIDE.md)
  - Updated Colab notebook (notebooks/LeechBot.ipynb)

---

## [3.3.1] - 2026-08-03

### Fixed
- **🔧 Pillow Dependency Conflict** — resolved `moviepy>=2.2.1` and `Pillow>=12.3.0` version incompatibility in `requirements.txt`
  - `moviepy>=2.2.1` requires `Pillow>=9.2.0,<12.0`, while the previous requirement specified `Pillow>=12.3.0`
  - Changed `Pillow>=12.3.0` to `Pillow>=9.2.0,<12.0` to align with `moviepy`'s constraints
  - Fixes Google Colab installation error: `ResolutionImpossible` for conflicting Pillow versions

### Changed
- **📦 Upgraded all dependencies to latest versions** in `requirements.txt`
  - `kurigram` >=2.2.23 → >=2.2.24
  - `yt-dlp` >=2026.6.9 → >=2026.7.4
  - `curl_cffi` >=0.15.0 → >=0.16.0
  - `gallery-dl` >=1.32.6.dev0 → >=1.32.8 (moved to Codeberg: https://codeberg.org/mikf/gallery-dl)
  - `aiohttp` >=3.14.1 → >=3.14.3

---

## [3.3.0] - 2026-06-30

### Added
- **📸 Auto-Screenshot After Upload** — screenshots extracted from local file after video upload
  - Enabled via Settings → 📸 Auto-SS: ON/OFF
  - Configurable count (1-20) and watermark text
  - Screenshots sent as media group (batch) to dump channel
  - No re-download — extracts directly from file on disk before cleanup
  - Works for all upload sources (aria2, ytdl, gallery-dl, anime, etc.)

### Changed
- `/start` keyboard: removed "Help" button, added "All" category grid directly
- Help navigation uses `edit_media(InputMediaPhoto)` for smooth photo+text transitions
- Status bar now includes `sysINFO_full()` by default (was on-demand only)

---

## [3.2.9] - 2026-06-30

### Added
- **📖 Shinobu-style Help Menu** — complete rewrite of /start and /help with photo support
  - `/start` → random photo from assets + welcome text + category grid buttons
  - `/help` → random photo + category grid navigation
  - "All" → paginated 3-column module grid (← 1/2 →) with random photo on each page
  - Category view → filtered module grid with random photo
  - Module detail → command list with `❖` formatting and random photo
  - About page → random photo + version info
  - Smooth transitions via `edit_media()` — no delete+resend needed
- **📊 Permanent System Info** — CPU, RAM, Disk, Network, Uptime now always visible in progress bar
  - No need to click "📊 Stats" button anymore
  - Compact `sysINFO()` at initial status, detailed `sysINFO_full()` on every progress update

### Changed
- `/start` keyboard: removed "Help" button, added "All" category grid directly
- Help navigation uses `edit_media(InputMediaPhoto)` for smooth photo+text transitions
- Status bar now includes `sysINFO_full()` by default (was on-demand only)

---

## [3.2.8] - 2026-06-30

### Added
- **🎬 Anime Episode Downloader** — full-featured anime downloading with 9 advanced features
  - `/anime <name>` — interactive search with inline buttons, episode titles, and info cards
  - `/anime <name> ep 1-5 sub` — quick batch download mode
  - Multi-provider fallback (kiwi → ally → miruro → animex)
  - Dub→sub fallback when dub unavailable
  - Quality selector (480p/720p/1080p/Auto) in interactive mode
  - Batch progress counter (Ep 3/10)
  - Resume interrupted downloads (`/anime resume`)
  - Subtitle embedding in MKV via mkvmerge/ffmpeg
  - Multi-episode zip before upload (`/anime ... zip`)
  - Sub/Dub audio category toggle
- **🏷️ Auto-Rename Template** — new `/autorename` command
  - `/autorename <template>` — set rename pattern with placeholders
  - Supports: `{season}`, `{episode}`, `{quality}`, `{audio}`, `{title}`, `{chapter}`
  - `/autorename clear` — remove template
- **ANIME_API_URL config** — required env var for anime feature
  - Set in `.env`: `ANIME_API_URL=<your-api-url>`
  - Error message with buy link (`t.me/Shineii86`) if not configured

### Changed
- **Migrated from Pyrogram to Kurigram** — actively maintained Pyrogram fork
  - `disable_web_page_preview=True` → `link_preview_options=types.LinkPreviewOptions(is_disabled=True)` (30 occurrences, 14 files)
  - `reply_to_message_id=` → `reply_parameters=types.ReplyParameters(...)` (7 occurrences in uploader/telegram.py)
  - Removed deprecated `warnings.filterwarnings` deprecation suppress
  - Added `from pyrogram import types` to all modified files
- Registered `/anime` and `/autorename` BotCommands with Telegram
- Updated command count from 34 to 38

### Fixed
- `reply_to_message_id` deprecation warnings from Pyrogram (now using kurigram API)
- Status_head ownership issue (YTDL_Status was overwriting Messages.status_head)

### Improved
- yt-dlp concurrent fragment downloads: 4 → 8 for faster HLS/DASH

---

## [3.2.7] - 2026-06-29

### Added
- **📸 Screenshot Generator** — new `/screenshot` command for generating thumbnails from videos and PDFs
  - `/screenshot [count]` — extract 1-20 frames (default 5) from video or PDF
  - `/setwm <text>` — set watermark text on screenshots (owner only)
  - Supports MP4, MKV, AVI, MOV, WebM, PDF
  - Uses ffmpeg (video) and Pillow (watermark) from existing stack
  - Per-user lock prevents concurrent processing

---

## [3.2.6] - 2026-06-22

### Changed
- **⚡ Speed optimizations** — faster downloads and uploads:
  - `aria2c`: enabled `-k 1M` min-split-size and `--max-concurrent-downloads=5` for non-torrent HTTP/FTP downloads (already using `-x 16 -s 16`).
  - `StreamTape` downloader: added `--min-split-size=1M` to match main aria2c settings.
  - `yt-dlp`: reduced `concurrent_fragment_downloads` from 5 to 4 for stable HLS/DASH parallel downloads.
  - Pyrogram client: raised `max_concurrent_transmissions` from 5 to 10 to improve parallel upload throughput.

---

## [3.2.5] - 2026-06-22

### Added
- **📰 RSS Auto-Download** — background RSS feed monitor for automatic downloads:
  - `/rss_add <url> <command> [interval]` — subscribe to an RSS/Atom feed
  - `/rss_list` — list configured feeds
  - `/rss_remove <id>` — remove a feed
  - `/rss_check` — manually trigger a feed check
  - New feeds are saved to `rss_feeds.json` in `BASE_DIR`
  - New entries are dispatched to the chosen command (`tupload`, `ytupload`, `gdupload`, etc.)
  - Added `feedparser` dependency and started the poller from `leechbot/__main__.py`

---

## [3.2.4] - 2026-06-22

### Added
- **🚀 Simple entry point `leechbot.py`** — added a root-level wrapper so the bot can be started with either:
  - `python3 leechbot.py`
  - `python3 -m leechbot`
  - Updated `README.md` and `GUIDE.md` to show both options.

---

## [3.2.3] - 2026-06-22

### Fixed
- **🐛 Callback answer recursion** — fixed `safe_answer()` in `leechbot/callbacks/common.py` which was calling itself instead of `callback_query.answer()`. This caused `RecursionError` on every inline button press.

---

## [3.2.2] - 2026-06-22

### Added
- **🔀 Custom command aliases** — owner can now create short aliases for any command:
  - `/alias <name> <target>` — create alias (e.g., `/alias dl tupload` makes `/dl` behave like `/tupload`)
  - `/aliases` — list all aliases
  - `/unalias <name>` — remove an alias
  - Aliases are persisted to `aliases.json` in `BASE_DIR` so they survive restarts.
  - New `leechbot/aliases.py` pre-processor rewrites aliased messages before the real command handlers run.

---

## [3.2.1] - 2026-06-22

### Changed
- **📚 Updated documentation for v3.2.0 modular structure** — refreshed project structure diagrams and file references in `README.md`, `GUIDE.md`, `ARCHITECTURE.md`, and `AGENTS.md` to use `leechbot/commands/` and `leechbot/callbacks/` packages instead of the old monolithic `commands.py`/`callbacks.py` files. Also updated the "Adding a New Command" agent instructions to point to the correct submodules.

---

## [3.2.0] - 2026-06-22

### Changed
- **🗂️ Modularized command and callback handlers** — split monolithic `leechbot/commands.py` (1021 lines) and `leechbot/callbacks.py` (724 lines) into focused packages:
  - `leechbot/commands/` — `admin.py`, `downloads.py`, `options.py`, `settings.py`, `start_help.py`, `status.py` + `__init__.py`
  - `leechbot/callbacks/` — `common.py`, `dispatcher.py`, `navigation.py`, `settings.py`, `system.py`, `update.py`, `upload.py` + `__init__.py`
  - Central callback dispatcher in `callbacks/dispatcher.py` routes queries to the new submodules; Pyrogram handlers still auto-register via package imports in `leechbot/__main__.py`.

---

## [3.1.48] - 2026-06-22

### Reverted
- **⏪ Reverted all 21–22 Jun 2026 changes** — rolled back 79 commits (v3.1.49 through v3.3.5) to restore the codebase to the stable v3.1.47 baseline. This removes anime/autorename features, multi-user state, moderation system, CF bypass proxy, hosting files, and the accidentally committed `.env` file from the working tree.

---

## [3.1.47] - 2026-06-08

### Changed
- **🎨 Full UI redesign — HTML formatting** — migrated ALL bot messages from Markdown (`**bold**`, `` `code` ``) to HTML (`<b>bold</b>`, `<code>code</code>`) across 20+ files:
  - `callbacks.py`: HELP_TEXT, ABOUT_TEXT, all callback messages (prefix, suffix, autodelete, format, bandwidth, video, caption, thumb, photo mode, upload, update, system info)
  - `commands.py`: WELCOME_TEXT, help_text, /format, /speed, /tupload, /gdupload, /drupload, /ytupload, /glupload, /setname, /formats, /preview, /zipaswd, /unzipaswd, /ping, /status, /cancel, /cancel_all, /admin, /broadcast, /cookies, /setcookies, /clearcookies, /restart, /logs, /update
  - `handlers.py`: gallery init, upload type selector, thumbnail, cookies, auto-delete delay
  - `utility/helper.py`: sysINFO, sysINFO_full, format_stats, settings menu, status bar
  - `utility/handler.py`: all upload status messages, cancel notification, task complete summary, file list
  - `utility/task_manager.py`: task init messages
  - `utility/converters.py`: video conversion, zipping, extracting, splitting
  - `downloader/*.py`: all status_head messages (aria2, ytdl, gallery, gdrive, mega, catbox, gofile, mediafire, pixeldrain, streamtape, torrent)
  - `uploader/telegram.py`: photo upload status
  - `debug.py`: error reporting messages
- **🔄 Arrow replacement** — changed `→` to `»` in all user-facing messages for better readability
- **🧭 Consistent navigation buttons** — all keyboards now use `⌂ Home` + `🔒 Close` pattern (Help, About, Settings menus)
- **💡 Tips added** — helpful tips in prefix, suffix, autodelete, format, caption messages

---

## [3.1.46] - 2026-06-08

### Removed
- **👤 UserBot feature removed** — deleted `userbot.py` and all related commands (`/userbot`, `/userbot_logout`, `/userbot_status`), auth flow, and state tracking

### Changed
- **📚 Full documentation sweep** — updated all 8 doc files to match v3.1.45 codebase:
  - README.md: fixed false modularization claims, corrected project structure, updated command count (32)
  - ARCHITECTURE.md: removed deleted config vars (`MAX_CONCURRENT_DOWNLOADS`, `GDRIVE_ENABLED`), removed `telegram.py` from download pipeline
  - AGENTS.md: removed deleted files from diagram, updated line counts, fixed command count
  - GUIDE.md: replaced Docker "Coming Soon" with actual instructions, removed deleted config vars, removed `YTDL_BROWSER_COOKIES` section, updated project structure
  - TERMUX.md: fixed version references, typo (`ENABLE_TRENTS`), command count, removed deleted config vars
  - AUDIT_REPORT.md: marked as historical document
  - pyproject.toml, Dockerfile: version sync

---

## [3.1.45] - 2026-06-08

### Fixed
- **🐛 NameError `HELP_KEYBOARD`** — added missing `InlineKeyboardMarkup`/`InlineKeyboardButton` imports at module level in `callbacks.py`
- **🐛 Dead button `"danger"`** — changed `callback_data` from `"danger"` to `"autodelete"` in `helper.py` so auto-delete settings are accessible when OFF
- **🐛 AttributeError `BOT.Options.file_name`** — added missing `file_name` attribute to `BOT.Options` in `variables.py`
- **🐛 AttributeError `Transfer.download_path`** — added missing `download_path` attribute to `Transfer` in `variables.py`
- **🔒 WebSocket auth bypass** — added auth token validation on WebSocket connect in `server.py`
- **🔒 CORS wildcard** — replaced `*` with configurable `WEB_CORS_ORIGIN` env var in `server.py`
- **🔒 Token exposure** — reduced auth token logged from 8 to 4 chars in `server.py`
- **🔒 Shell injection** — replaced `shell=True` with list args in `aria2.py:get_Aria2c_Name()`

### Changed
- **🧹 Dead code cleanup** — removed `commands_old.py`, `utility/style.py` (1529+ lines of unused code)
- **🧹 Dead config removed** — `MAX_CONCURRENT_DOWNLOADS`, `ENABLE_TORRENTS`, `GDRIVE_ENABLED`, `YTDL_BROWSER_COOKIES`
- **🧹 Dead state removed** — `Aria2c.pic_dwn_url`
- **🧹 Unused imports removed** — 14 stale imports across 8 files
- **🧹 Unused deps removed** — `requests`, `ffmpeg-python` from `requirements.txt`
- **🧹 Dead handlers removed** — `help_cat_`/`help_cmd_` callback handlers
- **🧹 Dead exports removed** — `is_gofile_link`, `is_catbox_link`, `is_streamtape_link`
- **📦 Config centralized** — `WEB_PORT` and `WEB_TOKEN` moved to `config.py` + `.env.example`

---

## [3.1.44] - 2026-06-08

### Fixed
- **🐛 ImportError `_help_render_main`** — removed stale `_help_render_*` imports from `callbacks.py`; help menu now uses inline `HELP_TEXT` and `HELP_KEYBOARD` constants
- **🐛 Progress bar overflow (101.97%)** — capped upload progress at 100% in `uploader/telegram.py`

### Changed
- **🔄 Reverted to single `commands.py`** — merged all modular command files back into one monolithic `commands.py` for simplicity

---

## [3.1.43] - 2026-06-08

### Changed
- **🔄 Commands modularized** — split monolithic `commands.py` (1529 lines) into 10 focused modules:
  - `commands/uploads.py` — `/tupload`, `/gdupload`, `/drupload`, `/ytupload`, `/glupload`
  - `commands/settings.py` — `/settings`, `/format`, `/speed`
  - `commands/help.py` — `/start`, `/help`, `/about`, help categories & commands dict
  - `commands/status.py` — `/status`, `/stats`, `/ping`
  - `commands/queue.py` — `/queue`, `/cancel`, `/cancel_all`
  - `commands/admin.py` — `/admin`, `/broadcast`
  - `commands/cookies.py` — `/cookies`, `/setcookies`, `/clearcookies`
  - `commands/userbot.py` — `/userbot`, `/userbot_status`, `/userbot_logout`
  - `commands/system.py` — `/restart`, `/update`, `/logs`
  - `commands/utility.py` — `/setname`, `/formats`, `/preview`, `/zipaswd`, `/unzipaswd`

- **📦 Package structure** — `leechbot/commands/` is now a proper Python package with `__init__.py` that imports all modules

### Improved
- **🔍 Better maintainability** — each command group is isolated, easier to locate and modify
- **📝 Clearer imports** — modules only import what they need, reducing coupling
- **🚀 Same behavior** — all handlers register via decorators; no functional changes

### Fixed
- **🐛 ModuleNotFoundError** — removed leftover `telegram.py` import from `leechbot/downloader/__init__.py` that caused `ModuleNotFoundError: No module named 'leechbot.downloader.telegram'`

---

## [3.1.42] - 2026-06-07

### Changed
- **🎨 Professional UI rewrite** — status bar and task complete message redesigned with clean box-drawing:

**Status Bar (3.1.42):**
```
┌───────────────────────────────┐
  ████░░░░  **75.00%**
├───────────────────────────────┤
  ⚡  **Speed**      →  `5.2 MB/s`
  ⏳  **ETA**        →  `10s`
  📦  **Processed**  →  `156 / 208 MB`
  ⏱️  **Elapsed**    →  `30s`
  🔧  **Engine**     →  `yt-dlp`
└───────────────────────────────┘
```

**Task Complete (3.1.42):**
```
┌───────────────────────────────┐
      ✅  **TASK COMPLETE**
├───────────────────────────────┤
  📛  **Name**    →  `IMG_5746.MOV`
  📦  **Size**    →  `5.95 MiB`
  📋  **Files**   →  `1`
  ⚡  **Speed**   →  `6.6 MB/s`
  ⏱️  **Time**    →  `1m 30s`
└───────────────────────────────┘
  🤖  LeechBot  •  v3.1.42
```

- Aligned labels with padding for clean column look
- Arrow `→` instead of `»` for better readability
- Double-line box borders `┌├└` for professional appearance
- Version shown in task complete footer

---

## [3.1.41] - 2026-06-07

### Changed
- **✅ Task Complete message upgraded** — added average speed and cleaned up layout:

**Before:**
```
✅ **Task Complete**

╭📛 **Name** » `IMG_5746.MOV`
├📦 **Size** » `5.95 MiB`
├📋 **Files** » `1`
├⏱️ **Time** » `1m 30s`
╰🤖 **By** » LeechBot
```

**After:**
```
✅ **Task Complete**

╭📛 **Name** » `IMG_5746.MOV`
├📦 **Size** » `5.95 MiB`
├📋 **Files** » `1`
├⚡ **Speed** » `6.6 MB/s`
├⏱️ **Time** » `1m 30s`
╰🤖 **By** » LeechBot
```

- Source link now inline: `🔗 **Source** » [Here](link)`
- Average speed calculated from total bytes / elapsed time

---

## [3.1.40] - 2026-06-07

### Changed
- **📤 Upload chunk_size increased to 5MB** — from 2MB (previous) / 1MB (original default):
  - 5x fewer HTTP round-trips than original
  - ~2.5x faster than 2MB setting
  - Telegram supports up to 50MB for bots; 5MB is optimal speed/memory balance

---

## [3.1.39] - 2026-06-07

### Changed
- **📤 Upload speed optimized** — increased Pyrogram chunk_size from 1MB (default) to 2MB:
  - Larger chunks = fewer HTTP round-trips = faster upload
  - Telegram supports up to 50MB chunks for bots; 2MB is a safe speed/memory balance
  - Applied to all upload types: video, audio, photo, document, batch photos

---

## [3.1.38] - 2026-06-07

### Changed
- **✅ Task Complete message — box-drawing style** — completion summary now matches the status bar's `╭├╰` layout:

**Before:**
```
✅ **Task Complete**

• 📛 **Name:** `IMG_5746.MOV`
• 📦 **Size:** `5.95 MiB`
• 📋 **Files:** `1`
• ⏱️ **Time:** `1m 30s`
• 🤖 **By:** LeechBot
```

**After:**
```
✅ **Task Complete**

╭📛 **Name** » `IMG_5746.MOV`
├📦 **Size** » `5.95 MiB`
├📋 **Files** » `1`
├⏱️ **Time** » `1m 30s`
╰🤖 **By** » LeechBot
```

- File list header also uses box-drawing: `╭📋 **Files** » 3` / `╰📜 **Logs:**`

---

## [3.1.37] - 2026-06-07

### Changed
- **📊 Status bar — box-drawing style** — adopted [ehraz786/tgdl](https://github.com/ehraz786/tgdl) layout for cleaner visual hierarchy:
  - `╭├╰` box-drawing characters create a structured vertical list
  - Each stat (Speed, Engine, Time Left, Time Spent, Processed, Total Size) on its own labeled line
  - Progress bar wrapped in `「」` brackets
  - Percentage now shows 2 decimal places (`75.00%` instead of `75.0%`)

**Before (3.1.36):**
```
████████░░░░ **75.0%**

⚡ `5.2 MB/s` · ⏳ `10s`
📦 `156 / 208 MB` · ⏱️ `30s`
🔧 `yt-dlp`
```

**After (3.1.37):**
```
╭「████████░░░░」 **»** __75.00%__
├⚡️ **Speed »** __5.2 MB/s__
├⚙️ **Engine »** __yt-dlp__
├⏳ **Time Left »** __10s__
├🍃 **Time Spent »** __30s__
├✅ **Processed »** __156 MB__
╰📦 **Total Size »** __208 MB__
```

---

## [3.1.36] - 2026-06-07

### Changed
- **📊 Status bar upgraded** — the download/upload progress bar is now cleaner and less noisy:
  - **Progress bar without backticks** — the bar was previously wrapped in backticks (`\`████░░░░\``), which looked ugly in Telegram. Now renders as plain `████░░░░` (cleaner monospace in Telegram's fixed-width font).
  - **Compressed info: 3 lines → 2 lines** — speed + ETA on one line, done/total + elapsed on one second. Less scrolling, same information density.
  - **System info removed from default view** — `sysINFO()` (CPU / RAM / disk) was previously appended to every 3-second progress update. This was noisy and distracted from the actual download progress. System info is now shown **on-demand** only when the user clicks:
    - **🔄 Refresh** — appends compact system info inline
    - **📊 Stats** — replaces the progress bar with detailed system info (CPU, RAM, disk, network, uptime)
  - **Removed `Messages.task_msg` prefix** — the status bar used to prepend `Messages.task_msg` (e.g. "**🎯 Task Mode:** ") to every update. This was redundant — downloaders already set `Messages.status_head` which contains the heading. Removed from the status bar; still used by other callers (gallery, manager, converters, handler).

### New status bar layout
```
📥 Downloading Link 01

`video.mp4`

████████░░░░ **75.0%**

⚡ `5.2 MB/s` · ⏳ `10s`
📦 `156 / 208 MB` · ⏱️ `30s`
🔧 `yt-dlp`
```

**Before (3.1.35):**
```
📥 Downloading Link 01

`video.mp4`
`████████░░░░` **75.0%**

• ⚡ `5.2 MB/s` · 📦 `156 MB` / `208 MB`
• ⏳ `10s` · ⏱️ `30s`
• 🔧 `yt-dlp`

─── System ───
• 🖥️ `23%` · 💾 `45 MB RAM` · 💽 `2.3 GB free`
```

**After (3.1.36):**
```
📥 Downloading Link 01

`video.mp4`

████████░░░░ **75.0%**

⚡ `5.2 MB/s` · ⏳ `10s`
📦 `156 / 208 MB` · ⏱️ `30s`
🔧 `yt-dlp`
```

(No more system info on every update — click "📊 Stats" to see it.)

### Tests
- **New `test_status_bar()`** with 8 sub-checks:
  - `status_bar` docstring mentions on-demand system info
  - `Messages.task_msg` NOT used in status bar (removed redundancy)
  - `sysINFO()` NOT appended to default status bar (on-demand only)
  - Progress bar has no backticks (clean monospace)
  - Info compressed to ≤3 lines (was 3 with bullet points)
  - `status_keyboard()` defined with expected buttons
  - Refresh + Stats + Cancel buttons all present
- **Test count:** 83 → 91 checks. All passing.

### Files
- `leechbot/utility/helper.py` — rewrote `status_bar()` (removed backticks, compressed info, removed `Messages.task_msg` and `sysINFO()` from message), updated `status_keyboard()` docstring.
- `tests/test_diagnostics.py` — added `test_status_bar()` (8 sub-checks); renumbered `test_syntax` from #10 to #11.

---

## [3.1.35] - 2026-06-07

### Changed
- **📝 WELCOME_TEXT trimmed from 35 lines to 9 lines** — the `/start` message used to be a wall-of-text that duplicated what `/help` now shows. Since 3.1.34 added the category-button `/help` UI, the welcome text just needs to greet + point to the right buttons. Removed: full command list, "Advance Tools" section, "Upload To" section, developer link at the bottom. Kept: bot name, one-line tagline, one-line usage hint, button navigation.

### Added
- **🆕 ℹ️ About button in welcome message** — new inline button "ℹ️ About" on the `/start` keyboard. Clicking it shows an about card with:
  - **Version** (read from `config.VERSION` — auto-updates)
  - **Build date** (read from `config.BUILD_DATE`)
  - **Stats**: live counts of commands, categories (from `HELP_CATEGORIES` + `HELP_COMMANDS`)
  - **Developer credits**: Shinei Nouzen + GitHub link
  - **License**: MIT
  - **Feature list** (condensed)
  - **Disclaimer** (copyright reminder)
- **🆕 📖 Help button in welcome message** — "📖 Help" button (callback_data=`help_main`) opens the category-button `/help` menu from 3.1.34. Replaces the old "📂 GitHub" / "🔔 Updates" / "Support" link row at the top of the keyboard — those are now in row 3-4.
- **🆕 `start_back` callback** — new "⬅️ Back to Start" button on the About card. Clicking it re-edits the message in place to show the welcome screen again. No need to retype `/start`.
- **🆕 `_start_keyboard()` helper** — extracted the welcome keyboard into a function so both the `/start` command and the `start_back` callback can use the same keyboard layout. Single source of truth.
- **🆕 `_send_welcome()` helper** — extracted the "send welcome" logic so it works for both the `/start` command and the `start_back` callback. Supports `edit=True` (re-edit message in place) and `edit=False` (delete + reply) modes.

### New welcome keyboard layout (4 rows, 2 buttons + 3 link buttons)

| | |
|---|---|
| **📖 Help** | **ℹ️ About** |
| **🤖 Bot Settings ⚙️** | |
| **📂 GitHub** | **🔔 Updates** |
| **💬 Support** | |

(Two new navigation buttons at the top, all 3 external link buttons still present.)

### New About card layout

| | |
|---|---|
| **📖 Help** | **⚙️ Settings** |
| **📂 GitHub** | **💬 Support** |
| **⬅️ Back to Start** | |

(Quick-jump to Help/Settings from About, plus the link pair, plus Back to Start.)

### Tests
- **New `test_welcome_about()`** with 24 sub-checks:
  - `WELCOME_TEXT` shortened (≤10 lines, was 35+)
  - `WELCOME_TEXT` no longer lists commands (those moved to `/help`)
  - `_start_keyboard()` and `_send_welcome()` helpers exist
  - `start_command` uses `_send_welcome` helper (no inline keyboard)
  - All 3 callback buttons present in welcome (`help_main`, `about`, `settings_menu`)
  - `_handle_about` and `_handle_start_back` defined in `callbacks.py`
  - `ABOUT_TEXT` template defined with all 4 placeholders (`version`, `build_date`, `n_cmds`, `n_cats`)
  - About uses `config.VERSION`, `config.BUILD_DATE`, `HELP_CATEGORIES`, `HELP_COMMANDS` (no hardcoded values)
  - About credits developer + mentions license
  - "Back to Start" button present
  - "about" and "start_back" callback patterns routed
- **Test count:** 47 → 71 checks. All passing.

### Files
- `leechbot/commands.py` — `WELCOME_TEXT` shrunk 35→9 lines, added `_start_keyboard()` + `_send_welcome()` helpers, rewrote `start_command` to use helper.
- `leechbot/callbacks.py` — added `_handle_about()` and `_handle_start_back()` callbacks, added `ABOUT_TEXT` template, wired 2 new callback patterns (`about`, `start_back`).
- `tests/test_diagnostics.py` — added `test_welcome_about()` (24 sub-checks); renumbered `test_syntax` from #8 to #9.
- `CHANGELOG.md`, `ROADMAP.md` updated.

### Backwards compatibility
- `/start` still works (just shorter text + new buttons)
- Old "📂 GitHub" / "🔔 Updates" / "Support" buttons are still present (just in different rows)
- No existing commands changed behavior
- No new dependencies

---

## [3.1.34] - 2026-06-07

### Added
- **🎨 Category-button /help UI** — `/help` no longer dumps a wall of text. It now opens an interactive inline-keyboard menu with 6 categories:
  - 📥 **Downloads** (10 commands) — tupload, gdupload, drupload, ytupload, glupload, setname, format, formats, preview, speed
  - 🗂 **Files** (5 commands) — zipaswd, unzipaswd, queue, cancel, cancel_all
  - ⚙️ **Status & Settings** (7 commands) — settings, status, stats, logs, ping, restart, update
  - 👤 **Account** (3 commands) — userbot, userbot_status, userbot_logout
  - 🍪 **Cookies** (3 commands) — cookies, setcookies, clearcookies
  - 🛠 **Admin** (2 commands) — admin, broadcast
- **🆕 Deep-link help: `/help <command>`** — type `/help ytupload` to get a detailed help card for that command directly, skipping the menu. If the command doesn't exist, the user gets the category menu + a "command not found" warning so they can still browse.
- **🆕 Per-command detail card** — clicking any command button in a category shows:
  - Title + category badge
  - One-line description
  - Usage: `/command <args>`
  - 1-3 worked examples
  - "Back to category" + "Main menu" + "Close" navigation buttons
- **🆕 Navigation pattern** — same UX as `BotFather`, `SpamBot`, and modern Telegram bots. Click button → message **edits in place** (no spam, no scroll-back). No new messages for each click.
- **🆕 Close button** — the ❌ button at the bottom of every help view deletes the help message (cleaner than leaving it open).

### Changed
- **`/help` command rewritten** — from 56-line static `help_text` + 3-link keyboard to 6-category dynamic menu backed by `HELP_CATEGORIES` and `HELP_COMMANDS` data tables.
- **Data-driven help** — all 30 commands now live in `HELP_COMMANDS` dict in `leechbot/commands.py` with `category`, `title`, `short`, `usage`, `examples` fields. Adding a new command = add one entry to both dicts, and it auto-appears in `/help`. No more editing wall-of-text.
- **Inline keyboard navigation** — `help_main` shows categories, `help_cat_<key>` shows commands in that category, `help_cmd_<name>` shows command detail. Three-tier drill-down.

### Why category buttons (not WilliamButcherBot's plugin loader)
- The plugin-loader pattern (`__MODULE__` + `__HELP__` per file) is great for *modular* bots where anyone can drop in a `.py` file. LeechBot is a *single-codebase* downloader bot — adding the plugin loader would be 300+ lines of refactor for a UX that ships in 200 lines of new code here.
- The category-button pattern is **the actual UX win** (drill-down, in-place editing, visual grouping) — that's what we adopted.

### Tests
- **New `test_help_system()`** with 13 sub-checks:
  - `HELP_CATEGORIES` exists (6 categories verified)
  - `HELP_COMMANDS` exists (30 commands verified)
  - Every category command has a `HELP_COMMANDS` entry (no orphans)
  - Every `HELP_COMMANDS.category` references a valid `HELP_CATEGORIES` key (no broken refs)
  - Every `HELP_COMMANDS` entry has all required fields (`category`, `title`, `short`, `usage`)
  - `help_command` uses all 3 renderers (`_help_render_main`, `_help_render_category`, `_help_render_command`) + deep-link branch
  - All 3 callback handlers defined in `callbacks.py` (`_handle_help_main`, `_handle_help_category`, `_handle_help_command`)
  - All 4 callback patterns routed (`help_main`, `help_close`, `help_cat_` prefix, `help_cmd_` prefix)
- **Test count:** 34 → 47 checks. All passing.
- Uses **AST parsing** of the source file to verify the data tables — no need to import `commands.py` (which pulls in `psutil` and breaks offline tests).

### Files
- `leechbot/commands.py` — added `HELP_CATEGORIES` dict (6 entries, 30 cmds), `HELP_COMMANDS` dict (30 entries with title/short/usage/examples), 3 renderer functions (`_help_render_main`, `_help_render_category`, `_help_render_command`), rewrote `help_command` (15 lines vs 56 lines).
- `leechbot/callbacks.py` — added 3 callback handlers (`_handle_help_main`, `_handle_help_category`, `_handle_help_command`), wired 4 callback patterns in the main router.
- `tests/test_diagnostics.py` — added `test_help_system` (13 sub-checks); renumbered `test_syntax` from #7 to #8.
- `CHANGELOG.md`, `GUIDE.md`, `ROADMAP.md` updated.

### Backwards compatibility
- `/help` still works (now with category menu instead of wall of text)
- `/help <command>` is **new** — old behavior was just to show the same wall of text
- No existing commands changed behavior
- No new dependencies
- No API breakage

---

## [3.1.33] - 2026-06-07

### Changed
- **🔧 Telegram downloader: ported xditya/GetRestrictedMessages parser logic** — the parsing algorithm from [xditya/GetRestrictedMessages](https://github.com/xditya/GetRestrictedMessages) is now adapted to our Pyrogram-based downloader. The original repo uses Telethon (different framework); we kept the *parsing pattern* (cleaner `parts[2 if parts[1] in ['c', 's'] else 1]` indexing, digit validation, peer-type inference) and dropped the Telethon-specific bits. The new code lives in `_parse_telegram_link()` inside `leechbot/downloader/telegram.py`. See "Attribution" at the bottom of this entry.

### Added
- **🆕 Slug-form links: `t.me/s/USERNAME/MSG_ID`** — the public-channel "slug" form was previously rejected (would fall through to the public branch but with `parts[1] = 's'` and crash on the `-100` prefix logic). Now correctly routed as a public link. Example: `https://t.me/s/TelegramTips/123`.
- **🆕 Discussion-thread links: `t.me/c/CHAT_ID/MSG_ID/THREAD_ID`** — links to a reply inside a discussion group attached to a channel. The 4-segment form was previously crashing on `int(parts[-1])` because `parts[-1]` was the thread ID, not the parent message ID. Now the parent message ID (`parts[3]`) is used and the thread ID is silently ignored for the fetch (Pyrogram's `get_messages` does not support fetching a specific thread reply position; the parent message is downloaded instead).
- **🆕 `http://` URLs** — the old parser only handled `https://`. Now both `http://` and `https://` are accepted (Telegram redirects them anyway, but some older mobile clients still share the `http://` form).
- **🆕 `telegram.me` mirror** — Telegram's old `telegram.me` URL mirror is now supported alongside `t.me`.

### Improved
- **Better error messages** — invalid links now show the user *which* formats are expected, e.g. `"Invalid Telegram link: 'foo'. Expected formats: t.me/USERNAME/MSG_ID, t.me/s/USERNAME/MSG_ID, t.me/c/CHAT_ID/MSG_ID"`. Missing-media errors now include the resolved `(chat_id, msg_id)` pair and a hint about membership. Borrowed from xditya's friendlier error UX (their `await event.reply("Invalid link?")` style).
- **Stricter validation** — `message_id_str.isdigit()` is checked *before* `int()` conversion, eliminating the `ValueError` that happened on `t.me/c/123/notanumber` style inputs. Edge cases like `https://t.me/c/1234567890` (no message ID) and `https://t.me/yunavip` (no message ID) now cleanly return `(None, None)` instead of raising.

### Tests
- **`test_telegram_parser()`** — expanded from 6 to 23 sub-checks:
  - All 3 original public/private cases (regression coverage)
  - 2 new slug-form cases (`s/` prefix, with/without trailing slash)
  - 1 new discussion-thread case (4-segment URL)
  - 2 new `http://` cases (public + slug)
  - 1 new `telegram.me` mirror case
  - 6 new invalid-input cases (garbage, empty, non-numeric, missing IDs, non-t.me domain)
  - 6 new source-file checks (xditya credit in docstring, `_parse_telegram_link` function exists, all 4 formats listed in module docstring)
- **Test count:** 16 → 34 checks. All passing.

### Attribution
- **Original algorithm:** [xditya/GetRestrictedMessages](https://github.com/xditya/GetRestrictedMessages) by [@xditya](https://xditya.me), licensed under AGPL-3.0.
- **Port to Pyrogram:** the parsing pattern (parts indexing, digit validation, peer-type inference) and the friendly-error UX are adapted from xditya's `main.py`. The Telethon-specific bits (`TelegramClient`, `StringSession`, `@client.on(events.NewMessage(...))`) are replaced with Pyrogram equivalents (`pyrogram.Client`, `app.get_messages`, `message.download`).
- **Why not just use xditya's code directly?** The project is built on Pyrogram 2.0.106 (per `AGENTS.md`) and adding Telethon as a second framework would double the dependency surface, double the auth-flow code, and break the existing `leechbot/userbot.py` Pyrogram session manager. The parsing logic is the only useful piece — the rest is framework glue.
- **Why credit visible in the source?** xditya's algorithm is the inspiration; the function docstring and module docstring both call this out so future maintainers can find the upstream if they want the full Telethon version.

### Files
- `leechbot/downloader/telegram.py` — replaced `media_Identifier` parser; added `_parse_telegram_link()` helper; rewrote module docstring; added xditya credit; expanded error messages. 171 → 230 lines.
- `tests/test_diagnostics.py` — expanded `test_telegram_parser` from 6 to 23 sub-checks. Renumbered test sections unchanged.
- No new dependencies. No API changes to other modules. No changes to `helper.py` (the existing `is_telegram()` substring check already covers all new formats).

---

## [3.1.32] - 2026-06-07

### Fixed
- **🔴 Noisy `CancelledError` traceback on bot shutdown** — when SIGINT/SIGTERM hit (Ctrl+C, Colab runtime disconnect, `/restart`), `startup()` would call `app.stop()` which cancels Pyrogram's dispatcher mid-handler. Any pending callback (e.g. a "normal" upload-type button click) was being drained by the dispatcher and triggered a long task — `Do_Leech` → `Leech` → `upload_file` → `reply_video` → `save_file` → `queue.put`. The cancel cascaded through that stack and produced a scary traceback at the top of the user's log.

  **Fix has two parts:**
  1. **`BOT.State.shutting_down` flag** (`leechbot/utility/variables.py`) — new bool field, defaults to False. Set to True in `__main__.py:startup()` AFTER `await idle()` returns and BEFORE `await app.stop()`. This signals to all in-flight callbacks and task schedulers that the bot is shutting down.
  2. **Bail-out checks at 3 layers:**
     - `callbacks.py:_handle_upload_type` — checks the flag first thing, answers the callback with "Bot is shutting down", returns early. Prevents new long tasks from being started at all.
     - `task_manager.py:taskScheduler` — defensive second-line check. If a queued message somehow bypasses the callback (e.g. via `task_starter`), the task scheduler bails before doing any work.
     - `uploader/telegram.py:upload_file` — wraps the upload in `try/except asyncio.CancelledError`. Logs a clean "Upload of X cancelled (bot shutting down) — partial upload discarded" warning instead of letting the error propagate raw. Re-raises after logging so the dispatcher knows to stop.

### Changed
- **`leechbot/__main__.py`** — added `from leechbot.utility.variables import BOT` import; added 4-line block between `idle()` and `app.stop()` that sets `BOT.State.shutting_down = True` and logs "🛑 Shutdown signal received — blocking new tasks, draining queue...".
- **`leechbot/callbacks.py:_handle_upload_type`** — added 11-line guard at the top. When shutting down, logs a warning, sends a `callback_query.answer("⏳ Bot is shutting down, try again later.")` with `show_alert=True`, and returns without starting any task.
- **`leechbot/utility/task_manager.py:taskScheduler`** — added 6-line guard at the top (defensive second line).
- **`leechbot/uploader/telegram.py:upload_file`** — added `import asyncio` and `except asyncio.CancelledError` block (10 lines, including the `raise` re-raise).
- **`tests/test_diagnostics.py`** — added new `test_shutdown_flag()` function with 7 sub-checks: attribute exists, default value, toggle-ability, main.py order, callbacks.py check, task_manager.py check, uploader CancelledError handler. Renumbered Test 3–8 to Test 4–7 to make room. Test count: 15 → 16.

### Notes
- The CancelledError is **still re-raised** in `upload_file` after logging — this is correct. Pyrogram's dispatcher expects the handler to acknowledge the cancel by raising. We just log first so the user sees "Upload cancelled (bot shutting down)" instead of a raw `asyncio.exceptions.CancelledError`.
- This fix only affects the **shutdown** path. Mid-task `/cancel` commands still work exactly as before.
- The `shutting_down` flag is process-scoped (Python bool, not persisted). On every fresh bot start, it resets to False.
- Backwards compatible — all 16 tests pass, no API changes, no new dependencies.

---

## [3.1.31] - 2026-06-07

### Removed (Breaking)
- **Bunkr downloader** (`leechbot/downloader/bunkr.py`) — entirely removed. The 3.1.26 fix added `bunkr.cr` / `dl.bunkr.cr` / `balbums.st` to the domain list, but the site's scraping logic is fragile and regularly breaks. Bunkr URLs now produce a clear "no downloader found" error instead of silently hanging.
- **Instagram downloader** — entirely removed. The 3.1.28 fix routed Instagram to yt-dlp first with gallery-dl as fallback, but Instagram's anti-bot measures make it untestable in CI and unreliable in production. Instagram URLs (`instagram.com`) no longer match `is_ytdl_link()`, `is_gallery()`, or any downloader. They will produce a clear "unsupported link" error.

### Code changes
- **`leechbot/downloader/bunkr.py`** — file deleted (was 7184 bytes).
- **`leechbot/utility/helper.py`** — removed `is_bunkr()` and `is_instagram()` functions; removed Bunkr branch from `detect_link_type()`; removed `instagram.com` from `is_ytdl_link()` domains list.
- **`leechbot/downloader/manager.py`** — removed `is_bunkr` and `is_instagram` from imports; removed the Instagram routing block (26 lines: yt-dlp-first + gallery-dl fallback) and the Bunkr routing block (3 lines).
- **`leechbot/downloader/gallery.py`** — removed `instagram.com` from `GALLERY_SITES`; removed Instagram branch from `get_gallery_name()`.
- **`leechbot/downloader/__init__.py`** — removed `bunkr_download` and `is_bunkr_link` from imports and `__all__`.
- **`leechbot/commands.py`** — removed Instagram example URL from `WELCOME_TEXT` gallery-link pattern.
- **`tests/test_diagnostics.py`** — removed `test_bunkr_domains()` (~62 lines) and `test_instagram_routing()` (~38 lines); removed Bunkr/Instagram rows from `test_domain_helpers`; removed `is_bunkr` and `is_instagram` from helper imports. Test count: 35 → 15.

### Documentation
- **`README.md`** — removed Instagram and Bunkr from Features, Supported Sources, and the project structure tree.
- **`GUIDE.md`** — removed Instagram and Bunkr from Video Platforms, Photo Galleries, Direct Downloads tables; updated Demo 4 (photo gallery) to remove Instagram example.
- **`ROADMAP.md`** — added 3.1.31 row at top of "Done (Recent)"; removed 3.1.26 and 3.1.28 fix rows; annotated 3.1.1 row to mark Bunkr as "removed in 3.1.31".
- **`AUDIT_REPORT.md`** — TL;DR updated to reflect 2 bugs found + 2 fixes reverted in 3.1.31; §11.3 and §11.4 replaced with a "REMOVED" entry explaining the rationale; §15 "What changed" table now shows the full 3.1.20 → 3.1.31 timeline with reverted entries marked.
- **`TERMUX.md`** — test-suite description table updated (4 sections, not 6) with `32 commands` (was `29`).

### Rationale
Per the developer's observation: both Bunkr and Instagram have become untestable in real production usage. Rather than ship unreliable downloaders that fail silently, we remove them outright. Users get a clear error message and can save the file to Telegram or Google Drive manually.

The 3.1.26 Bunkr fix and 3.1.28 Instagram fix are not lost — they remain in git history. If these sites become tractable again in the future, the code is still recoverable via `git log -p -- leechbot/downloader/bunkr.py`.

### Notes
- **No new features in 3.1.31.** This is a removal-only release.
- **No new bugs introduced.** All 15 remaining diagnostic tests pass.
- **Test count went DOWN from 35 to 15** because Bunkr and Instagram had ~20 dedicated checks between them. This is not a regression — those tests no longer apply to code that no longer exists.

---

## [3.1.30] - 2026-06-07

### Added
- **`/status` command** — shows active task detail (mode, elapsed time, bytes downloaded/uploaded, remaining, files sent, current link) + download queue (current + next 5 pending). Owner / allowed-users only. Self-deletes after the standard delay.
- **`/restart` command** — gracefully cancels any active task, sends a confirmation message, then sends `SIGTERM` to its own PID. The process wrapper (systemd, `docker --restart=always`, `pm2`, tmux respawn loop, Colab auto-reconnect, nohup loop) brings the bot back in 5-10 seconds. Owner-only.
- **`/logs [N]` command** — shows last N log lines (default 30, max 100). Tails from end of file efficiently (reads last 256 KB max, no full file load). Truncates to fit Telegram's 4096-char limit while keeping first + last lines. Owner-only.
- **Rotating file logger** — `leechbot/__init__.py` now configures a `RotatingFileHandler` writing to `LOGS_PATH/leechbot.log` (2 MB × 3 backups = max 8 MB on disk). Exports `LOG_FILE` constant for `/logs` to find the log file. Falls back gracefully to stdout-only if the filesystem is read-only.
- **WELCOME_TEXT updated** — quick-commands section now shows `/status`, `/ping`, `/logs` alongside existing commands.

### Changed
- **README.md** — version badge 3.1.21 → 3.1.30; new "What's New in v3.1.30" section; command count 28 → 32; new rows for `/status`, `/restart`, `/logs` in the Commands table; arch tree updated to "32 commands".
- **GUIDE.md** — auto-registration note 29 → 32 commands; new rows in the Commands Reference table for `/status`, `/restart`, `/logs`.
- **ROADMAP.md** — "Done (Recent)" table gains 3.1.30 row.

### Notes
- `/restart` relies on an external process supervisor. On bare `python -m leechbot` with no wrapper, it WILL exit and the bot will NOT come back automatically. Documented in TERMUX.md Step 7 (the 3 wrapper methods: nohup, tmux, screen).
- Log file location: `LOGS_PATH` defaults to `/tmp/leechbot/logs/leechbot.log` per `config.py`. Override `LEECHBOT_BASE_DIR` env var to relocate.
- This commit brings the count from 29 → 32 registered bot commands, all auto-registered on startup (no BotFather needed).

---

## [3.1.29] - 2026-06-07

### Added
- **`tests/test_diagnostics.py` — offline diagnostic test suite** — 35+ checks across 8 sections covering every fix from 3.1.23-3.1.28 plus all domain detection helpers, command registration consistency, version string format, and Python syntax for all 38 source files. Runs in ~2 seconds with **zero external dependencies** (no bot token, no Telegram API, no network). Use this to catch regressions locally before deploying. Soft-skips section 5 if `psutil` isn't installed (e.g. minimal dev envs).
- **TERMUX.md** — added "🧪 Running Offline Tests" section explaining how to use the new test suite on Termux, with a per-section breakdown of what each test verifies.

### Notes
- No code changes — pure testing infrastructure. Bot behavior identical to 3.1.28.
- The test suite uses pure stdlib (`ast`, `re`, `pathlib`) so it works even in stripped-down Termux installs that haven't pulled all `requirements.txt` deps yet.
- This addresses the recurring pattern of "fix pushed → user can't easily verify it works → reports another symptom that turns out to be a different bug". Now there's a 2-second local check before every deploy.

---

## [3.1.28] - 2026-06-07

### Fixed
- **🔴 Instagram downloads silently fail — "not downloading" with no useful error** — `is_gallery()` matched `instagram.com` (since it was in `GALLERY_SITES`) and routed to `gallery-dl`. But Instagram returns a login redirect for unauthenticated requests, so `gallery-dl` produced a cryptic `AbortExtraction: HTTP redirect to login page` that was logged but never surfaced to the user — DUMP channel just showed the task header with no completion or error, and the user saw "Not Downloading". Worse, for age/region-restricted content (`This content isn't available to everyone`) even logged-in gallery-dl can't fetch, but yt-dlp gives a clear actionable error.

  Fix: Added `is_instagram(link)` helper and an **Instagram-specific branch in `manager.py::downloadManager`** that tries yt-dlp first (better error messages, supports `YTDL_COOKIES_FILE` for age-restricted content) and falls back to `gallery-dl` only if yt-dlp fails. This way:
  - Public Reels/Posts → yt-dlp succeeds
  - Age/region-restricted content → yt-dlp gives clear error ("This content isn't available to everyone"), with cookies it works
  - Multi-image carousels where gallery-dl has richer metadata → fallback handles them

### Added
- **`is_instagram(link)` helper in `helper.py`** — explicit `instagram.com` substring check, separate from the broader `is_gallery` check. Will be useful for future Instagram-specific features (e.g., story downloads, highlight extraction).

### Notes
- Manual reproduction confirmed: `gallery-dl -j <instagram-url>` returns `AbortExtraction` for the exact URLs the user reported (`DP34SPPD6AA` reel, `DL4edmZPINu` post). `yt-dlp -j <same-urls>` returns the much clearer `"This content isn't available to everyone"` error.
- Recommendation for users: if the post is age-restricted or from a private account, **set Instagram cookies via `/setcookies`**. The bot already supports `YTDL_COOKIES_FILE` env var or `/setcookies` upload.
- Twitter, Pinterest, Pixiv etc. still use gallery-dl as before (they work reliably without auth).

---

## [3.1.27] - 2026-06-07

### Added
- **`TERMUX.md` — complete Termux deployment guide** — 250+ line walkthrough covering: F-Droid install vs Play Store warning, `pkg` setup, system packages (python/git/ffmpeg/aria2/p7zip/rust), repo clone with version pinning, `requirements.txt` install with compile fallback, `.env` configuration with DUMP_ID/OWNER_ID explanation, foreground sanity check, 3 methods to run 24/7 (`nohup` + `termux-wake-lock`, `tmux`, `screen`), Termux:Boot auto-start on phone boot, storage permission setup (`termux-setup-storage`), 10+ common issues + fixes (libtorrent, ffmpeg, permission denied, recursion error, address in use, etc.), update flow, uninstall flow, resource usage table.

### Notes
- Docs-only release, no code changes.
- Mentions Termux's known limitation: `libtorrent` is optional — default `ENABLE_TORRENTS=false` uses `aria2c` as fallback for magnet links.
- Tested setup commands against current Termux 0.118 (noble, Python 3.11-3.13) on Android 10+.

---

## [3.1.26] - 2026-06-07

### Fixed
- **🔴 Bunkr downloads completely broken — domain list stale** — `BUNKR_DOMAINS` in `leechbot/downloader/bunkr.py` AND the duplicated list in `is_bunkr()` in `leechbot/utility/helper.py` only contained the legacy domains `bunkr.la`, `bunkr.ru`, `bunkr.si`, `bunkr.is`, `bunkr.black`. Bunkr's current primary domain is `bunkr.cr` and the CDN lives at `dl.bunkr.cr` — neither was recognized, so `is_bunkr(link)` returned `False`, the URL fell through to a generic handler, and the task got stuck with no error log (just the task header in DUMP). Added `bunkr.cr`, `dl.bunkr.cr`, `dl.bunkr.la`, `dl.bunkr.si`, and `balbums.st` (the new album sub-site per their own notice on every file page) to both domain lists.

### Changed
- **`_get_direct_url()` — new Method 2** — the legacy "cdn" substring matcher (Method 1) only caught old `media-files.bunkr.la` style URLs. Added a dedicated `dl.bunkr.*` matcher as Method 2 so current CDN URLs (`https://dl.bunkr.cr/file/<id>/<filename>`) are caught before falling through to the generic "download" or direct-media patterns. Verified against a real Bunkr page (`https://bunkr.cr/f/...`) — correctly extracts `https://dl.bunkr.cr/file/...` link and derives filename from URL.

### Notes
- Two-place duplication (the `BUNKR_DOMAINS` list in `bunkr.py` and the inline list in `helper.py:is_bunkr`) is a known smell — flagged for future refactor (consistent with the messages.py discussion). For 3.1.26, kept them in sync manually.
- Bunkr appears to rotate domains regularly; the page itself displays "bunkr-albums.io is now balbums.st (old domain isn't working anymore)" — added that to the list as a defensive measure.

---

## [3.1.25] - 2026-06-07

### Added
- **`/ping` command** — measures Telegram round-trip latency in milliseconds, displays it as a colored 5-dot bar (🟢 Excellent < 200ms / 🟢 Good < 500ms / 🟡 Average < 1s / 🔴 Poor ≥ 1s), plus bot uptime and current version. Self-deletes after the standard delay (consistent with `/stats`, `/queue`, `/cancel`). Registered as a Telegram bot command in `_register_commands()` so it shows up in the menu automatically.

### Changed
- **GUIDE.md** — auto-registration note updated from "all 28 commands" → "all 29 commands"; added `/ping` row to the Commands Reference → Utility Commands table.

### Notes
- Pure feature add, no bug fixes. The ping measurement uses the round-trip time of `message.reply_text()` to Telegram's servers — a true client→server→client RTT, not just a `time.sleep(0)`. On a healthy Colab session this should land in the 100-300ms range.

---

## [3.1.24] - 2026-06-07

### Fixed
- **🔴 `thumbMaintainer` crashes with `os.stat(None)` for non-yt-dlp downloads** — `leechbot/utility/helper.py::thumbMaintainer()` initialized `ytdl_thmb = None` and only overwrote it if a matching `.webp/.jpg/.png/.jpeg` file existed in `Paths.thumbnail_ytdl`. The next check was `elif ospath.exists(ytdl_thmb):` — which calls `os.stat(None)` and raises `TypeError: stat: path should be string, bytes, os.PathLike or integer, not NoneType`. The TypeError was swallowed by the surrounding `try/except Exception` and logged as "Thumbnail generation error", leaving the upload to proceed with no thumbnail. Triggered by any non-yt-dlp video download (pixeldrain video, direct link, torrent with .mp4, etc.). Fixed by adding a None guard: `elif ytdl_thmb and ospath.exists(ytdl_thmb):`.

### Notes
- One-character fix (added `ytdl_thmb and` short-circuit). The error was cosmetic — uploads still succeeded, just with the system default thumbnail instead of a generated one.
- Reproduced in isolation: `os.path.exists(None)` raises the exact TypeError string the user saw in their DUMP channel.
- No test suite exists (per `AGENTS.md`), so this kind of `None` regression in low-traffic code paths is easy to miss. The fix prevents the log spam but a proper test would be useful for future regressions.

---

## [3.1.23] - 2026-06-07

### Fixed
- **🔴 Telegram public-link download broken (off-by-one in link parser)** — `leechbot/downloader/telegram.py::media_Identifier()` was using `parts[4]` to extract the chat identifier from public links like `https://t.me/yunavip/28`. That index is correct for the `/c/` private format (6 parts, chat_id is at index 4) but wrong for public links (5 parts, username is at index 3). Effect: every public-channel Telegram download since the 2026-04 refactor (`bdf8e1e`) was calling `app.get_messages("28", 28)` instead of `app.get_messages("yunavip", 28)`, producing `[400 PEER_ID_INVALID]`. Fixed by using `parts[-2]`, which is the segment immediately before the message_id in BOTH formats and works for trailing slashes too. Verified against 5 link shapes: public w/o slash, public w/ slash, /c/ w/o slash, /c/ w/ slash, public with higher msg_id. All pass.

### Notes
- One-line fix, no API changes, no behavior change for `/c/` private links.
- This bug silently regressed in 3.1.5/3.1.6 era cleanup commits; the prior public-link parser used `parts[3]` (correct) before the consolidation refactor. No test suite exists (per `AGENTS.md`), so this went undetected for ~2 months of releases.
- Symptom in DUMP channel: `Cannot access private channel ... [400 PEER_ID_INVALID]` for ANY public `t.me/<username>/<msg_id>` link, including non-NSFW channels. Private `/c/` links and UserBot-fetched content were unaffected.

---

## [3.1.22] - 2026-06-07

### Fixed
- **`/formats` and `/preview` were not registered with Telegram** — `leechbot/__main__.py::_register_commands()` builds a hardcoded list of `BotCommand(...)` entries to push to `app.set_bot_commands()` so the menu shows up in the Telegram client. The list was last updated before 3.1.21, so the two new commands (which DO have working `@app.on_message(filters.command(...))` handlers in `commands.py`) were missing from the auto-registered menu. Users would have to type the full `/formats` or `/preview` command path with the leading slash. Fixed by adding both to the registered command list. Also updated the `/stats` description from "📊 System statistics" → "📊 Bot & system statistics" to reflect the 3.1.20 lifetime-totals change. Total registered commands: 26 → 28.

### Changed
- **README.md** — version badge 3.1.15 → 3.1.21; "What's New" section rewritten for v3.1.21; command count 26 → 28; added `/formats` and `/preview` rows to the Downloads table; updated `/stats` description to mention "Bot & system statistics (lifetime totals)".
- **GUIDE.md** — auto-registration note updated from "all 23 commands" → "all 28 commands"; added `/formats` and `/preview` rows to the Commands Reference → Download Commands table; updated `/stats` description to mention "lifetime task totals + system resource info".
- **ROADMAP.md** — "Done (Recent)" table now lists 3.1.15 through 3.1.21 in reverse-chronological order, including the dead-code cleanup, the resource-leak fix, the stats-counter bug fix, the YTDL thread-safety hardening, and the 4 unwired features that landed in 3.1.21.
- **ARCHITECTURE.md** — no changes needed; only historical "since v3.1.1+" markers present.

### Notes
- This is a **docs-only release** + one real bug fix (the missing command registrations). No code behavior changes. The fix is important though: without it, `/formats` and `/preview` would only work if the user knew the command existed and typed it manually — the Telegram command menu would not show them.
- ARCHITECTURE.md, AGENTS.md, and CONTRIBUTING.md were checked and required no updates (no version numbers or feature claims that had gone stale).
- Cross-reference check: the 28 commands listed in the menu match the 28 `@app.on_message(filters.command(...))` handlers in `commands.py` exactly.

---

## [3.1.21] - 2026-06-07

### Added
- **`/formats <url>` command** — wires up the previously-unused `ytdl.list_formats()` helper. Lists all available yt-dlp formats (resolution, codec, size) for a given video URL so users can see what quality options are available before downloading. Resolves audit report item §3 (`list_formats` — "Should be wired to a `/formats` command for users to pick quality").
- **`/preview <url>` command** — wires up the previously-unused `gallery.list_gallery_content()` helper. Runs `gallery-dl -K <url>` as a dry run to show what files would be downloaded from a gallery URL, without actually downloading anything. Useful for previewing imgur/pixiv/etc. galleries. Resolves audit report item §3.
- **Multi-link support in URL handler** — wires up the previously-unused `helper.extract_links()` helper. `handle_url` in `handlers.py` now extracts ALL URLs (and magnets) from the message text using the existing `LINK_PATTERNS` regex set, not just one per line. Forwarded messages with multiple links on the same line (e.g. `https://a.com https://b.com`) or scattered through paragraphs now process all of them in series. Resolves audit report item §3.
- **Task-lifetime stats in `/stats`** — wires up the previously-unused `helper.format_stats()` helper. `/stats` now shows lifetime totals (total tasks, total bytes downloaded, total bytes uploaded, failed tasks, uptime) in addition to the existing system resource info (CPU, RAM, disk). Resolves audit report item §3.

### Changed
- **YTDL thread-safety refactor** — `downloader/ytdl.py` no longer mutates global `YTDL` state directly from yt-dlp's worker thread. Every write from `_progress_hook` and `MyLogger.debug` is now marshaled through `loop.call_soon_threadsafe` so the asyncio event loop is the single owner of `YTDL.*` attributes. The hook is built by a factory `_make_progress_hook(loop)` that captures the loop once, and updates are batched into atomic `_set_progress(speed, percentage, eta, done, left)` and `_set_header(value)` setters. Under CPython's GIL the old direct writes were atomic in practice, but they could let the event loop observe a stale-but-individually-consistent value (e.g. `percentage` updated but `speed` not yet). The new pattern is correct under PyPy and future no-GIL CPython, and verified with a real `asyncio.run()` + `threading.Thread` test (14/15 progress snapshots observed non-zero values within 50ms of write, all 5 fields stay consistent). Resolves audit report item §4.
- **UserBot logout is now defensive** — `userbot.py:272-279` wraps `os.remove()` of `.session` and `.session-journal` files in `try/except OSError` with a warning log. If the file is locked or read-only on logout, the session is still marked disconnected and the bot continues. Resolves audit report item §6.

### Notes
- All 4 unwired features from `AUDIT_REPORT.md` §3 are now exposed as user-facing commands. The `list_gallery_content` function continues to shell out to `gallery-dl -K` (dry-run mode) — no download happens during `/preview`.
- The YTDL refactor adds one event-loop round-trip per progress update (sub-millisecond), so throughput is unchanged in practice. The `loop=None` fallback in `YouTubeDL(url, loop=None)` preserves the legacy direct-write behavior for any future test code that calls it without an event loop.
- `/formats` and `/preview` were added to the text-input handler's command-exclusion list so they don't get re-routed to the userbot auth flow.
- Smoke tests run: all edited files parse cleanly, `_make_progress_hook` exercised against real threading + asyncio with race-free state updates, all 4 new wiring points verified to call the previously-unused functions.

---

## [3.1.20] - 2026-06-07

### Fixed
- **CRITICAL: `/stats` and `/botstats` always showed 0 bytes** — `task_manager.py:288-289, 332` accumulated `BotStats.total_downloaded` / `BotStats.total_uploaded` from `Transfer.down_bytes[0]` / `Transfer.up_bytes[0]`. But `Transfer.down_bytes` and `Transfer.up_bytes` are initialized to `[0, 0]` (the `[0]` is the running total stub, the `[1]` is the per-file size), and per-file sizes are appended via `.append(...)` — so `down_bytes[0]` was **always 0**. Cumulative stats never incremented past 0 in production. Fixed by replacing with `sum(Transfer.down_bytes)` / `sum(Transfer.up_bytes)`. This is a one-line semantic change (the total bytes transferred) with no performance cost. Now `/stats` and `/botstats` will show real lifetime totals across all tasks. (Audit report §1)
- **Orphan ffmpeg/zip/7z processes on /cancel** — `converters.py` had 4 `subprocess.Popen(...)` calls (video converter, zip, unzip, video split) wrapped in `while proc.poll() is None: await ...` polling loops with no `CancelledError` handler. If a user hit `/cancel` while ffmpeg/zip/7z was actively running, the cancellation would propagate up but the subprocess would keep running in the background until completion (or until the OOM killer got it). Fixed by adding a shared `_terminate_subprocess(proc)` helper (SIGTERM → 5s wait → SIGKILL) and wrapping each polling loop in `try/except CancelledError` that calls the helper then re-raises. Cleanup is best-effort and self-contained — no signal handlers, no global state. (Audit report §2)

### Removed
- **4 dead style helpers** — verified zero call sites across the codebase via `grep -rn`:
  - `style.py::style_text` — never imported, no callers
  - `style.py::style_button` — never imported, no callers
  - `style.py::mini_stats_bar` — never imported, no callers
  - `helper.py::mini_bar` — never imported, no callers
  Survivors in `style.py` (`to_small_caps`, `style_title`, `progress_text_bar`) are kept since `to_small_caps` is still used internally by `style_title` and the file remains the canonical home for Unicode-style helpers. Net code reduction: 25 lines, no behavior change. (Audit report §3)

### Changed
- **`shutil.copy` in `handler.py:146` is now defensive** — wrapped in `try/except (OSError, shutil.SameFileError) as e: logger.warning(...)`. If the source file is missing (e.g. user hit `/cancel` mid-download, or a symlink is broken), the upload pipeline previously crashed with `FileNotFoundError`. Now it logs a warning and falls back to the original path. `shutil.SameFileError` is also caught (some filesystems raise this when src == dst). (Audit report §6)

### Notes
- All changes are derived from `AUDIT_REPORT.md` §10 recommendations 1, 2, 3, and 6. Items 4 (wire up 4 unwired features) and 5 (PyPy/no-GIL hardening) are intentionally deferred — bigger effort, not what "Fix" means in a maintenance release.
- Smoke tests re-run: all 4 modified files pass `ast.parse()`, no stale symbol references. Popen + `/cancel` cleanup is testable manually by running a large zip and hitting `/cancel` mid-archive (verify with `pgrep -af ffmpeg\|zip\|7z` that the process is gone within ~5s).

---

## [3.1.19] - 2026-06-07

### Added
- **`AUDIT_REPORT.md`** — comprehensive static-analysis report covering all 35 Python files, 9,229 lines, 257 functions. Documents: 1 critical bug found (`Transfer.down_bytes[0]` stats accumulation — see report §1), 8 truly-dead functions, 1 thread-safety concern (works in CPython GIL but fragile), 4 resource-leak risks (Popen without cancel cleanup), full error-handling coverage stats (37%), structural comparison vs. `ehraz786/tgdl` (LeechBot is a strict superset). Includes prioritized recommendations for the 6 follow-up items. Report is documentation-only — no code changes in this commit.

### Notes
- This is a **documentation-only release**. The 6 recommendations in `AUDIT_REPORT.md` §10 are listed in priority order; user can pick which to apply next. Most impactful low-risk fix: the 2-line `Transfer.down_bytes[0]` → `sum(Transfer.down_bytes)` change in `task_manager.py:288-289` (see report §1).

---

## [3.1.18] - 2026-06-07

### Fixed
- **NameError on every task start** — `task_manager.py:155-157` used `os.path.join(...)` 3 times but the `os` module was never imported (only `from os import makedirs, path as ospath` was present). The first time `taskScheduler()` ran and tried to pick the random hero image, it would have crashed with `NameError: name 'os' is not defined`. Caught only because pyflakes flagged it during a full audit — not via runtime, which means it had been latent and would have hit the user on the first `/tupload` or `/glupload`. Fixed by replacing all 3 calls with `ospath.join(...)` (which is the same `os.path` module, just already imported as `ospath`). Zero behavior change, just uses the binding that was already in scope.

### Audit
- **Full static + smoke audit completed** across all 35 Python files in `leechbot/`:
  - 257 functions (142 async / 115 sync), 20 classes, 9,229 total lines
  - 0 syntax errors, 0 bare `except:` clauses, 0 `import moviepy` (cleanly removed in 3.1.16)
  - 15 downloader modules all routed in `manager.py:downloadManager()` (gdrive, telegram, gallery, hls, gofile, bunkr, catbox, streamtape, youtube, mega, terabox, pixeldrain, mediafire, torrent, default-aria2)
  - 15 link-detection helpers in `helper.py` all working (`is_google_drive`, `is_telegram`, `is_ytdl_link`, `is_mega`, `is_terabox`, `is_torrent`, `is_pixeldrain`, `is_mediafire`, `is_streamtape`, `is_hls_stream`, `is_gofile`, `is_bunkr`, `is_catbox`, `is_gallery`, `is_direct_link`)
  - Smoke tests passed: `sizeUnit` 9/9, `getTime` 8/8, `fileType` 10/10, link detection 9/9
  - `thumbMaintainer` fix from 3.1.17 verified end-to-end: bug reproduces without `original_name`, fix works with it, custom THMB_PATH still takes priority
  - The 2 remaining `asyncio.get_event_loop()` calls (`__init__.py:55`, `__main__.py:206`) are at module-level / entry-point — correct API for that scope (deprecation only applies inside `async def`)
  - `pyflakes` false positives on function-local `from … import …` patterns in `commands.py`, `manager.py` — verified the imports ARE used later in the function bodies

### Changed
- **Version bump** — `config.py` `VERSION` updated to `3.1.18`.

---

## [3.1.17] - 2026-06-07

### Fixed
- **YouTube thumbnail not showing on video uploads** — root cause: `Leech()` in `utility/handler.py` runs `shortFileName()` on the video (truncates to 60 chars) and renames the file on disk, then passes the shortened path to `upload_file()`. Inside `upload_file()`, `thumbMaintainer(file_path)` used `ospath.basename(file_path)` — the SHORTENED name — to look for the matching thumbnail in `Paths.thumbnail_ytdl`. But yt-dlp had saved the thumbnail with the ORIGINAL full title. Names didn't match → `ytdl_thmb` stayed `None` → ffmpeg fallback also returned nothing on most files → fell back to `Paths.HERO_IMAGE` (the random intro image). User saw intro image instead of the YouTube thumbnail. Fixed by adding an optional `original_name` parameter to `thumbMaintainer()` and passing `real_name` (the original title) from both call sites in `uploader/telegram.py` (video upload path line 90, and the document-fallback-for-video path line 138). `file_path` is still used for ffprobe/ffmpeg so duration detection and frame extraction work on the actual on-disk file. Lookup is now `lookup_name = original_name if original_name else ospath.basename(file_path)` — fully backward compatible, all existing callers unaffected.

### Changed
- **Version bump** — `config.py` `VERSION` updated to `3.1.17`.

### Notes
- **Architecture review** — confirmed the modular `leechbot/` package layout (downloader/, uploader/, utility/, web/, plus top-level commands/callbacks/handlers/debug/updater/userbot) is clean and well-separated. No restructuring needed. Comparison made against `ehraz786/tgdl` (the "forked inspiration" repo) — the LeechBot is a strict superset in features, with no remaining structural debt. Decision: keep current structure, surgical bug fix only.
- **Audit results** — no bare `except:` clauses, no `import moviepy` (correctly removed in 3.1.16), no syntax errors across all 18 Python files. The 2 remaining `asyncio.get_event_loop()` calls (`__init__.py:55`, `__main__.py:206`) are at module top-level / entry point — the correct API for that scope (the deprecation only applies inside async functions). No other latent bugs found in the touched area.

---

## [3.1.16] - 2026-05-10

### Fixed
- **Hero images not sending** — WebP format treated as stickers by Telegram/Pyrogram `send_photo`. Converted to optimized JPG instead. Images still compressed (15.4MB → 2.2MB, 86% reduction) and display correctly as photos.
- **Link previews in status messages** — added `disable_web_page_preview=True` to all `send_message` calls (task_manager, handlers, callbacks, handler) to prevent unwanted link previews cluttering bot messages.
- **UserBot freezing after OTP** — `verify_code` and `verify_2fa` didn't check if client was connected before calling `sign_in`/`check_password`. Connection could drop between auth steps. Added reconnection check, 30s timeout wrapper, FloodWait handling, and 1s post-auth delay for Telegram to finalize.
- **YouTube thumbnail generation failing** — moviepy not installed caused `thumbMaintainer` to return hero image with duration=0. Replaced moviepy with ffmpeg/ffprobe for both duration detection and frame extraction. moviepy now optional in converters.py (graceful fallback).
- **Hero images silently failing** — `send_photo` could crash without fallback. Added try/except around `send_photo` to fall back to text message with error logging. Added debug logging for image path resolution.

### Changed
- **Cleaner status bar** — removed box-drawing clutter from progress messages. Status bar now uses compact inline layout instead of `┏┠┗` borders. System info condensed to single line.
- **Removed all box-drawing formatting** — replaced `┏┠┗┣━┓┛` borders with `•` bullets and `─── Section ───` dividers across all messages: help menu, command prompts, settings, queue stats, broadcast results, completion logs, converter progress, admin panel, cookies status.

### Optimized
- **Hero images reduced 86% (15.4MB → 2.2MB)** — all 11 PNG hero images in `assets/images/` converted to optimized JPG. Oversized JPEGs masquerading as .png (up to 4035×2690) downscaled to 1280px width. Quality 92 with optimize flag.

## [3.1.15] - 2026-05-10

### Fixed
- **Hero image path wrong on Colab** — `ASSETS_IMAGES` pointed to `BASE_DIR/assets/images/` but images are in the repo root. Fixed to use `Path(__file__)` relative to package root. Made `HERO_IMAGE`/`DEFAULT_HERO` dynamic — picks whatever images exist in the folder, no hardcoded filenames. Gracefully falls back to text message if no images found.
- **`Image.open()` crash when hero image missing** — uploader crashed with `FileNotFoundError` if thumbnail path didn't exist. Added existence check, falls back to `None` (no thumbnail).
- **Bot completely unresponsive** — `__main__.py` never imported `leechbot.commands`, `leechbot.callbacks`, `leechbot.handlers`. Without these imports, no `@app.on_message()` or `@app.on_callback_query()` decorators registered. Bot started but responded to nothing.
- **Colab runtime disconnects on Deploy cell** — old notebook used `get_ipython().system('python3 -m leechbot')` which blocks the event loop, preventing JS keep-alive from firing. Colab's idle detection triggers and disconnects. Replaced with `subprocess.Popen` (non-blocking) + JS keep-alive daemon thread + `clear_output` monitor loop. Old notebook had no keep-alive at all.
- **Colab notebook libtorrent install** — added `python3-libtorrent` via apt with conda fallback to setup flow.
- **`info()` NameError in torrent fallback** — `manager.py` called `info()` (a notebook-only UI function) when libtorrent falls back to aria2c, causing `NameError` crash at runtime. Replaced with `logger.warning()`.
- **Wrong Colab install instruction in `_check_libtorrent()`** — `torrent.py` error message still told Colab users `!conda install -y -c conda-forge libtorrent` (conda doesn't exist on Colab). Fixed to `!apt-get install -y python3-libtorrent`.
- **Wrong Colab install instruction in FAQ** — `.github/discussions/faq.md` had same conda instruction for Colab. Fixed to apt-get.
- **`Transfer.total_down_size` not reset between tasks** — progress bar used stale size from previous task, showing wrong percentage and ETA. Added reset to 0 at task start.
- **`Paths.down_path` persists across tasks** — class variable mutation caused next task to use stale/wrong download path. Reset to default at task start.
- **`BotStats` counters never incremented** — `total_tasks`, `total_downloaded`, `total_uploaded` always showed 0. Added increments at task start and completion.
- **Shell injection risk in `converters.py`** — `subprocess.Popen(cmd, shell=True)` with f-string file paths enabled command injection via crafted filenames. Replaced all 4 instances with list-based args.
- **`asyncio.get_event_loop()` deprecated** — used in `callbacks.py`, `handlers.py`, `gdrive.py`, `helper.py`, `mega.py`, `debug.py`. Replaced with `asyncio.get_running_loop()` (works in async context, Python 3.12+ safe).
- **GoFile downloads 404** — URL used `filename` instead of `file_id`. GoFile API requires file ID in the download path.
- **`_upload_photo_with_progress` infinite recursion on FloodWait** — recursive call with no depth limit could stack overflow on repeated waits. Added max 10 retries.
- **Dead `_download()` function in `gdrive.py`** — generator function with `yield` never called (incomplete refactoring leftover). Removed.
- **Duplicate cookie config in `config.py`** — `YTDL_COOKIES_FILE` and `YTDL_BROWSER_COOKIES` defined twice. Second block silently overwrote first. Removed duplicate.
- **Bare `except:` in notebook** — caught `SystemExit`, `KeyboardInterrupt`, `MemoryError`. Changed all to `except Exception:`.
- **Unclosed file handles in notebook Deploy cell** — `log_fh` and restart handles leaked. Added tracking list `_open_handles` and cleanup on exit.
- **`isLink` filter uses `__` parameter** — shadowed Python dunder convention. Changed to `client`.
- **`MyLogger.debug` inconsistent with `warning`/`error`** — `debug` was instance method while others were `@staticmethod`. Made all `@staticmethod`.

### Changed
- **Notebook restructured to 3-cell layout** — restored old style with Drive Auth cell + monolithic Deployer cell, but with non-blocking subprocess + JS keep-alive + auto-restart. Old style used `get_ipython().system()` which blocked the event loop and caused disconnects.

---

## [3.1.14] - 2026-05-10

### Added
- **Torrent/magnet aria2c fallback**

### Fixed
- **GDrive folder size wrong for large folders** — `get_Gfolder_size()` only fetched first page (100 files). Now paginates through all files, so folders with 1000+ files show correct total size and progress bar.
- **GDrive blocks event loop** — all Google API calls were synchronous `execute()` calls that froze the entire bot during GDrive operations. Now wrapped in `asyncio.run_in_executor()` with real-time progress polling every 2 seconds.
- **GDrive no build_service() safety** — `g_DownLoad()` assumed `Gdrive.service` was initialized. Now calls `build_service()` if missing, prevents `NoneType` crash.
- **GDrive Google Apps crash** — Google Docs/Sheets/Slides in folders caused download errors. Now skipped with a log message (they can't be downloaded via API).
- **GDrive recursion limit** — deeply nested folders could hit Python's 1000-level limit. Added `MAX_FOLDER_DEPTH = 50` guard.
- **GDrive incomplete URL regex** — missed `drive.google.com/open?id=...` and `/uc?id=...` formats. Rewrote regex to cover all common GDrive URL patterns.
- **GDrive `getFileMetadata`/`get_Gfolder_size` sync-async mismatch** — made async wrappers; updated `manager.py` calls to use `await`. — if libtorrent isn't installed, magnet and torrent links now fall back to aria2c instead of failing. User sees a warning but download proceeds. This means torrent support works out-of-the-box on every platform, just slower without DHT/peer exchange.

### Added
- **`ROADMAP.md`** — future plans: rclone integration, unit tests, i18n, resume uploads, mobile dashboard. Also lists what's NOT planned (direct OneDrive/Dropbox APIs, file manager UI).

### Changed
- **Colab notebook consolidated: 6 cells → 3** — merged Google Drive Setup + Health Check into Setup cell, merged Update into Deploy cell as ACTION dropdown ("Start Bot" / "Update & Restart" / "Stop Bot"). Cleaner flow: Setup → Deploy.

### Fixed
- **Colab notebook missing libtorrent** — removed from pip (not on PyPI) but never added to Colab apt install. Added `python3-libtorrent` to system packages with apt → conda → pip fallback chain. Optional — setup continues even if unavailable.
- **Health Check missing libtorrent/megatools** — added checks for both with "optional" tag so users know what's available.

### Changed
- **All documentation updated** to reflect v3.1.12–3.1.14 changes:
  - `README.md`: version badge → 3.1.14, What's New rewrite, system deps (libtorrent, megatools), Mega.nz async status
  - `ARCHITECTURE.md`: threading model updated (async subprocess, not blocking), FloodWait retry depth, error handling examples
  - `AGENTS.md`: FloodWait max retry guidance
  - `CONTRIBUTING.md`: Docker status → ✅ Done, FloodWait retry guidance
  - `GUIDE.md`: system deps include python3-libtorrent and megatools on all platforms
  - `.github/copilot-instructions.md`: FloodWait retry guidance
  - `config.py`: VERSION → 3.1.14

### Fixed
- **`__init__.py` broken imports** — `is_gofile`, `is_bunkr`, `is_catbox` imported but functions are actually named `is_gofile_link`, `is_bunkr_link`, `is_catbox_link`. Any code importing from the package would crash with `ImportError`.
- **aria2c blocks event loop** — `subprocess.Popen` froze the entire bot during downloads. Replaced with `asyncio.create_subprocess_exec`.
- **aria2c tracker download at import time** — `subprocess.run(["wget", ...])` ran during `import leechbot.downloader.aria2`, blocking module loading. Changed to lazy-load on first download via `_load_trackers()`.
- **Upload speed/ETA wrong after 1 hour** — `progress_bar()` used `.seconds` (resets at 3600s) instead of `.total_seconds()`. Uploads >1hr showed incorrect speed and ETA.
- **Upload FloodWait recursion** — `upload_file()` called itself recursively on FloodWait, which could stack overflow on repeated waits. Added max retry depth (10) with `_retry_depth` parameter.
- **StreamTape `url` undefined** — if no regex matched, `url` was used before assignment. Added explicit `None` check with clear error.
- **GoFile/Bunkr/Catbox `__import__` hacks** — inline `__import__('datetime')` replaced with proper top-level `from datetime import datetime`.
- **GoFile no request timeout** — API calls had no timeout, dead server = bot hangs. Added 30s `aiohttp.ClientTimeout`.
- **Bunkr no request timeout** — added 60s timeout on all HTTP requests.
- **Catbox no request timeout** — added 300s timeout (catbox files can be large).
- **Pixeldrain list status timing** — status updated AFTER downloading each file, not BEFORE. Now shows correct current file name during download.
- **Pixeldrain no request timeout** — added 30s timeout on API calls.
- **Mediafire no request timeout** — added 60s timeout, deduplicated headers into module-level `_HEADERS`.
- **`global Transfer, MSG`** — removed useless `global` declaration in `upload_file()`.

### Changed
- **Dockerfile overhaul**

### Added
- **Mega.nz folder support** — folder links (`/folder/...`, `/#F!...`) now download all files recursively with per-file progress tracking and file count in status bar.
- **Mega.nz link type detection** — auto-detects file vs folder links, shows "Folder 📁" or "Mega 💾" in status bar.
- **Mega.nz error extraction** — megadl error messages (invalid link, file not found, auth failures) are parsed from output and shown cleanly instead of raw stderr dumps.
- **Mega.nz recursive file collection** — `_collect_downloaded()` walks the save directory tree to find all files from multi-file/folder downloads.
- **Mega.nz stderr capture** — errors from stderr are now parsed alongside stdout for complete error reporting.

### Fixed
- **Mega.nz downloader blocks event loop** — `mega.py` used synchronous `subprocess.Popen` which froze the entire bot during Mega downloads. Replaced with `asyncio.create_subprocess_exec` for non-blocking async execution.
- **Mega.nz fragile progress parsing** — hardcoded index positions in megadl output broke on different file names or sizes. Replaced with regex-based parser (`_PROGRESS_RE`) that handles any output format.
- **Mega.nz no install check** — bot crashed with unhelpful `FileNotFoundError` if megatools wasn't installed. Added `_check_megadl()` with clear install instructions (apt/pacman/brew).
- **Mega.nz download timeout** — no timeout meant a stalled download would hang forever. Added 10-minute idle timeout on stdout reads.
- **Mega.nz no file tracking** — didn't return downloaded file paths, so the manager couldn't track what was saved. Now scans save directory for newly created files.
- **TeraBox `global Aria2c` misuse** — `global` on a module-level import object does nothing but is misleading. Removed; `Aria2c.link_info` is accessed via the imported module reference.
- **TeraBox content-type check flawed** — checked Content-Type of the redirect response (which is always the API's response, not the file). Now probes the actual download URL to verify it returns a binary file, not an HTML page.
- **TeraBox no request timeout** — API calls had no timeout, so a hung server would block the bot indefinitely. Added 30-second `aiohttp.ClientTimeout`.
- **TeraBox error handling** — API errors, missing links, and HTTP failures now raise clear `RuntimeError` messages instead of silently failing or showing raw tracebacks.

### Changed
- **Dockerfile overhaul** — improved reliability, smaller image, proper signal handling:
  - Added `python3-libtorrent` via apt — torrent/magnet downloads now work out of the box in Docker
  - Added `tini` as PID 1 entrypoint — `docker stop` now sends SIGTERM correctly for graceful shutdown instead of hard-killing after 10s timeout
  - Megatools install: apt-first with source-build fallback (was fragile `||` chain that could leave partial builds)
  - Added `apt-get clean` before `rm -rf /var/lib/apt/lists/*` for smaller layer size
  - Added `DEBIAN_FRONTEND=noninteractive` to suppress interactive apt prompts
  - Added `--start-period=15s` to healthcheck — gives the bot time to start before first probe
  - Added `LABEL` metadata (maintainer, description, version)
  - Removed dead `chmod +x main.py` (container runs via `python3 -m leechbot`, not direct execution)

### Fixed
- **IndentationError in Colab notebook** — `Setup LeechBot` cell had credential backup/restore code at wrong indentation level inside `if os.path.exists("/content/leechbot"):` block, causing `IndentationError: expected an indented block after 'if'` on line 138. Fixed indentation so backup, cleanup, and clone logic are properly nested.
- **`python-libtorrent` not on PyPI** — `requirements.txt` listed `python-libtorrent>=2.0.0` which doesn't exist on PyPI, breaking `pip install` in Colab and all deployment platforms. Removed from pip requirements; now documented as a system package install (`apt install python3-libtorrent`, `conda install libtorrent`).
- **Torrent module crashes on import if libtorrent missing** — `torrent.py` did `import libtorrent as lt` at module level with no guard, causing `ImportError` that could break the entire bot. Added `try/except` import guard with `lt = None` fallback and `_check_libtorrent()` helper that raises a clear install instruction at call time.

---

## [3.1.11] - 2026-05-10

### Fixed
- **YouTube thumbnails not showing** — yt-dlp saved thumbnails as `%(id)s.webp` but `thumbMaintainer` looked for `%(title)s.webp`. Filename mismatch meant thumbnails were never found, falling back to generated frames.
  - `ytdl.py`: changed thumbnail template from `%(id)s.%(ext)s` to `%(title)s.%(ext)s`
  - `helper.py`: `thumbMaintainer` now checks multiple extensions (`.webp`, `.jpg`, `.png`, `.jpeg`) instead of hardcoding `.webp`

---

## [3.1.10] - 2026-05-10

### Added
- **`assets/images/` folder** — 6 themed hero images for task status messages
  - `hero_purple.jpg`, `hero_blue.jpg`, `hero_green.jpg`, `hero_red.jpg`, `hero_cyan.jpg`, `hero_orange.jpg`
  - Bot randomly picks a different image for each task — no two tasks look the same
  - No more downloading from `picsum.photos` — uses local files instantly
  - Users can add/remove images in `assets/images/` — bot picks from all `.jpg/.png/.webp` files

### Changed
- `variables.py`: `HERO_IMAGE`/`DEFAULT_HERO` → `assets/images/hero_purple.jpg`, added `ASSETS_IMAGES` path
- `task_manager.py`: replaced aria2c picsum download with `random.choice()` from local assets folder

---

## [3.1.9] - 2026-05-10

### Added
- **Docker support** — `Dockerfile` + `docker-compose.yml` for universal deployment
  - Multi-stage build, all system deps included (ffmpeg, aria2, megatools, p7zip, unrar)
  - Health check on `/api/health`
  - Volume mounts for sessions, downloads, thumbnails
  - GPU support (uncomment for NVIDIA)
- **Railway** — `railway.json` one-click deploy config
- **Fly.io** — `fly.toml` config with auto-restart, shared CPU, 512MB
- **Render** — `render.yaml` Blueprint auto-deploy
- **Heroku** — `Procfile` for worker dyno
- **`.dockerignore`** — clean build context
- **8 deployment methods** documented in README: Colab, Docker, Railway, Fly.io, Render, VPS, Oracle Cloud Free Tier, Heroku

### Changed
- README deployment section expanded with platform-specific instructions for all 8 methods

---

## [3.1.8] - 2026-05-10

### Removed
- **Dashboard tunnel from notebook** — ngrok/cloudflared tunnel setup removed from Deploy cell. The web dashboard still runs in the background (VPS users access it directly at `http://server:8080`), but Colab users interact 100% via Telegram. No more tunnel tokens, no more unreachable URLs.

### Fixed
- **Colab runtime still disconnects despite JS keep-alive** — Two root causes:
  1. **JS `setInterval` couldn't fire** — the Python `while True: time.sleep(15)` loop blocked the IPython event loop, preventing JS callbacks from executing. Fix: JS keep-alive now runs in a **separate daemon thread** using `google.colab.output.eval_js()` which bypasses the blocked event loop.
  2. **`\r` heartbeat wasn't counted as output** — Colab's server-side idle detection didn't recognize carriage-return-only updates as new output. Fix: uses `clear_output(wait=True)` + full `print()` every 20 seconds to force Colab to register fresh output as activity.

### Changed
- Keep-alive now uses **dual strategy**: daemon thread for JS injection (eval_js every 25s) + main loop with `clear_output` for visible output (every 20s)
- Heartbeat shows full banner + uptime + PID + last log line (not just `\r` overwrite)
- `global restart_count, bot_proc` replaces `nonlocal` (Colab IPython compat)

---

## [3.1.7] - 2026-05-10

### Added
- **🧲 libtorrent magnet/torrent downloader** — new `leechbot/downloader/torrent.py` module using python-libtorrent for magnet links and .torrent files:
  - Fast metadata retrieval via DHT with 2-minute timeout
  - Real-time progress bar with speed, ETA, peers, seeds, pieces
  - Resume data persistence — interrupted downloads resume where they left off
  - 15 built-in DHT trackers for better peer discovery
  - Sequential download mode for streaming
  - Bandwidth limit support
  - Multi-file and single-file torrent support
  - Automatic seeding after download completes
- `python-libtorrent>=2.0.0` added to `requirements.txt`
- Magnet/torrent links now route to libtorrent instead of aria2c in download manager

### Changed
- Download manager: magnet links (`magnet:`) and `.torrent` files now use dedicated libtorrent downloader instead of falling through to aria2c
- `get_d_name()`: torrent/magnet links resolve actual torrent name via metadata

---

## [3.1.6] - 2026-05-10

### Fixed
- **`SyntaxError: no binding for nonlocal` in Deploy cell** — `nonlocal` doesn't work at cell/module level in Colab's IPython kernel. Changed to `global` for `restart_count` and `bot_proc` variables used by the `restart_bot()` inner function.
- **Credentials lost on every Setup re-run** — `shutil.rmtree("/content/leechbot")` deleted `credentials.json` with the repo. Now backs up credentials to `/content/.leechbot_creds.json` before clone and restores them after, so you never have to re-enter credentials on update.

---

## [3.1.5] - 2026-05-10

### Fixed
- **Colab runtime disconnects despite keep-alive** — Root cause: the monolithic Deploy cell's `while/sleep` loop + single `setInterval` JS hack wasn't reliable against Colab's browser-side idle detection. Complete notebook restructure:
  - Split into **2 focused cells**: Setup (clone + install + configure) → Deploy (bot + tunnel + keep-alive)
  - Setup cell completes fast, Deploy cell stays alive as the single blocking cell

### Added
- **3-strategy JS keep-alive** injected at deploy time:
  - **Strategy 1:** Click runtime connect indicators (main button + shadow DOM)
  - **Strategy 2:** Simulate DOM activity (scroll, mousemove, keydown events)
  - **Strategy 3:** Focus/blur cycle to reset idle timer
  - All run every 30 seconds via JS `setInterval`
  - Python heartbeat prints status every 15 seconds (timestamp, PID, last log line)
- **Auto-restart watchdog** — if the bot process crashes, automatically restarts it (up to 5 attempts)
- **Dashboard tunnel integrated** into Deploy cell — tunnel setup happens right after bot starts, URL/token shown immediately (no separate unreachable cell)
- **📋 Cell Order table** in notebook header — clear guide for run order

### Changed
- **Notebook restructured** from 5 cells to 6 cells:
  1. Header (markdown)
  2. ♻️ Google Drive Setup (optional)
  3. 📦 Setup LeechBot (clone + install + configure — completes fast)
  4. 🚀 Deploy LeechBot (bot + tunnel + keep-alive — single blocking cell)
  5. 🔄 Update LeechBot
  6. 🔍 Health Check
- Version badge updated to 3.1.5

---

## [3.1.4] - 2026-05-10

### Fixed
- **Colab runtime keeps disconnecting** — Python `sleep` loop wasn't enough; Colab's idle detection runs in the browser, not the runtime. Added JavaScript `setInterval` that simulates user interaction every 60 seconds (clicks connect indicator, triggers DOM activity). Also added periodic heartbeat that tails the last log line.
- **Merged Deploy + Tunnel + Logs into single cell** to eliminate gaps between cells.

---

## [3.1.3] - 2026-05-10

### Removed
- **29 unused imports** across 10 files
- **250 lines of trailing whitespace** across 8 files

### Fixed
- **Duplicate function names** — `is_bunkr()`, `is_catbox()`, `is_gofile()` renamed to `is_bunkr_link()`, `is_catbox_link()`, `is_gofile_link()` in downloader modules to avoid collision with link detection helpers
- **Colab runtime disconnects after Deploy cell** — cell exited immediately after launching bot in background, causing Colab to think the session was idle and disconnect. Now waits for bot startup confirmation, then keeps the cell alive with a `while` loop that monitors the process. Cell stays running → Colab stays connected.

---

## [3.1.2] - 2026-05-10

### Fixed
- **Critical: `helper.py` SyntaxError on startup** — removed unreachable dead code (duplicate `elif is_streamtape()` / `else` block) after a `return` statement in `get_link_type()` that caused Python to refuse loading the module, crashing the entire bot on launch
- **Colab: Deploy cell blocks Dashboard Tunnel cell** — bot was launched with `get_ipython().system()` which runs as a foreground blocking process; Cell 3 (tunnel) could never execute because Cell 2 never finished. Replaced with `subprocess.Popen` so the bot runs in the background, Cell 2 completes, and the tunnel cell is now reachable

### Added
- **📋 Bot Logs & Status cell** in `LeechBot.ipynb` — new cell between Tunnel and Update that checks if the bot process is alive (via `pgrep`) and tails the last 50 lines of `bot.log` for quick debugging

### Changed
- **GUIDE.md** — updated Web Dashboard section with GitHub Pages access option, Colab cell order instructions, and Bot Logs & Status cell reference

---

## [3.1.1] - 2026-05-09

### Fixed
- **Batch photo upload crash** — `reply_media_group()` does not accept a `progress` callback (Telegram Bot API limitation); replaced with per-photo upload-with-progress strategy
- Each photo is now uploaded individually first via `reply_photo(progress=...)` with full progress bar (speed, ETA, percentage), then grouped into albums using `file_id`
- Temporary individual messages are auto-deleted after capturing `file_id`
- Media group send is instant since files are already on Telegram servers

### Added
- `_upload_photo_with_progress()` — helper that uploads a single photo with progress tracking and returns its `file_id`
- **Dashboard Tunnel cell** (optional) in `notebooks/LeechBot.ipynb` — exposes the web dashboard to the internet via ngrok or cloudflared
  - `ngrok` option — reliable, needs free authtoken (supports Colab Secrets)
  - `cloudflared` option — no signup, random URL each restart
  - Auto-detects if dashboard port is open before tunneling
  - Skippable if remote access not needed
- **Commands tab** in web dashboard — quick reference for all bot commands with tips
- **Files tab** — separated from Queue for cleaner layout
- **Version display** in login screen and footer

### Changed
- **Dashboard upgrade** — `public/index.html` fully reworked:
  - Active task now shows mode (Leech/Mirror/Gallery), engine name, speed, download progress, total size
  - Progress bar percentage calculated from server data
  - Stat cards with hover effects and pulse indicators
  - Better visual polish: fade-in animations, improved spacing, emoji labels
  - Login screen shows dashboard version and helper text
  - WebSocket fallback: REST polling only kicks in when WS is disconnected
  - HTML escaping for user content (file names, links)
  - Connection timeout (10s) with error feedback on login
- **GUIDE.md** — updated Dashboard section with Colab tunnel instructions, nginx proxy example, Commands tab mention

### Added (Agent/Developer Files)
- **`AGENTS.md`** — comprehensive instructions for AI coding agents: architecture overview, key files, state model, data flow, conventions, common tasks, known constraints
- **`ARCHITECTURE.md`** — technical deep dive: system architecture, module dependency graph, state management, request lifecycle, download/upload pipelines, web dashboard internals, error handling strategy, configuration system, threading model
- **`CONTRIBUTING.md`** — human contribution guide: setup, workflow, code guidelines, PR checklist
- **`.github/copilot-instructions.md`** — GitHub Copilot-specific instructions
- **`.cursorrules`** — Cursor IDE rules
- **`.clinerules`** — Cline rules
- **`.windsurfrules`** — Windsurf rules
- **`pyproject.toml`** — Python tooling config (ruff, mypy)
- **`.editorconfig`** — consistent formatting across editors

### Added (v3.1.1)
- **UserBot session for private channels** — login with your own Telegram account to download from private channels/groups without adding the bot as a member
  - `leechbot/userbot.py` — session manager with OTP + 2FA auth flow
  - `/userbot` — start login (phone → OTP → 2FA)
  - `/userbot_status` — check session
  - `/userbot_logout` — disconnect and remove session
  - Auto-fallback: tries UserBot first, falls back to bot client
  - Session saved locally in `sessions/userbot_session.session`
  - Startup check: logs UserBot session status on boot
- **HLS/DASH stream support** — direct `.m3u8` and `.mpd` URLs now download via yt-dlp
- **GoFile.io downloader** — API-based, supports folders, multi-file, password-protected
- **Bunkr downloader** — album + single file support (bunkr.la/ru/si/is/black)
- **Catbox.moe downloader** — direct file downloads from Catbox and Litterbox
- **StreamTape downloader** — video extraction with aria2c download
- **Massively expanded yt-dlp coverage** — 50+ domains now recognized (was 11)
  - Added: Kick, Rumble, Bilibili, SoundCloud, Spotify, Crunchyroll, VK, Odysee, Reddit video, adult sites, Chinese platforms
- **Direct link detection** — URLs with file extensions (mp4, zip, pdf, etc.) auto-detected
- **Better link type labels** — GoFile, Bunkr, Catbox, StreamTape, HLS/DASH, Direct Link, Web Link

### Changed
- `upload_photos_batch()` reworked: pre-uploads each photo with progress → groups via `file_id` instead of raw file paths
- Version bump to 3.1.1

---

## [3.1.0] - 2026-05-09

### Added
- **Web Dashboard** — real-time browser dashboard for monitoring and controlling the bot
  - `leechbot/web/server.py` — aiohttp-based REST API + WebSocket server
  - `public/index.html` — complete dashboard rewrite with live stats, queue, settings, system monitoring
  - Login screen with token auth (stored in localStorage)
  - Real-time WebSocket updates every 3 seconds
  - REST API endpoints: `/api/status`, `/api/queue`, `/api/stats`, `/api/settings`, `/api/cancel`, `/api/queue/clear`
  - Health check endpoint: `/api/health` (no auth required)
  - CORS middleware for cross-origin dashboard access
  - Auto-broadcast background task pushes state to all connected WebSocket clients
- **Dashboard features:**
  - Status cards: active/idle, downloads, uploads, task count
  - Active task card: progress bar, speed, ETA, elapsed, current file
  - Queue tab: view pending items, clear queue button
  - Settings tab: view current bot settings
  - System tab: CPU, RAM, disk usage bars
  - Recent files list
- **`WEB_PORT` env var** — configure dashboard port (default: 8080)
- **`WEB_TOKEN` env var** — set auth token (auto-generated if not set)
- Dashboard auto-starts alongside the bot

### Changed
- `__main__.py` — starts web server after bot connects, logs dashboard URL and token
- `public/index.html` — complete rewrite from Colab setup page to functional dashboard
- `README.md` — updated version badge, What's New, project structure
- `config.py` — version bump to 3.1.0

---

## [3.0.8] - 2026-05-09

### Removed
- **Removed button color styles entirely** — Pyrogram 2.0.106 predates Bot API 9.4 and does not support the `style` parameter on `InlineKeyboardButton`; keeping it would crash the bot
- Removed `leechbot/utility/compat.py` compatibility layer — unnecessary complexity; reverted to clean standard buttons
- Removed all `style=` parameters from `InlineKeyboardButton` calls across all files
- Removed `InlineButton` wrapper function — back to native `InlineKeyboardButton`

### Changed
- All buttons now use standard `InlineKeyboardButton` without `style` parameter
- Bot is clean, simple, and guaranteed to work on Pyrogram 2.0.106+
- Auto-register commands via `app.set_bot_commands()` (this works fine in 2.0.106)

---

## [3.0.7] - 2026-05-09

### Added
- **Auto-register bot commands with Telegram** — `_register_commands()` in `__main__.py` calls `app.set_bot_commands()` on startup with all 23 bot commands; no need to manually set commands via @BotFather
- Commands are registered with emoji descriptions (e.g. "📥 Upload to Telegram", "♻️ Mirror to Google Drive")

### Changed
- **Upgraded all message styles** across the entire bot with consistent box-drawing characters (`┏┣┗` borders, `┏━━━━┓` panels)
- `WELCOME_TEXT` — replaced `───────` separators with `┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓` panels, bullet lists use `┣┗` tree
- `/help` menu — complete redesign with `┣┗` tree structure for all command categories
- `/tupload`, `/gdupload`, `/drupload`, `/ytupload`, `/glupload` — all use bordered instruction panels
- `/setname`, `/zipaswd`, `/unzipaswd` — usage messages use bordered example panels
- `/queue` — session stats use `┏━━━━ **Session Stats** ━━━━┓` bordered panel
- `/broadcast` — usage and completion messages use bordered panels
- `/admin` — command list uses bordered panel, user list uses `┣` tree
- `/cookies` — status display uses bordered panel, steps use numbered tree
- `/setcookies` — instructions use bordered panel with numbered steps
- `sysINFO()` — replaced `⌬─────` with `┏━━━━ **System Info** ━━━━┓` bordered panel
- `sysINFO_full()` — same bordered panel upgrade with `┣┗` tree items
- `_strip_sysinfo()` — handles both old (`⌬─────`) and new (`┏━━━━`) formats for backward compatibility
- Upload type selection message — bordered panel with descriptions
- All command responses now use consistent `✓` suffixes on success messages

---

## [3.0.6] - 2026-05-09

### Added
- **Colored buttons across the entire bot** using Telegram Bot API 9.4 `style` parameter on `InlineKeyboardButton`
  - 🔴 `danger` (red) — Cancel, Delete, Close, destructive actions
  - 🟢 `success` (green) — Confirm, Complete, positive/active states
  - 🔵 `primary` (blue) — Navigation, Back, Settings, main actions
  - ⚪ default — Secondary options, informational toggles
- Applied to all button instances across 5 files:
  - `callbacks.py` — upload type, video/caption/thumb/autodelete/photo menus, update confirm/cancel, format/speed back buttons
  - `commands.py` — /start settings button, /format best quality, /speed unlimited, /update confirm/cancel
  - `handlers.py` — upload type selection (Regular=success), gallery cancel button
  - `helper.py` — status cancel (danger), refresh (primary), settings close (danger), auto-delete toggle (success/danger)
  - `utility/handler.py` — cancel notification keyboard (URL buttons unchanged)

### Changed
- Auto-delete toggle button dynamically switches between `success` (ON) and `danger` (OFF)
- Photo mode buttons show `success` style on the currently active option
- Settings menu close button uses `danger` style for visual clarity
- Status bar cancel button uses `danger` style consistently across all download engines

---

## [3.0.5] - 2026-05-09

### Fixed
- **callbacks.py: Massive refactor** — split monolithic 400-line `handle_callback()` into focused async functions (`_handle_upload_type`, `_handle_video_settings`, `_handle_caption_settings`, `_handle_thumb_settings`, `_handle_delete_thumb`, `_handle_autodelete_menu`, `_handle_photo_mode_menu`, `_handle_ytdl_confirm`, `_handle_do_update`, `_handle_sys_refresh`, `_handle_sys_stats`)
- **All callbacks now answer properly** — added missing `callback_query.answer()` to every callback path; users no longer see a stuck loading spinner on button press
- **cancelTask() robustness** — wrapped all operations in individual try/except blocks so a single failure (e.g., status_msg.delete()) doesn't prevent the rest of the cancellation flow from completing
- **cancelTask() crash on missing src_link** — `Messages.src_link` could be empty if task was cancelled before source log was sent; now conditionally includes the source line
- **cancelTask() getTime() crash** — was calling `.seconds` on a timedelta which loses hours/days; now uses `int(...total_seconds())` for correct elapsed time
- **SendLogs() robustness** — wrapped source reply, status edit, and file list send in individual try/except blocks; a failure in one doesn't block the others
- **SendLogs() index safety** — added bounds check for `Transfer.sent_file_names` access
- **SendLogs() empty download_name** — falls back to "Unknown" if `Messages.download_name` is empty
- **callbacks.py redundant import** — removed duplicate `import config` (already imported at module level)
- **callbacks.py fragile sysinfo parsing** — extracted `_strip_sysinfo()` helper for cleaner text manipulation in sys_refresh/sys_stats callbacks
- **do_update restart safety** — wrapped `os.execv()` in try/except with user-facing fallback message if auto-restart fails
- **Unknown callback handling** — added catch-all with `show_alert=True` so users see a proper error for unhandled callback data

### Changed
- `callbacks.py` — dispatcher now logs callback data at DEBUG level for easier troubleshooting
- `callbacks.py` — all callback errors caught and shown to user as "❌ Something went wrong" alert instead of silent failure
- `handler.py` — `cancelTask()` logs reason at INFO level for debugging
- `handler.py` — `SendLogs()` logs individual failures at ERROR level instead of silently swallowing exceptions

---

## [3.0.4] - 2026-05-09

### Fixed
- **gallery-dl downloads now show a live progress bar** with speed, file count, total size, ETA, and elapsed time — matching the aria2c and yt-dlp status bar experience
- Removed `-q` (quiet) flag from gallery-dl command to enable real-time stderr output parsing
- Added async stderr reader task for non-blocking line-by-line output capture during gallery downloads
- Gallery completion message now includes elapsed time
- **Batch photo uploads now show a live progress bar** — `upload_photos_batch()` was missing the `progress` callback, so batch uploads showed no progress until completion; added `_batch_progress()` callback with speed, ETA, and percentage
- **GDrive downloader `down_msg` NameError** — `g_DownLoad()` defined `down_msg` as a local variable but `gDownloadFile()` referenced it out of scope; replaced with `Messages.status_head` which is the shared status message pattern used by all other downloaders
- **Telegram downloader error handling** — improved error messages for public vs private channel access; better detection of missing media, empty messages, and service messages

### Changed
- `gallery_download()` now uses `status_bar()` for consistent UI across all download engines
- Progress monitoring loop reads stderr in real-time instead of only polling file count
- Added `datetime` import for proper speed/elapsed time calculation
- Added `getTime` and `status_bar` imports to gallery module
- Batch photo upload now shows batch range label (e.g. "📤 Uploading Photos 1–10/25")

---

## [3.0.3] - 2026-05-09

### Fixed
- **Critical:** `upload_photos_batch()` used wrong parameter name `media_group` for Pyrogram's `reply_media_group()` — changed to `media` (the correct Pyrogram API parameter)
- **Critical:** Batch photo retry logic used `i -= batch_size` inside a `for` loop which had no effect — refactored to `while` loop with manual index control for proper FloodWait retries
- **Critical:** Batch-uploaded photos were never cleaned up when `remove=True` — added `os.remove()` cleanup after successful batch upload
- Missing `Transfer.up_bytes` tracking in batch photo mode — upload progress now accurately reflects batch uploads
- `upload_photos_batch` was not exported from `leechbot.uploader.__init__` — added to `__all__`

### Added
- `/glupload` command — dedicated gallery-dl download mode for image galleries from Instagram, Twitter, Pinterest, Pixiv, DeviantArt, ArtStation, Flickr, Reddit, Tumblr, TikTok, Bluesky, and 100+ sites
- `BOT.Mode.gallery` flag to track gallery-dl mode state across the task pipeline
- Gallery mode label in task status display (shows "Gallery" instead of generic "Leech")
- `GUIDE.md` — comprehensive user guide covering credentials, installation, configuration, commands, settings, supported sites, Google Drive setup, YouTube auth, and troubleshooting
- 20 interactive demos in `GUIDE.md` showing real command flows: single file download, multi-link, YouTube, gallery, zip/extract, Telegram (public + private), Google Drive mirror, local directory, queuing, thumbnail, prefix/suffix, bandwidth limiting, multi-user, broadcast, update, cookie auth, cancel, auto-delete, and error recovery

### Changed
- Improved `media_Identifier()` in Telegram downloader with better error messages for public vs private channel access
- Added `message.empty` and `message.service` checks to prevent processing invalid messages
- Updated `GUIDE.md` Telegram section with clear public/private link distinction and membership requirements
- `upload_photos_batch()` now accepts `remove` parameter to match `upload_file()` cleanup behavior
- Added `import os` to `telegram.py` for file cleanup support
- Updated `/start` welcome text and `/help` menu with `/glupload` command
- All upload commands (`/tupload`, `/gdupload`, `/drupload`, `/ytupload`) now explicitly reset `gallery` flag to prevent mode leakage between tasks
- Gallery mode skips zip/unzip/undzip type selection — goes straight to download since gallery-dl only fetches images, not archives

---

## [3.0.2] - 2026-05-09

### Fixed
- **Critical:** YouTube downloads fail with "Sign in to confirm you're not a bot" error — added PO Token plugin (`bgutil-ytdlp-pot-provider`) for automatic token generation, no user action required
- **Critical:** Updated `yt-dlp` minimum version to `2025.5.22` for PO Token Provider Framework support
- `YouTubeDL()`, `get_YT_Name()`, and `list_formats()` now all use cookie options when configured
- Removed explicit `mweb` client restriction — yt-dlp auto-selects best client with full format support

### Added
- **PO Token auto-generation** via `bgutil-ytdlp-pot-provider` plugin — fully automated, no manual setup
- **🔄 Auto-Update** — `/update` command checks GitHub for new versions, shows changelog, one-click update with auto-restart
- **📸 gallery-dl integration** — download photo galleries from Instagram, Twitter, Pinterest, Pixiv, DeviantArt, ArtStation, Flickr, Reddit, Tumblr, and 100+ sites
- **📸 Photo Upload Mode** setting — choose between Group (batch of 10) or Single (one by one) via `/settings` menu
- **YT-DLP Cookie Authentication** — fallback methods to pass cookies to yt-dlp:
  - `YTDL_COOKIES_FILE` env var — path to a Netscape-format cookies.txt file
  - `YTDL_BROWSER_COOKIES` env var — extract cookies directly from a browser (chrome, firefox, edge, brave, opera, safari, vivaldi)
- `/cookies` command — shows PO token + cookie authentication status
- `/setcookies` command — step-by-step browser export instructions for cookie fallback
- `/clearcookies` command — delete stored cookies file
- **Document handler** — auto-detects `cookies.txt` uploads and saves them for yt-dlp
- Cookie options documented in `.env.example` with inline comments
- Cookie file path exposed in `Paths.ytdl_cookies` and `Paths.COOKIE_FILE` for cross-module access
- Default cookie save path: `<SESSIONS_PATH>/cookies.txt`

### Changed
- Updated `/help` command with PO token + cookie configuration section
- Updated VERSION to 3.0.2
- Redesigned Colab notebook with better UI/UX and Update cell for one-click updates
- Fixed Colab credentials loading — `credentials.json` now works as fallback for Colab compatibility
- Fixed Colab ALSA audio noise — suppressed ALSA error messages in Colab environment
- Fixed Colab session cleanup — wrong session file was being cleaned on restart

---

## [3.0.1] - 2026-05-09

### Fixed
- **Critical:** `Transfer` undefined in `/broadcast` command — would crash at runtime
- **Critical:** `Queue.size()` method missing — `/queue` command would raise `AttributeError`
- **Critical:** All `global` declarations in `handler.py`, `task_manager.py`, `converters.py`, `mega.py`, `gdrive.py` were incorrect (used `global` on class objects from another module instead of importing them)
- **Critical:** `task_manager.py` used synchronous `os.system()` for aria2c — blocked the async event loop; replaced with `asyncio.create_subprocess_exec()`
- **Critical:** `.gitignore` only contained `__pycache__/` — missing `.env`, `*.session`, `credentials.json`, `*.pickle`, IDE files, OS files
- **Critical:** `moviepy` 2.x removed `moviepy.editor` — added fallback imports in `converters.py` and `helper.py` for `moviepy` 1.x and 2.x compatibility
- **Critical:** Pyrogram Client variable named `leechbot` shadowed the `leechbot` package — renamed to `app` across all modules
- `config.py` VERSION was `1.0.0` with BUILD_DATE `2026-05-01` — mismatched README v3; updated to `3.0.0`
- `broadcast_command` referenced undefined `Transfer.sent_file` — added proper import
- `handle_text_input` handler caught ALL private text messages — now excludes known commands via `~filters.command()`

### Changed
- **Modularized `__main__.py`** (1,149 lines → 48 lines) — split into three focused modules:
  - `leechbot/commands.py` (611 lines) — all `/command` handlers
  - `leechbot/callbacks.py` (375 lines) — all inline keyboard callback handlers
  - `leechbot/handlers.py` (156 lines) — message handlers (URL, photo, text, reply)
  - `leechbot/__main__.py` (48 lines) — thin entry point that imports handlers and runs the bot
- Stored `src_request_msg` on `BOT._src_request_msg` for cross-module access between commands and handlers
- Cleaned up unused imports across `commands.py`, `handlers.py`, `downloader/mediafire.py`, `downloader/manager.py`
- All async functions now properly import their dependencies instead of using incorrect `global` declarations

### Added
- `Queue.size()` method to `DownloadQueue` class in `variables.py`
- `src_request_msg` stored on `BOT` object for cross-module handler communication

### Docs
- Updated README with v3.0.1 changelog section
- Added project structure tree to README
- Updated "Code Structure" in comparison table to reflect modularization

### Fixed (continued)
- **Critical:** Pyrogram rejects large channel IDs (>2147483647) due to 32-bit limits — patched `MIN_CHANNEL_ID` to support 15-digit Telegram IDs
- Bot startup now resolves DUMP_ID and OWNER_ID peers at launch to prevent 'Peer id invalid' errors on restarts
- System Info callbacks (`sys_refresh`, `sys_stats`) crashed on photo messages — `message.text` is `None` for photos; now falls back to `message.caption`
- `handle_reply` in handlers.py crashed on non-text replies (photo/sticker) — now checks `message.text or message.caption` and returns early if None
- Upload `progress_bar` division by zero when `Transfer.total_down_size` is 0 — added `max(..., 1)` guard
- Unguarded `os.remove()` / `os.rename()` / `shutil.rmtree()` calls across `handler.py`, `converters.py`, `helper.py`, `callbacks.py` — wrapped with try/except or `ignore_errors=True`

### Added
- `leechbot/debug.py` — Debug logging and error reporting module:
  - `TelegramLogHandler` — sends ERROR/CRITICAL logs to DUMP_ID channel in real-time
  - `AsyncExceptionHandler` — catches unhandled asyncio task exceptions and reports to Telegram
  - `send_debug()` — manual debug message sender for testing
  - All errors now appear in the DUMP_ID channel with emoji severity, timestamps, module names, and tracebacks

---

## [1.0.1] - 2026-05-09

### Fixed
- **Colab credentials not loading** — `credentials.json` is now loaded as fallback when env vars are missing (Colab notebook compatibility)
- **Colab ALSA audio noise** — suppressed ALSA error messages that spam the Colab console
- **Colab session cleanup** — fixed wrong session file being deleted on bot restart

---

## [1.0.0] - 2026-05-09

### Added
- **Complete redesign** of the Telegram Leecher codebase
- Modular architecture — separated into `commands`, `callbacks`, `handlers`, `downloader`, `uploader`, `utility`
- **Download sources:** Direct links, Google Drive, Telegram, YouTube (YT-DLP), Terabox, Mega.nz, Pixeldrain, Mediafire
- **Upload targets:** Telegram (single file + batch photos), Google Drive mirror
- **Video processing:** GPU-accelerated FFmpeg conversion, MoviePy fallback
- **Archive handling:** ZIP, RAR, 7z, TAR, GZ creation and extraction with password support
- **Smart splitting:** Auto-split files >2GB for Telegram limits
- **Interactive settings menu:** Upload mode, video settings, caption style, thumbnail, prefix/suffix, auto-delete
- **Download queue:** Queue multiple downloads, process sequentially
- **Bandwidth control:** Limit download speed via aria2c
- **Custom thumbnails:** Auto-generate from video or user-uploaded images
- **Multi-user support:** Admin panel to allow/deny users
- **Broadcast:** Send files to multiple chats
- **Auto-retry:** Configurable retry count on download failures
- **Custom naming:** `/setname` or inline `[name]` syntax
- **Password protection:** ZIP/unzip passwords via inline `{}` / `()` syntax
- **Auto-delete:** Configurable auto-delete for bot messages
- **System monitoring:** CPU, RAM, disk usage in status messages
- **Debug logging:** Error reporting to Telegram channel
- **Google Colab support:** One-click notebook deployment
- **Text styling:** Unicode small caps for consistent UI
- `style.py` — Text styling utilities
- `variables.py` — Centralized global state management
- `config.py` — Environment-based configuration with `.env` support

### Changed
- Renamed project from "Telegram Leecher" to "LeechBot"
- Replaced monolithic `__main__.py` (1,149 lines) with modular structure
- All Pyrogram client references renamed from `leechbot` to `app`
- Replaced synchronous `os.system()` calls with `asyncio.create_subprocess_exec()`
- Replaced incorrect `global` declarations with proper module imports
- Updated README with new project structure, features, and deployment guide

---

## [0.1.0] - 2026-05-09

### Added
- Initial project upload — based on [XronTrix10/Telegram-Leecher](https://github.com/XronTrix10/Telegram-Leecher)
- Basic file download and upload functionality
- Google Drive integration
- YouTube download via YT-DLP
- Aria2c download engine
- Google Colab notebook
- Basic README and requirements.txt
