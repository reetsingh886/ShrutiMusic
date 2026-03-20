import os
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from py_yt import VideosSearch
from config import YOUTUBE_IMG_URL
from ShrutiMusic import app

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)


async def gen_thumb(videoid: str, player_username=None):
    if player_username is None:
        player_username = app.username

    path = f"{CACHE_DIR}/{videoid}_clean.png"
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

    # 🎨 Background (simple dark)
    bg = Image.new("RGB", (1280, 720), (45, 60, 65))

    draw = ImageDraw.Draw(bg)

    # 🖼 Thumbnail (rounded)
    thumb = Image.open(thumb_path).resize((520, 300)).convert("RGB")

    mask = Image.new("L", (520, 300), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 520, 300), 30, fill=255)

    thumb.putalpha(mask)
    bg.paste(thumb, (380, 120), thumb)

    # Fonts
    try:
        title_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 42)
        meta_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 28)
    except:
        title_font = meta_font = ImageFont.load_default()

    # 🎵 Title
    draw.text((200, 460), title[:50], fill="white", font=title_font)

    # 📊 Meta
    draw.text((200, 520), f"{views} views", fill=(200, 200, 200), font=meta_font)

    # 🎚 Progress bar (left side vertical style)
    draw.rounded_rectangle((120, 120, 140, 520), 10, fill=(200, 200, 200, 100))
    draw.rounded_rectangle((120, 300, 140, 520), 10, fill=(255, 255, 255))

    # ⏱ Time
    draw.text((90, 90), duration, fill="white", font=meta_font)
    draw.text((90, 540), "00:00", fill="white", font=meta_font)

    try:
        os.remove(thumb_path)
    except:
        pass

    bg.save(path)
    return path
