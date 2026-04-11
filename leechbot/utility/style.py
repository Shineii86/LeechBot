# =============================================================================
# Telegram Leech Bot - Text Styling Utilities
# =============================================================================
# Project   : LeechBot
# Developer : Shinei Nouzen
# GitHub: @Shineii86 || Telegram: @Shineii86 || X: @Shinei86
# =============================================================================

"""
Text styling for Telegram messages using Unicode small caps.
All user‑facing messages are converted to Title Case with small‑caps letters.
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
    """Convert lowercase letters in text to small caps Unicode."""
    return ''.join(SMALL_CAPS_MAP.get(c, c) for c in text)

def style_text(text: str) -> str:
    """
    Convert text to Title Case and replace lowercase letters with small caps.
    First letter of each word remains normal uppercase, the rest become small caps.
    """
    # Split into words while preserving multiple spaces (if any)
    words = text.split(' ')
    styled_words = []
    for w in words:
        if not w:
            styled_words.append(w)
            continue
        # Capitalize first character (normal uppercase), rest small caps
        styled = w[0].upper() + to_small_caps(w[1:].lower())
        styled_words.append(styled)
    return ' '.join(styled_words)

def style_button(text: str) -> str:
    """
    Style button text. Usually we want Title Case with small caps,
    but sometimes we keep emojis and symbols.
    """
    return style_text(text)
