# =============================================================================
# Telegram Leech Bot - Entry Point
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================
# License   : MIT License
# You may use, modify, and distribute this code under the MIT License.
# Please retain this header when using or modifying the code.
# =============================================================================

"""
LeechBot entry point.

This module imports all handler modules to register Pyrogram handlers,
then starts the bot. Handlers are organized in:
  - leechbot.commands  — /command handlers
  - leechbot.callbacks — inline keyboard callback handlers
  - leechbot.handlers  — message handlers (URL, photo, text, reply)
"""

import os
import asyncio
import logging

from leechbot.utility.variables import BOT

# =============================================================================
# Patch Pyrogram's 32-bit peer ID limits
# Telegram supports 64-bit channel/supergroup IDs, but Pyrogram defaults
# to 32-bit MAX_INT (2147483647). This patches the limits to support
# larger channel IDs like 3030595089.
# =============================================================================
import pyrogram.utils as _pyro_utils
_pyro_utils.MIN_CHANNEL_ID = -100999999999999  # Support up to 15-digit IDs

from leechbot import app
import config

logger = logging.getLogger(__name__)

# =============================================================================
# Import handlers to register them with Pyrogram
# These imports trigger the @app.on_message() and @app.on_callback_query()
# decorators in each module. Without these, the bot is unresponsive.
# =============================================================================
import leechbot.aliases      # registers alias pre-processor before real commands
import leechbot.commands
import leechbot.callbacks
import leechbot.handlers


# =============================================================================
# Peer Resolution Helper
# =============================================================================
async def _resolve_peer(peer_id: int, label: str):
    """
    Resolve a Telegram peer ID and cache it in Pyrogram's storage.
    Tries multiple methods to handle fresh sessions and restarts.
    """
    if not peer_id:
        return

    # Method 1: Direct resolve (fast, works if peer is already cached)
    try:
        await app.resolve_peer(peer_id)
        logger.info("✅ %s peer resolved: %s", label, peer_id)
        return
    except Exception:
        pass

    # Method 2: get_chat (fetches full chat info, caches automatically)
    try:
        chat = await app.get_chat(peer_id)
        logger.info("✅ %s peer resolved via get_chat: %s (%s)", label, peer_id, getattr(chat, 'title', 'user'))
        return
    except Exception:
        pass

    # Method 3: Send a silent message to force peer resolution
    try:
        msg = await app.send_message(peer_id, "🔄 Bot restarted — peer cache refreshed.")
        await msg.delete()
        logger.info("✅ %s peer resolved via test message: %s", label, peer_id)
        return
    except Exception:
        pass

    logger.warning(
        "⚠️ Could not resolve %s (%s). "
        "Make sure the bot is a member of the chat and has permission to send messages. "
        "The bot will retry when sending the first task message.",
        label, peer_id,
    )


# =============================================================================
# Startup — resolve peers, install error reporting, enter idle loop
# =============================================================================
async def _register_commands():
    """
    Register bot commands with Telegram automatically.
    No need to set these manually via @BotFather.
    """
    from pyrogram.types import BotCommand

    commands = [
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("help", "📖 Show help & commands"),
        BotCommand("tupload", "📥 Upload to Telegram"),
        BotCommand("gdupload", "♻️ Mirror to Google Drive"),
        BotCommand("drupload", "📁 Upload local directory"),
        BotCommand("ytupload", "🏮 Download with YT-DLP"),
        BotCommand("glupload", "📸 Download image galleries"),
        BotCommand("formats", "🎞️ List available formats for a URL"),
        BotCommand("preview", "👁️ Preview a gallery URL (dry run)"),
        BotCommand("settings", "⚙️ Bot settings menu"),
        BotCommand("setname", "✏️ Set custom filename"),
        BotCommand("zipaswd", "🔐 Set zip password"),
        BotCommand("unzipaswd", "🔓 Set unzip password"),
        BotCommand("alias", "🔀 Create command alias"),
        BotCommand("aliases", "📋 List command aliases"),
        BotCommand("unalias", "❌ Remove command alias"),
        BotCommand("format", "🎬 Set YT-DLP quality"),
        BotCommand("speed", "⚡ Set bandwidth limit"),
        BotCommand("queue", "📋 View download queue"),
        BotCommand("cancel", "🚫 Cancel current task"),
        BotCommand("cancel_all", "🗑️ Cancel & clear queue"),
        BotCommand("stats", "📊 Bot & system statistics"),
        BotCommand("ping", "🏓 Check latency & uptime"),
        BotCommand("status", "📊 Active task + queue detail"),
        BotCommand("restart", "🔄 Restart the bot"),
        BotCommand("logs", "📋 Recent log lines"),
        BotCommand("admin", "👥 Manage allowed users"),
        BotCommand("rss_add", "📰 Add RSS auto-download feed"),
        BotCommand("rss_list", "📋 List RSS feeds"),
        BotCommand("rss_remove", "❌ Remove RSS feed"),
        BotCommand("rss_check", "🔍 Check RSS feeds now"),
        BotCommand("broadcast", "📢 Broadcast to chats"),
        BotCommand("cookies", "🍪 YT-DLP auth status"),
        BotCommand("setcookies", "📤 Upload cookies.txt"),
        BotCommand("clearcookies", "🗑️ Delete cookies file"),
        BotCommand("screenshot", "📸 Generate screenshots from video/PDF"),
        BotCommand("setwm", "✏️ Set watermark text for screenshots"),
        BotCommand("autorename", "🏷️ Set auto-rename template"),
        BotCommand("update", "🔄 Check for updates"),
    ]

    try:
        await app.set_bot_commands(commands)
        logger.info("✅ Registered %d bot commands with Telegram", len(commands))
    except Exception as e:
        logger.warning("⚠️ Failed to register commands: %s", e)


