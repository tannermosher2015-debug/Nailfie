"""
Generate images/og-cover.png — the social-share preview for Nailfie Studio.
Dusty-rose branded card (mauve + rose-gold, nail-tip-arch motif). Re-run after
dropping in a real hero photo if you'd rather feature her work.

    python build_og.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images", "og-cover.png")

W, H = 1200, 630
MAUVE = (94, 70, 80)
ROSE = (192, 138, 126)
LROSE = (230, 178, 168)
CREAM = (251, 241, 234)

def font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()

DISPLAY = ["C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/Arialbd.ttf", "arialbd.ttf"]
ITALIC  = ["C:/Windows/Fonts/georgiaz.ttf", "C:/Windows/Fonts/georgiab.ttf", "arialbd.ttf"]
BODY    = ["C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/segoeui.ttf", "arial.ttf"]
SEMI    = ["C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/seguisb.ttf", "arial.ttf"]

img = Image.new("RGB", (W, H), MAUVE)

# soft rose glow, top-right
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([W - 560, -280, W + 240, 520], fill=ROSE + (130,))
glow = glow.filter(ImageFilter.GaussianBlur(150))
img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))

# nail-tip arch motif (right side), partly off-canvas
ax, aw, atop, abot, dome = 1080, 300, 150, 690, 150
arch = Image.new("RGBA", (W, H), (0, 0, 0, 0))
adraw = ImageDraw.Draw(arch)
adraw.rectangle([ax - aw // 2, atop + dome, ax + aw // 2, abot], fill=ROSE + (235,))
adraw.pieslice([ax - aw // 2, atop, ax + aw // 2, atop + 2 * dome], 180, 360, fill=ROSE + (235,))
adraw.rounded_rectangle([ax - aw // 2 + 26, atop + 40, ax - aw // 2 + 60, abot - 30], radius=18, fill=(255, 255, 255, 70))
img.paste(Image.alpha_composite(img.convert("RGBA"), arch).convert("RGB"), (0, 0))
draw = ImageDraw.Draw(img)

# eyebrow
eb = font(SEMI, 27)
draw.text((90, 130), "W A I L U K U   ·   M A U I", font=eb, fill=LROSE)

# headline (serif)
f_disp = font(DISPLAY, 84)
f_ital = font(ITALIC, 84)
draw.text((86, 200), "Sculpted", font=f_disp, fill=CREAM)
draw.text((86, 296), "by hand.", font=f_disp, fill=CREAM)
y2 = 392
x = 86
draw.text((x, y2), "Worn like ", font=f_disp, fill=CREAM)
xw = draw.textlength("Worn like ", font=f_disp)
draw.text((x + xw, y2), "art.", font=f_ital, fill=LROSE)
# rose-gold brushstroke under "art."
uy = y2 + 92
draw.rounded_rectangle([x + xw, uy, x + xw + draw.textlength("art.", font=f_ital), uy + 11], radius=6, fill=ROSE)

# sub line
f_sub = font(BODY, 29)
draw.text((90, 548), "Sculpted nail artistry by Maylei  ·  @nailfiehi", font=f_sub, fill=(226, 210, 206))

img.save(OUT, "PNG")
print("wrote", OUT, img.size)
