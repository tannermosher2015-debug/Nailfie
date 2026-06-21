"""
Generate images/og-cover.png — the social-share preview for Nailfie Studio.
Branded placeholder (plum-ink + fuchsia, nail-tip-arch motif). Re-run after
dropping in a real hero photo if you'd rather feature her work.

    python build_og.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images", "og-cover.png")

W, H = 1200, 630
INK = (20, 16, 25)
FUCHSIA = (255, 46, 126)
PORC = (251, 246, 242)

def font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()

DISPLAY = ["C:/Windows/Fonts/ ariblk.ttf".replace(" ", ""), "C:/Windows/Fonts/Arialbd.ttf", "arialbd.ttf"]
BODY    = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/Arial.ttf", "arial.ttf"]
SEMI    = ["C:/Windows/Fonts/seguisb.ttf", "C:/Windows/Fonts/segoeui.ttf", "arial.ttf"]

img = Image.new("RGB", (W, H), INK)

# fuchsia glow, top-right
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([W - 560, -280, W + 240, 520], fill=FUCHSIA + (115,))
glow = glow.filter(ImageFilter.GaussianBlur(150))
img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))

draw = ImageDraw.Draw(img)

# nail-tip arch motif (right side), partly off-canvas
ax, aw, atop, abot, dome = 1080, 300, 150, 690, 150
arch = Image.new("RGBA", (W, H), (0, 0, 0, 0))
adraw = ImageDraw.Draw(arch)
adraw.rectangle([ax - aw // 2, atop + dome, ax + aw // 2, abot], fill=FUCHSIA + (235,))
adraw.pieslice([ax - aw // 2, atop, ax + aw // 2, atop + 2 * dome], 180, 360, fill=FUCHSIA + (235,))
# glossy highlight stripe
adraw.rounded_rectangle([ax - aw // 2 + 26, atop + 40, ax - aw // 2 + 60, abot - 30], radius=18, fill=(255, 255, 255, 60))
img.paste(Image.alpha_composite(img.convert("RGBA"), arch).convert("RGB"), (0, 0))
draw = ImageDraw.Draw(img)

# eyebrow (letter-spaced manually)
eb = font(SEMI, 26)
eyebrow = "W A I L U K U   ·   M A U I"
draw.text((90, 132), eyebrow, font=eb, fill=FUCHSIA)

# headline
f_disp = font(DISPLAY, 84)
draw.text((86, 200), "Not a", font=f_disp, fill=PORC)
draw.text((86, 296), "manicure.", font=f_disp, fill=PORC)
# "A commission." with commission in fuchsia
y2 = 392
x = 86
draw.text((x, y2), "A ", font=f_disp, fill=PORC)
xw = draw.textlength("A ", font=f_disp)
draw.text((x + xw, y2), "commission.", font=f_disp, fill=FUCHSIA)
# brushstroke under "commission."
uy = y2 + 88
draw.rounded_rectangle([x + xw, uy, x + xw + draw.textlength("commission.", font=f_disp), uy + 11], radius=6, fill=FUCHSIA)

# sub line
f_sub = font(BODY, 30)
draw.text((90, 548), "Sculpted nail artistry by Maylei  ·  @nailfiehi", font=f_sub, fill=(206, 191, 202))

img.save(OUT, "PNG")
print("wrote", OUT, img.size)
