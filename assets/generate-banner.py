"""Rebuild the profile artwork with Pillow: python3 assets/generate-banner.py."""

from math import pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
WIDTH, HEIGHT = 1280, 360
NAVY, MINT, WHITE, MUTED = "#0c1524", "#73e2c2", "#f1f5fb", "#a9b7cb"


def font(size, bold=False, mono=False):
    name = "DejaVuSansMono" if mono else "DejaVuSans"
    suffix = "-Bold" if bold else ""
    return ImageFont.truetype(
        f"/usr/share/fonts/truetype/dejavu/{name}{suffix}.ttf", size
    )


base = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
draw = ImageDraw.Draw(base)
for x in range(820, WIDTH, 28):
    for y in range(28, HEIGHT, 28):
        draw.ellipse((x, y, x + 2, y + 2), fill="#233047")
draw.rectangle((0, 0, 7, HEIGHT), fill=MINT)
draw.text((56, 36), "SHUNTE88 / DATA · AUDIO · CODE", font=font(17, mono=True), fill=MINT)
draw.text((52, 91), "shunte88 (Stue Hunter)", font=font(46, bold=True), fill=WHITE)
draw.text((56, 177), "Making data useful.", font=font(30), fill=WHITE)
draw.text((56, 219), "Making audio visible.", font=font(30), fill=WHITE)
draw.text((56, 303), "RUST   /   GO   /   PYTHON   /   C", font=font(17, mono=True), fill=MUTED)
draw.rounded_rectangle((850, 69, 1228, 291), radius=18, fill="#111f31", outline="#2b3c52", width=2)
draw.text((874, 90), "SIGNAL / IN MOTION", font=font(14, mono=True), fill=MUTED)
draw.line((874, 245, 1204, 245), fill="#34475e", width=1)

frames = []
for frame in range(48):
    artwork = base.copy()
    draw = ImageDraw.Draw(artwork)
    phase = 2 * pi * frame / 48
    for bar in range(24):
        envelope = sin(pi * (bar + 1) / 25)
        energy = (sin(phase + bar * 0.46) + sin(2 * phase - bar * 0.31) + 2) / 4
        height = int(14 + 100 * envelope * (0.25 + 0.75 * energy))
        x = 875 + bar * 14
        draw.rounded_rectangle((x, 243 - height, x + 8, 243), radius=3, fill=MINT if bar < 16 else "#7ca9f4")
    frames.append(artwork)

frames[0].save(OUT / "profile-banner.png")
# GIF loop=0 repeats continuously; GitHub controls autoplay per viewer.
frames[0].save(
    OUT / "profile-banner.gif",
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0,
    optimize=True,
)
