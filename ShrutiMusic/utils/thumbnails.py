import os
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageFont
from py_yt import VideosSearch
from config import YOUTUBE_IMG_URL
from ShrutiMusic import app

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)


def trim(text, max_len=55):
    return text[:max_len] + "..." if len(text) > max_len else text


async def gen_thumb(videoid: str, player_username=None):
    if player_username is None:
        player_username = app.username

    path = f"{CACHE_DIR}/{videoid}_yt.png"
    if os.path.exists(path):
        return path

    try:
        results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
        data = (await results.next())["result"][0]

        title = data["title"]
        thumb_url = data["thumbnails"][0]["url"]
        duration = data.get("duration", "0:00")
        views = data["viewCount"]["short"]
        channel = data.get("channel", {}).get("name", "YouTube")
    except:
        title, thumb_url, duration, views, channel = "Unknown", YOUTUBE_IMG_URL, "0:00", "0", "YouTube"

    thumb_path = f"{CACHE_DIR}/{videoid}.png"

    async with aiohttp.ClientSession() as s:
        async with s.get(thumb_url) as r:
            async with aiofiles.open(thumb_path, "wb") as f:
                await f.write(await r.read())

    # 🎨 Background (same grey)
    bg = Image.new("RGB", (1280, 720), (55, 70, 75))
    draw = ImageDraw.Draw(bg)

    # 🖼 Thumbnail (center)
    thumb = Image.open(thumb_path).resize((700, 380)).convert("RGB")

    # rounded mask
    mask = Image.new("L", (700, 380), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 700, 380), 40, fill=255)
    thumb.putalpha(mask)

    bg.paste(thumb, (290, 120), thumb)

    # ⏱ Vertical progress bar (left)
    draw.rounded_rectangle((120, 120, 150, 500), 20, fill=(200, 200, 200))
    draw.rounded_rectangle((120, 300, 150, 500), 20, fill=(255, 255, 255))

    # time
    try:
        font_small = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 30)
        font_title = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 44)
        font_meta = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 32)
    except:
        font_small = font_title = font_meta = ImageFont.load_default()

    draw.text((95, 80), duration, fill="white", font=font_small)
    draw.text((95, 520), "00:00", fill="white", font=font_small)

    # 🎵 Title
    title = trim(title)
    draw.text((250, 540), title, fill="white", font=font_title)

    # 📊 Channel + views
    meta = f"{channel}  |  {views} views"
    draw.text((250, 600), meta, fill=(200, 200, 200), font=font_meta)

    # ⚡ Branding (small)
    draw.text((950, 670), "Powered by Mr Thakur", fill=(180, 180, 180), font=font_small)

    try:
        os.remove(thumb_path)
    except:
        pass

    bg.save(path)
    return path
