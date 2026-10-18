#!/usr/bin/env python3
"""One-off: draws the original CourseGauge social share image (og-image.png, 1200x630).
Original artwork by Joshua Israel Ventures LLC (DejaVu fonts, free licence). Needs Pillow."""
from PIL import Image, ImageDraw, ImageFont
W, H = 1200, 630
im = Image.new("RGB", (W, H), "#1b4d3e"); d = ImageDraw.Draw(im)
F = "/usr/share/fonts/truetype/dejavu/"
big = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 96); mid = ImageFont.truetype(F + "DejaVuSans.ttf", 40); small = ImageFont.truetype(F + "DejaVuSans.ttf", 30)
# gauge logo (same geometry as logo.svg, scaled x7.5)
cx, cy, s = 220, 300, 7.5
d.ellipse([cx - 15*s, cy - 15*s, cx + 15*s, cy + 15*s], fill="#24604e")
d.arc([cx - 10*s, cy - 6*s, cx + 10*s, cy + 14*s], 180, 360, fill="#f2c14e", width=int(3*s))
d.line([cx, cy + 4*s, cx + 6*s, cy - 4*s], fill="#ffffff", width=int(2.5*s))
d.ellipse([cx - 2.5*s, cy + 1.5*s, cx + 2.5*s, cy + 6.5*s], fill="#ffffff")
d.text((380, 190), "CourseGauge", font=big, fill="#ffffff")
d.text((384, 315), "Sourced reviews, comparisons and", font=mid, fill="#f2c14e")
d.text((384, 365), "price tools for online course platforms", font=mid, fill="#f2c14e")
d.text((384, 470), "coursegauge.com", font=small, fill="#d9e6e1")
im.save("og-image.png", optimize=True)
print("ok")
