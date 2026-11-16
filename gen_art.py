"""Generate entry.png: a vibrant robot sunburst poster."""
import math
import random

from PIL import Image, ImageDraw, ImageFilter

W = H = 1024
random.seed(7)

img = Image.new("RGB", (W, H))
pix = img.load()
top = (255, 0, 200)
bot = (255, 140, 20)
for y in range(H):
    t = y / (H - 1)
    r = int(top[0] + (bot[0] - top[0]) * t)
    g = int(top[1] + (bot[1] - top[1]) * t)
    b = int(top[2] + (bot[2] - top[2]) * t)
    for x in range(W):
        pix[x, y] = (r, g, b)

cx, cy = W // 2, int(H * 0.42)
ray_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(ray_layer)
for i in range(28):
    a0 = 2 * math.pi * i / 28
    a1 = a0 + math.pi / 28 * 0.9
    rad = 900
    pts = [(cx, cy), (cx + rad * math.cos(a0), cy + rad * math.sin(a0)),
           (cx + rad * math.cos(a1), cy + rad * math.sin(a1))]
    rd.polygon(pts, fill=(255, 255, 90, 70 if i % 2 == 0 else 40))
ray_layer = ray_layer.filter(ImageFilter.GaussianBlur(3))
img = Image.alpha_composite(img.convert("RGBA"), ray_layer)

glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for rad, alpha in ((360, 60), (280, 70), (200, 80)):
    gd.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=(255, 240, 120, alpha))
glow = glow.filter(ImageFilter.GaussianBlur(30))
img = Image.alpha_composite(img, glow)

# floating confetti
conf = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(conf)
colors = [(255, 255, 255), (80, 255, 255), (255, 255, 0), (120, 255, 160),
          (255, 80, 180), (140, 120, 255)]
for _ in range(260):
    x = random.uniform(0, W)
    y = random.uniform(0, H)
    s = random.uniform(6, 20)
    a = random.uniform(0, math.pi)
    c = random.choice(colors)
    dx, dy = math.cos(a) * s, math.sin(a) * s
    ex, ey = -math.sin(a) * s * 0.5, math.cos(a) * s * 0.5
    cd.polygon([(x + dx, y + dy), (x + ex, y + ey), (x - dx, y - dy), (x - ex, y - ey)],
               fill=c + (170,))
img = Image.alpha_composite(img, conf)

# robot mascot
robot = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rb = ImageDraw.Draw(robot)
body_c = (230, 235, 255, 255)
edge = (70, 90, 160, 255)
# antenna
rb.line((W // 2, cy - 310, W // 2, cy - 250), fill=edge, width=10)
rb.ellipse((W // 2 - 26, cy - 360, W // 2 + 26, cy - 308), fill=(255, 80, 60, 255))
# head
head = (cx - 210, cy - 260, cx + 210, cy + 130)
rb.rounded_rectangle(head, radius=80, fill=body_c, outline=edge, width=10)
# ears
rb.rounded_rectangle((head[0] - 34, cy - 120, head[0] + 4, cy - 20), radius=14, fill=(120, 160, 255, 255))
rb.rounded_rectangle((head[2] - 4, cy - 120, head[2] + 34, cy - 20), radius=14, fill=(120, 160, 255, 255))
# eyes
for ex in (cx - 95, cx + 95):
    rb.ellipse((ex - 62, cy - 150, ex + 62, cy - 10), fill=(0, 230, 255, 255))
    rb.ellipse((ex - 26, cy - 120, ex + 26, cy - 50), fill=(255, 255, 255, 255))
# cheeks
for ex in (cx - 165, cx + 165):
    rb.ellipse((ex - 26, cy + 10, ex + 26, cy + 46), fill=(255, 150, 190, 255))
# smile
rb.arc((cx - 90, cy - 30, cx + 90, cy + 95), start=15, end=165, fill=(50, 60, 110, 255), width=16)
# body
rb.rounded_rectangle((cx - 150, cy + 150, cx + 150, cy + 420), radius=60, fill=(120, 170, 255, 255), outline=edge, width=10)
# chest light
rb.ellipse((cx - 40, cy + 220, cx + 40, cy + 300), fill=(255, 220, 60, 255))
# arms
rb.rounded_rectangle((cx - 230, cy + 170, cx - 160, cy + 360), radius=30, fill=body_c, outline=edge, width=8)
rb.rounded_rectangle((cx + 160, cy + 170, cx + 230, cy + 360), radius=30, fill=body_c, outline=edge, width=8)

rob_glow = robot.filter(ImageFilter.GaussianBlur(18))
img = Image.alpha_composite(img, rob_glow)
img = Image.alpha_composite(img, robot)

img = img.convert("RGB")
img.save("entry.png", optimize=True)
print(img.size)
