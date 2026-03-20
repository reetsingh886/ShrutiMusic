import os
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageFont
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

    path = f"{CACHE_DIR}/{videoid}_red_clean.png"
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

    # 🎨 SOLID DARK BG (NO BLUR)
    bg = Image.new("RGB", (1280, 720), (15, 10, 10))
    draw = ImageDraw.Draw(bg)

    # 🖼 THUMB
    thumb = Image.open(thumb_path).resize((420, 420)).convert("RGBA")

    mask = Image.new("L", (420, 420), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 420, 420), 40, fill=255)
    thumb.putalpha(mask)

    # red border
    border = Image.new("RGBA", (460, 460), (0, 0, 0, 0))
    bd = ImageDraw.Draw(border)
    bd.rounded_rectangle((0, 0, 460, 460), 50, outline=(255, 60, 60), width=8)

    bg.paste(border, (100, 130), border)
    bg.paste(thumb, (120, 150), thumb)

    # fonts
    try:
        title_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 42)
        meta_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 30)
        small_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 26)
    except:
        title_font = meta_font = small_font = ImageFont.load_default()

    # 🔴 NOW PLAYING
    draw.rounded_rectangle((600, 140, 820, 190), 25, fill=(255, 60, 60))
    draw.text((630, 150), "NOW PLAYING", fill="white", font=small_font)

    # 🎵 TITLE (WHITE)
    title = trim(title, title_font, 550)
    draw.text((600, 230), title, fill="white", font=title_font)

    # underline
    draw.line((600, 290, 1000, 290), fill=(255, 60, 60), width=3)

    # 📊 META (WHITE + RED MIX)
    draw.text((600, 320), f"Duration: {duration}", fill="white", font=meta_font)
    draw.text((600, 360), f"Views: {views}", fill=(255, 80, 80), font=meta_font)
    draw.text((600, 400), f"Player: @{player_username}", fill=(255, 80, 80), font=meta_font)

    # 🎚 PROGRESS BAR
    bar_x, bar_y = 600, 470
    bar_w = 500

    draw.rounded_rectangle((bar_x, bar_y, bar_x+bar_w, bar_y+12), 6, fill=(255,255,255,80))
    draw.rounded_rectangle((bar_x, bar_y, bar_x+bar_w//2, bar_y+12), 6, fill=(255,60,60))

    draw.ellipse((bar_x+bar_w//2-8, bar_y-4, bar_x+bar_w//2+8, bar_y+16), fill="white")

    # time
    draw.text((600, 510), "00:00", fill="white", font=small_font)
    draw.text((1080, 510), duration, fill="white", font=small_font)

    # branding
    draw.text((900, 660), "Powered by Mr Thakur", fill=(180,180,180), font=small_font)

    try:
        os.remove(thumb_path)
    except:
        pass

    bg.save(path)
    return path
