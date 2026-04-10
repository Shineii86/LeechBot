# =============================================================================
# LeechBot Pro - Entry Point
# =============================================================================
# Project   : LeechBot Pro v3.0
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://t.me/Shineii86
# =============================================================================

import logging
from colab_leecher import colab_bot, logger

# Import handlers to register them
from . import handlers
from . import callbacks


def main():
    """Main entry point for the bot."""
    logger.info("=" * 60)
    logger.info("LeechBot Pro v3.0")
    logger.info("Developer: Shinei Nouzen")
    logger.info("GitHub: https://github.com/Shineii86")
    logger.info("Telegram: https://t.me/Shineii86")
    logger.info("=" * 60)
    logger.info("Starting bot...")
    
    try:
        colab_bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise


if __name__ == "__main__":
    main()
