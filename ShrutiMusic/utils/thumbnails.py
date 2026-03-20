import os
import re
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


async def gen_thumb(videoid: str, player_username: str = None):
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
    bg = Image.new("RGBA", (1280, 720), (10, 10, 15, 255))

    # ✨ Glow effect
    glow = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse((300, 100, 1100, 700), fill=(0, 150, 255, 80))
    glow = glow.filter(ImageFilter.GaussianBlur(200))
    bg = Image.alpha_composite(bg, glow)

    # 🎵 Thumbnail
    thumb = Image.open(thumb_path).resize((420, 420)).convert("RGBA")

    mask = Image.new("L", (420, 420), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, 420, 420), 40, fill=255)
    thumb.putalpha(mask)

    # Glow border
    border = Image.new("RGBA", (440, 440), (0, 0, 0, 0))
    d = ImageDraw.Draw(border)
    d.rounded_rectangle((0, 0, 440, 440), 50, outline=(100, 200, 255, 255), width=4)

    bg.paste(border, (80, 140), border)
    bg.paste(thumb, (90, 150), thumb)

    draw = ImageDraw.Draw(bg)

    # Fonts
    try:
        title_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 44)
        meta_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 28)
        small_font = ImageFont.truetype("ShrutiMusic/assets/font2.ttf", 24)
    except:
        title_font = meta_font = small_font = ImageFont.load_default()

    # 🎧 NOW PLAYING
    draw.rounded_rectangle((600, 110, 820, 160), 25, fill=(40, 40, 50, 200))
    draw.text((630, 120), "NOW PLAYING", fill=(200, 200, 200), font=small_font)

    # 🎵 Title
    title = trim(title, title_font, 500)
    draw.text((600, 200), title, fill="white", font=title_font)

    # underline glow
    draw.line((600, 260, 1000, 260), fill=(100, 200, 255), width=2)

    # 📊 Meta
    draw.text((600, 290), f"Duration: {duration}", fill=(180, 180, 180), font=meta_font)
    draw.text((600, 330), f"Views: {views}", fill=(180, 180, 180), font=meta_font)
    draw.text((600, 370), f"Player: @{player_username}", fill=(100, 200, 255), font=meta_font)

    # 🎚 Progress bar
    bar_x, bar_y = 600, 460
    bar_w = 500

    draw.rounded_rectangle((bar_x, bar_y, bar_x+bar_w, bar_y+10), 6, fill=(255,255,255,60))
    draw.rounded_rectangle((bar_x, bar_y, bar_x+bar_w//2, bar_y+10), 6, fill=(100,200,255))

    # circle indicator
    draw.ellipse((bar_x+bar_w//2-7, bar_y-5, bar_x+bar_w//2+7, bar_y+15), fill=(200, 255, 255))

    # ⏱ time
    draw.text((600, 500), "00:00", fill=(180,180,180), font=small_font)
    draw.text((1080, 500), duration, fill=(180,180,180), font=small_font)

    # ⚡ branding
    draw.text((900, 650), "Powered by Mr Thakur", fill=(120,120,120), font=small_font)

    try:
        os.remove(thumb_path)
    except:
        pass

    bg.save(path)
    return path
