"""Prepare web-ready images for the General Robotics website.

Crops the painted picture out of each approved round 10 advertisement
(leaving the baked-in headline and footer behind, because the website sets
its own lettering in real text) and saves each image at several widths in
WebP with a JPEG fallback.

Also prepares the Wheeler engineering drawing and the founder portrait from
the files in _source/.

Run from the website folder:  python3 tools/prepare_images.py "/path/to/GR Branding/"
"""
import os
import sys

import numpy as np
from PIL import Image

BRAND = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/uploads/GR Branding/"
ADS = BRAND + "Campaign Concepts/10 - Corrected Emblems and Red Flags/"
EDEN = BRAND + "Logo Concepts/Taking Flight in Eden - No Suffix/01-eden-sparrow-no-suffix.png"
# Kept beside the site, outside the published files.
WHEELER = "_source/wheeler-whole.png"
PORTRAIT = "_source/founder-portrait.jpg"
OUT = "assets/img/"


def longest_run(mask):
    """Return (start, stop) of the longest run of True values in a 1-D mask."""
    idx = np.where(mask)[0]
    runs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
    run = max(runs, key=len)
    return int(run[0]), int(run[-1]) + 1


def picture_box(im, inset=3):
    """Find the painted picture inside an advertisement's paper border.

    Rows and columns belonging to the picture are those where most pixels
    differ from the paper colour; headline and footer rows are mostly paper.

    Returns:
        (left, top, right, bottom), pulled in by ``inset`` pixels.
    """
    a = np.asarray(im.convert("RGB")).astype(int)
    non = np.abs(a - a[6, 6]).sum(2) > 12
    top, bottom = longest_run(non.mean(1) > 0.6)
    left, right = longest_run(non[top:bottom].mean(0) > 0.6)
    return left + inset, top + inset, right - inset, bottom - inset


def export(im, stem, widths, quality=82):
    """Save WebP and JPEG copies at each width; return the (width, height) list."""
    sizes = []
    for w in widths:
        w = min(w, im.width)
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        r.save(f"{OUT}{stem}-{w}.webp", "WEBP", quality=quality, method=6)
        r.save(f"{OUT}{stem}-{w}.jpg", "JPEG", quality=quality, optimize=True, progressive=True)
        sizes.append((w, h))
    return sizes


def drawing(path, max_width=720):
    """Load the Wheeler engineering drawing.

    The drawing is rendered from the CAD model already in the site's ink and
    plate colours (see _source/README.md), so it only needs resizing.

    Returns:
        PIL RGB image no wider than ``max_width``.
    """
    im = Image.open(path).convert("RGB")
    if im.width > max_width:
        im = im.resize((max_width, round(im.height * max_width / im.width)), Image.LANCZOS)
    return im


def round_portrait(path, size=320):
    """Square, web-sized copy of the founder portrait."""
    im = Image.open(path).convert("RGB")
    side = min(im.size)
    left, top = (im.width - side) // 2, (im.height - side) // 2
    return im.crop((left, top, left + side, top + side)).resize((size, size), Image.LANCZOS)


def whiten_paper(im):
    """Scale an engraving so its paper becomes pure white.

    The site lays the engraving over the page with a multiply blend; with
    white paper the engraving's rectangle disappears into the page colour.
    """
    a = np.asarray(im).astype(float)
    paper = np.percentile(a.reshape(-1, 3), 97, axis=0)
    return Image.fromarray(np.clip(a / paper * 255.0, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    home = Image.open(ADS + "01-a-life-of-your-own.png").convert("RGB")
    home_pic = home.crop(picture_box(home))
    print("home", home_pic.size, export(home_pic, "home", [520, 800, home_pic.width]))
    expo = Image.open(ADS + "02-grand-exposition.png").convert("RGB")
    expo_pic = expo.crop(picture_box(expo))
    print("exposition", expo_pic.size, export(expo_pic, "exposition", [720, 1100, expo_pic.width]))
    eden = whiten_paper(Image.open(EDEN).convert("RGB"))
    print("eden", eden.size, export(eden, "eden-crest", [420, 720], quality=80))
    wheeler = drawing(WHEELER)
    print("wheeler", wheeler.size, export(wheeler, "wheeler-cad", [360, wheeler.width], quality=86))
    round_portrait(PORTRAIT).save(OUT + "founder.jpg", quality=86, optimize=True)

