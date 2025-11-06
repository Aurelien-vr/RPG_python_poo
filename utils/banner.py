#!/usr/bin/env python3
"""Banner helper: render a figlet banner if pyfiglet is available."""

from typing import Optional

try:
    import pyfiglet  # optional dependency for pretty banners
except Exception:
    pyfiglet = None  # type: ignore

def banner_text(text: str, width: int = 80) -> str:
    """Return a banner string. Uses pyfiglet if available, otherwise plain text."""
    if pyfiglet:
        try:
            fig = pyfiglet.Figlet(font="slant", width=width)
            return fig.renderText(text)
        except Exception:
            return text
    return text
