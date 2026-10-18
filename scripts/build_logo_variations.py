#!/usr/bin/env python3
"""Trace the approved Shiny PNG artwork into two-color SVG logo assets."""

from __future__ import annotations

import struct
import zlib
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "dist" / "assets" / "brand"


def read_rgba_png(path: Path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not a PNG: {path}")

    pos = 8
    chunks = defaultdict(bytes)
    width = height = color_type = bit_depth = None
    while pos < len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        kind = data[pos + 4 : pos + 8]
        payload = data[pos + 8 : pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            width, height, bit_depth, color_type, _, _, interlace = struct.unpack(
                ">IIBBBBB", payload
            )
            if bit_depth != 8 or color_type != 6 or interlace != 0:
                raise ValueError(f"Expected non-interlaced 8-bit RGBA PNG: {path}")
        elif kind == b"IDAT":
            chunks[kind] += payload
        elif kind == b"IEND":
            break

    raw = zlib.decompress(chunks[b"IDAT"])
    bpp = 4
    stride = width * bpp
    rows = []
    previous = bytearray(stride)
    offset = 0

    def paeth(a, b, c):
        p = a + b - c
        pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
        return a if pa <= pb and pa <= pc else b if pb <= pc else c

    for _ in range(height):
        filter_type = raw[offset]
        offset += 1
        source = raw[offset : offset + stride]
        offset += stride
        row = bytearray(stride)
        for i, value in enumerate(source):
            left = row[i - bpp] if i >= bpp else 0
            up = previous[i]
            up_left = previous[i - bpp] if i >= bpp else 0
            if filter_type == 0:
                result = value
            elif filter_type == 1:
                result = value + left
            elif filter_type == 2:
                result = value + up
            elif filter_type == 3:
                result = value + ((left + up) // 2)
            elif filter_type == 4:
                result = value + paeth(left, up, up_left)
            else:
                raise ValueError(f"Unsupported PNG filter {filter_type}")
            row[i] = result & 255
        rows.append(row)
        previous = row
    return width, height, rows


def masks_from_png(path: Path):
    width, height, rows = read_rgba_png(path)
    green, navy = set(), set()
    for y, row in enumerate(rows):
        for x in range(width):
            r, g, b, a = row[x * 4 : x * 4 + 4]
            if a < 80:
                continue
            target = green if g > b and g > r * 1.15 else navy
            target.add((x, y))
    return width, height, green, navy


def mask_to_loops(mask):
    edges = set()
    for x, y in mask:
        if (x, y - 1) not in mask:
            edges.add(((x, y), (x + 1, y)))
        if (x + 1, y) not in mask:
            edges.add(((x + 1, y), (x + 1, y + 1)))
        if (x, y + 1) not in mask:
            edges.add(((x + 1, y + 1), (x, y + 1)))
        if (x - 1, y) not in mask:
            edges.add(((x, y + 1), (x, y)))

    outgoing = defaultdict(list)
    for start, end in edges:
        outgoing[start].append(end)

    loops = []
    unused = set(edges)
    while unused:
        start, end = next(iter(unused))
        loop = [start, end]
        unused.remove((start, end))
        current = end
        while current != start:
            candidates = [n for n in outgoing[current] if (current, n) in unused]
            if not candidates:
                break
            nxt = candidates[0]
            unused.remove((current, nxt))
            loop.append(nxt)
            current = nxt
        if len(loop) > 3 and loop[-1] == start:
            loops.append(simplify_collinear(loop[:-1]))
    return loops


def simplify_collinear(points):
    if len(points) < 4:
        return points
    changed = True
    current = points
    while changed and len(current) > 3:
        changed = False
        result = []
        size = len(current)
        for i, point in enumerate(current):
            prev = current[(i - 1) % size]
            nxt = current[(i + 1) % size]
            if (prev[0] == point[0] == nxt[0]) or (prev[1] == point[1] == nxt[1]):
                changed = True
                continue
            result.append(point)
        current = result
    return current


def loops_to_path(loops):
    parts = []
    for loop in loops:
        if not loop:
            continue
        parts.append(f"M{loop[0][0]} {loop[0][1]}")
        parts.extend(f"L{x} {y}" for x, y in loop[1:])
        parts.append("Z")
    return "".join(parts)


def trace(path: Path):
    width, height, green, navy = masks_from_png(path)
    return {
        "width": width,
        "height": height,
        "green": loops_to_path(mask_to_loops(green)),
        "navy": loops_to_path(mask_to_loops(navy)),
    }


def svg_markup(art, *, title, navy="#233f63", green="#20a63b"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {art['width']} {art['height']}" role="img" aria-labelledby="title">
  <title id="title">{title}</title>
  <path fill="{green}" fill-rule="evenodd" d="{art['green']}"/>
  <path fill="{navy}" fill-rule="evenodd" d="{art['navy']}"/>
</svg>
'''


def group_markup(art, x, y, width, *, navy="#f7f8fa", green="#55d776"):
    scale = width / art["width"]
    return f'''<g transform="translate({x} {y}) scale({scale:.8f})">
      <path fill="{green}" fill-rule="evenodd" d="{art['green']}"/>
      <path fill="{navy}" fill-rule="evenodd" d="{art['navy']}"/>
    </g>'''


def build_sheet(artworks):
    placements = [
        (artworks["full"], 520, 60, 100),
        (artworks["horizontal"], 430, 105, 390),
        (artworks["wordmark"], 280, 180, 670),
        (artworks["symbol"], 112, 264, 840),
    ]
    groups = []
    for art, width, x, y in placements:
        groups.append(group_markup(art, x, y, width))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 1040" role="img" aria-labelledby="title desc">
  <title id="title">Shiny Carpet Cleaning responsive logo variations</title>
  <desc id="desc">Four centered logo variations descend from the full lockup to the standalone S and sparkle symbol.</desc>
  <rect width="640" height="1040" fill="#081725"/>
  {''.join(groups)}
</svg>
'''


def main():
    sources = {
        "full": ASSET_DIR / "shiny-logo-full.png",
        "horizontal": ASSET_DIR / "shiny-logo-horizontal.png",
        "wordmark": ASSET_DIR / "shiny-wordmark.png",
        "symbol": ASSET_DIR / "shiny-symbol.png",
    }
    names = {
        "full": ("shiny-logo-full.svg", "Shiny Carpet Cleaning full logo"),
        "horizontal": ("shiny-logo-horizontal.svg", "Shiny horizontal logo"),
        "wordmark": ("shiny-wordmark.svg", "Shiny wordmark"),
        "symbol": ("shiny-symbol.svg", "Shiny S and sparkle symbol"),
    }
    artworks = {key: trace(path) for key, path in sources.items()}
    for key, art in artworks.items():
        filename, title = names[key]
        (ASSET_DIR / filename).write_text(svg_markup(art, title=title))
    (ASSET_DIR / "shiny-logo-horizontal-reversed.svg").write_text(
        svg_markup(
            artworks["horizontal"],
            title="Shiny horizontal logo reversed",
            navy="#f7f8fa",
        )
    )
    (ASSET_DIR / "shiny-logo-variations.svg").write_text(build_sheet(artworks))


if __name__ == "__main__":
    main()
