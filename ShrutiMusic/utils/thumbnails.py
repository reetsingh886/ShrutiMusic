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
    return text + "..." if len(text) > 3 else text


async def gen_thumb(videoid: str, player_username=None):
    if player_username is None:
        player_username = app.username

    path = f"{CACHE_DIR}/{videoid}_final.png"
    if os.path.exists(path):
        return path

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

    async with aiohttp.ClientSession() as s:
        async with s.get(thumb_url) as r:
            async with aiofiles.open(thumb_path, "wb") as f:
                await f.write(await r.read())

    # ⚫ Background
    bg = Image.new("RGBA", (1280, 720), (10, 10, 20, 255))

    # 💙 Glow background
    glow = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse((300, 100, 1100, 700), fill=(100, 200, 255, 80))
    glow = glow.filter(ImageFilter.GaussianBlur(200))
    bg = Image.alpha_composite(bg, glow)

    draw = ImageDraw.Draw(bg)

    # ✨ particles
    for _ in range(80):
        x = random.randint(0, 1280)
        y = random.randint(0, 720)
        r = random.randint(2, 5)
        draw.ellipse((x, y, x+r, y+r), fill=(200, 220, 255, 60))

    # 🎵 Thumbnail
    thumb = Image.open(thumb_path).resize((420, 420)).convert("RGBA")

    mask = Image.new("L", (420, 420), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, 420, 420), 40, fill=255)
    thumb.putalpha(mask)

    # border
    border = Image.new("RGBA", (440, 440), (0, 0, 0, 0))
    bd = ImageDraw.Draw(border)
    bd.rounded_rectangle((0, 0, 440, 440), 50, outline=(120, 200, 255, 255), width=4)

    bg.paste(border, (80, 140), border)
    bg.paste(thumb, (90, 150), thumb)

    # 🧊 Glass Card
    card = Image.new("RGBA", (700, 350), (255, 255, 255, 25))
    card = card.filter(ImageFilter.GaussianBlur(15))
    bg.paste(card, (560, 140), card)

    draw = ImageDraw.Draw(bg)

    # Fonts
    try:
        title_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 44)
        meta_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 28)
        small_font = ImageFont.truetype("ShrutiMusic/assets/font2.ttf", 24)
    except:
        title_font = meta_font = small_font = ImageFont.load_default()

    # NOW PLAYING
    draw.rounded_rectangle((600, 110, 820, 160), 25, fill=(50, 50, 60, 200))
    draw.text((630, 120), "NOW PLAYING", fill=(220, 220, 220), font=small_font)

    # Title
    title = trim(title, title_font, 500)
    draw.text((600, 200), title, fill="white", font=title_font)
    draw.line((600, 260, 1000, 260), fill=(120, 200, 255), width=2)

    # Meta
    draw.text((600, 290), f"Duration: {duration}", fill=(200, 200, 200), font=meta_font)
    draw.text((600, 330), f"Views: {views}", fill=(200, 200, 200), font=meta_font)
    draw.text((600, 370), f"Player: @{player_username}", fill=(120, 200, 255), font=meta_font)

    # 🎚 Progress Bar
    bar_x, bar_y = 600, 460
    bar_w = 500
    progress = bar_w // 2

    draw.rounded_rectangle((bar_x, bar_y, bar_x+bar_w, bar_y+10), 6, fill=(255,255,255,60))
    draw.rounded_rectangle((bar_x, bar_y, bar_x+progress, bar_y+10), 6, fill=(120,200,255))

    # 💖 Heart
    hx = bar_x + progress
    hy = bar_y + 5

    heart = [
        (hx, hy+6),
        (hx-6, hy),
        (hx-12, hy+6),
        (hx, hy+16),
        (hx+12, hy+6),
        (hx+6, hy)
    ]
    draw.polygon(heart, fill=(180, 240, 255))

    # glow
    glow = Image.new("RGBA", (40, 40), (0,0,0,0))
    g = ImageDraw.Draw(glow)
    g.ellipse((0,0,40,40), fill=(120,200,255,120))
    glow = glow.filter(ImageFilter.GaussianBlur(15))
    bg.paste(glow, (hx-20, hy-10), glow)

    # time
    draw.text((600, 500), "00:00", fill=(200,200,200), font=small_font)
    draw.text((1080, 500), duration, fill=(200,200,200), font=small_font)

    # branding
    draw.text((900, 650), "Powered by Mr Thakur", fill=(120,120,120), font=small_font)

    try:
        os.remove(thumb_path)
    except:
        pass

    bg.save(path)
    return path
