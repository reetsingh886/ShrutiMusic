import os
import re
import random
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from py_yt import VideosSearch
from config import YOUTUBE_IMG_URL
from ShrutiMusic import app

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)


def trim(text, font, max_w):
    while font.getlength(text) > max_w:
        text = text[:-1]
    return text + "..."


async def gen_thumb(videoid: str, player_username=None):
    if player_username is None:
        player_username = app.username

    path = f"{CACHE_DIR}/{videoid}_final.png"
    if os.path.exists(path):
        return path

    # 🔍 Fetch data
    try:
        results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
        data = (await results.next())["result"][0]

        title = data["title"]
        thumb_url = data["thumbnails"][0]["url"]
        duration = data.get("duration", "Live")
        views = data["viewCount"]["short"]
    except:
        title, thumb_url, duration, views = "Unknown", YOUTUBE_IMG_URL, "Live", "0"

    thumb_path = f"{CACHE_DIR}/{videoid}.png"

    # ⬇ Download thumbnail
    async with aiohttp.ClientSession() as s:
        async with s.get(thumb_url) as r:
            async with aiofiles.open(thumb_path, "wb") as f:
                await f.write(await r.read())

    # 🎨 Background
    bg = Image.new("RGBA", (1280, 720), (10, 15, 25))

    # center glow
    glow = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((250, 100, 1150, 700), fill=(120, 200, 255, 80))
    glow = glow.filter(ImageFilter.GaussianBlur(180))
    bg = Image.alpha_composite(bg, glow)

    draw = ImageDraw.Draw(bg)

    # ✨ Smooth particles (FIXED)
    for _ in range(40):
        x = random.randint(0, 1280)
        y = random.randint(0, 720)
        size = random.randint(4, 8)

        dot = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(dot)
        d.ellipse((0, 0, size, size), fill=(200, 220, 255, 120))

        dot = dot.filter(ImageFilter.GaussianBlur(2))
        bg.paste(dot, (x, y), dot)

    # 🖼 Thumbnail
    thumb = Image.open(thumb_path).convert("RGBA")
    thumb = thumb.resize((420, 420), Image.LANCZOS)

    mask = Image.new("L", (420, 420), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 420, 420), 40, fill=255)
    thumb.putalpha(mask)

    border = Image.new("RGBA", (440, 440), (0, 0, 0, 0))
    bd = ImageDraw.Draw(border)
    bd.rounded_rectangle((0, 0, 440, 440), 50, outline=(120, 200, 255), width=4)

    bg.paste(border, (80, 140), border)
    bg.paste(thumb, (90, 150), thumb)

    # 🧊 REAL GLASS EFFECT (FIXED)
    card = bg.crop((560, 140, 1260, 490)).copy()
    card = card.filter(ImageFilter.GaussianBlur(30))

    overlay = Image.new("RGBA", card.size, (255, 255, 255, 25))
    card = Image.alpha_composite(card, overlay)

    bg.paste(card, (560, 140))

    draw = ImageDraw.Draw(bg)

    # 🔤 Fonts
    try:
        title_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 44)
        meta_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 28)
        small_font = ImageFont.truetype("ShrutiMusic/assets/font2.ttf", 24)
    except:
        title_font = meta_font = small_font = ImageFont.load_default()

    # 🎧 NOW PLAYING
    draw.rounded_rectangle((600, 110, 820, 160), 25, fill=(50, 50, 60, 200))
    draw.text((630, 120), "NOW PLAYING", fill=(230, 230, 230), font=small_font)

    # 🎵 Title
    title = trim(title, title_font, 500)
    draw.text((600, 200), title, fill="white", font=title_font)
    draw.line((600, 260, 1000, 260), fill=(120, 200, 255), width=2)

    # 📊 Meta
    draw.text((600, 290), f"Duration: {duration}", fill=(200, 200, 200), font=meta_font)
    draw.text((600, 330), f"Views: {views}", fill=(200, 200, 200), font=meta_font)
    draw.text((600, 370), f"Player: @{player_username}", fill=(120, 200, 255), font=meta_font)

    # 🎚 Progress bar
    bar_x, bar_y = 600, 460
    bar_w = 500
    progress = bar_w // 2

    draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + 10), 6, fill=(255, 255, 255, 60))
    draw.rounded_rectangle((bar_x, bar_y, bar_x + progress, bar_y + 10), 6, fill=(120, 200, 255))

    hx = bar_x + progress
    hy = bar_y + 5

    # 💖 HEART (FIXED)
    draw.ellipse((hx - 12, hy - 10, hx, hy), fill=(120, 200, 255))
    draw.ellipse((hx, hy - 10, hx + 12, hy), fill=(120, 200, 255))
    draw.polygon([(hx - 12, hy), (hx + 12, hy), (hx, hy + 20)], fill=(120, 200, 255))

    # glow
    glow = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((0, 0, 80, 80), fill=(120, 200, 255, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(20))
    bg.paste(glow, (hx - 40, hy - 30), glow)

    # ⏱ Time
    draw.text((600, 500), "00:00", fill=(200, 200, 200), font=small_font)
    draw.text((1080, 500), duration, fill=(200, 200, 200), font=small_font)

    # ⚡ Branding
    draw.text((900, 650), "Powered by Mr Thakur", fill=(130, 130, 130), font=small_font)

    try:
        os.remove(thumb_path)
    except:
        pass

    bg.save(path)
    return path
