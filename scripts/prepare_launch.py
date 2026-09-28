#!/usr/bin/env python3
"""Normalize generated HTML for the current static-site launch."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def update_page(path: Path) -> None:
    source = path.read_text()
    source = re.sub(
        r'<span><a href="https?://(?:www\.)?shinycarpetcleaning\.com/terms-conditions/">Terms</a>'
        r'<a href="https?://(?:www\.)?shinycarpetcleaning\.com/privacy-policy/">Privacy</a></span>',
        "",
        source,
    )
    source = re.sub(r"https?://(?:www\.)?shinycarpetcleaning\.com", "", source)
    source = re.sub(r"(?<![\w/])/?assets/site\.css\?v=\d+", "/assets/site.css?v=101", source)
    source = re.sub(r"(?<![\w/])/?assets/site\.js\?v=\d+", "/assets/site.js?v=53", source)
    path.write_text(source)


def main() -> None:
    pages = list(DIST.rglob("*.html"))
    for page in pages:
        update_page(page)
    print(f"Prepared {len(pages)} HTML pages for launch.")


if __name__ == "__main__":
    main()
