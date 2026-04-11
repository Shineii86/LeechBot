# =============================================================================
# Telegram Leech Bot - Text Styling Utilities
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub    : https://github.com/Shineii86
# Telegram  : https://telegram.me/Shineii86
# =============================================================================

"""
Text styling for Telegram messages using Unicode small caps.
Only lowercase letters are converted to small caps; uppercase and other characters remain unchanged.
"""

# Mapping from normal lowercase letters to small caps Unicode
SMALL_CAPS_MAP = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ',
    'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ',
    'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ',
    'p': 'ᴘ', 'q': 'ҩ', 'r': 'ʀ', 's': 's', 't': 'ᴛ',
    'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ',
    'z': 'ᴢ'
}

def to_small_caps(text: str) -> str:
    """Convert lowercase letters to small caps Unicode; leave other characters unchanged."""
    return ''.join(SMALL_CAPS_MAP.get(c, c) for c in text)

def style_text(text: str) -> str:
    """
    Convert lowercase letters to small caps while preserving original case.
    Uppercase letters remain normal ASCII uppercase.
    """
    return to_small_caps(text)

def style_title(text: str) -> str:
    """
    Convert text to Title Case with small caps for lowercase letters.
    First letter of each word is normal uppercase, rest small caps.
    """
    words = text.split(' ')
    styled_words = []
    for w in words:
        if not w:
            styled_words.append(w)
            continue
        styled = w[0].upper() + to_small_caps(w[1:].lower())
        styled_words.append(styled)
    return ' '.join(styled_words)

def style_button(text: str, button_type: str = "default") -> str:
    """
    Style button text with Unicode small caps and emoji prefix.
    button_type: 'primary', 'success', 'danger', 'default'
    """
    emoji_map = {
        "primary": "🔵",   # Blue circle
        "success": "🟢",   # Green circle
        "danger": "🔴",    # Red circle
        "default": "⚪"    # White circle
    }
    emoji = emoji_map.get(button_type, "")
    styled = style_title(text)
    return f"{emoji} {styled}" if emoji else styled