async def startup():
    """
    Runs once after the bot connects to Telegram.
    1. Registers bot commands with Telegram
    2. Resolves DUMP_ID and OWNER_ID peers
    3. Installs debug/error reporting to Telegram
    4. Enters idle loop
    """
    from pyrogram import idle
    from leechbot.debug import setup_error_reporting

    # Start the client first (required before resolve_peer)
    await app.start()

    # Register commands with Telegram (replaces @BotFather setup)
    await _register_commands()

    # Resolve critical peers at startup
    await _resolve_peer(config.DUMP_ID, "DUMP_ID")
    await _resolve_peer(config.OWNER_ID, "OWNER_ID")

    # Install error reporting (sends errors to DUMP_ID channel)
    await setup_error_reporting(app, config.DUMP_ID, config.OWNER_ID)

    # Start RSS auto-download poller
    try:
        from leechbot.utility.rss_manager import start_rss_poller
        start_rss_poller()
        logger.info("📰 RSS auto-download poller started")
    except Exception as e:
        logger.warning("⚠️ RSS poller failed to start: %s", e)

    logger.info("=" * 60)
    logger.info("LeechBot started successfully")
    logger.info("Developer: Shinei Nouzen")
    logger.info("GitHub: https://github.com/Shineii86/LeechBot")
    logger.info("Debug: Error reporting → DUMP_ID channel")

    # Start web dashboard server
    try:
        from leechbot.web.server import start_web_server
        import secrets
        web_port = int(os.environ.get("WEB_PORT", "8080"))
        web_token = os.environ.get("WEB_TOKEN", secrets.token_urlsafe(32))
        await start_web_server(port=web_port, token=web_token)
        logger.info("🌐 Dashboard: http://0.0.0.0:%d/dashboard", web_port)
        logger.info("🔑 Dashboard token: %s", web_token)
    except Exception as e:
        logger.warning("⚠️ Web dashboard failed to start: %s", e)

    logger.info("=" * 60)

    # Keep the bot running
    await idle()

    # Graceful shutdown — set the flag BEFORE app.stop() so that any
    # in-flight callbacks (which the dispatcher drains before stopping)
    # check this flag and bail instead of starting new long-running tasks
    # (download + upload) that will get cancelled mid-flight and produce
    # a noisy CancelledError traceback. See callbacks.py:_handle_upload_type
    # and task_manager.py:taskScheduler for the full shutdown flow.
    BOT.State.shutting_down = True
    logger.info("🛑 Shutdown signal received — blocking new tasks, draining queue...")

    # Stop RSS poller
    try:
        from leechbot.utility.rss_manager import stop_rss_poller
        stop_rss_poller()
    except Exception as e:
        logger.warning("⚠️ RSS poller stop failed: %s", e)

    await app.stop()


# =============================================================================
# Entry Point
# =============================================================================
asyncio.get_event_loop().run_until_complete(startup())
