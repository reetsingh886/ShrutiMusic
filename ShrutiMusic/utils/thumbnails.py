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


def trim_to_width(text: str, font, max_w: int) -> str:
    ellipsis = "…"
    try:
        if font.getlength(text) <= max_w:
            return text
        for i in range(len(text)-1, 0, -1):
            if font.getlength(text[:i] + ellipsis) <= max_w:
                return text[:i] + ellipsis
    except:
        return text[:max_w//10] + "…"
    return ellipsis


async def gen_thumb(videoid: str, player_username: str = None) -> str:
    if player_username is None:
        player_username = app.username

    cache_path = os.path.join(CACHE_DIR, f"{videoid}_red.png")
    if os.path.exists(cache_path):
        return cache_path

    try:
        results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
        search = await results.next()
        data = search.get("result", [])[0]
        title = re.sub(r"\W+", " ", data.get("title", "Unknown")).title()
        thumbnail = data.get("thumbnails", [{}])[0].get("url", YOUTUBE_IMG_URL)
        duration = data.get("duration")
        views = data.get("viewCount", {}).get("short", "Unknown")
    except:
        title, thumbnail, duration, views = "Unknown", YOUTUBE_IMG_URL, None, "Unknown"

    duration_text = duration if duration else "Live"

    thumb_path = os.path.join(CACHE_DIR, f"thumb_{videoid}.png")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as r:
                if r.status == 200:
                    async with aiofiles.open(thumb_path, "wb") as f:
                        await f.write(await r.read())
    except:
        return YOUTUBE_IMG_URL

    # 🔥 Background
    bg = Image.open(thumb_path).resize((1280, 720)).convert("RGBA")
    bg = bg.filter(ImageFilter.GaussianBlur(25))

    # Dark + Red overlay
    overlay = Image.new("RGBA", (1280, 720), (0, 0, 0, 160))
    red_overlay = Image.new("RGBA", (1280, 720), (255, 0, 0, 60))
    bg = Image.alpha_composite(bg, overlay)
    bg = Image.alpha_composite(bg, red_overlay)

    # 🎯 Thumbnail image (square instead of hexagon)
    thumb = Image.open(thumb_path).resize((420, 420)).convert("RGBA")

    mask = Image.new("L", (420, 420), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, 420, 420), 40, fill=255)

    thumb.putalpha(mask)

    # 🔴 Red glow border
    border = Image.new("RGBA", (440, 440), (0, 0, 0, 0))
    d = ImageDraw.Draw(border)
    d.rounded_rectangle((0, 0, 440, 440), 50, outline=(255, 0, 0, 255), width=6)

    bg.paste(border, (80, 140), border)
    bg.paste(thumb, (90, 150), thumb)

    draw = ImageDraw.Draw(bg)

    # Fonts
    try:
        title_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 46)
        meta_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 28)
        tag_font = ImageFont.truetype("ShrutiMusic/assets/font2.ttf", 26)
    except:
        title_font = meta_font = tag_font = ImageFont.load_default()

    # 🔴 NOW PLAYING Tag
    tag_x, tag_y = 600, 120
    draw.rounded_rectangle((tag_x, tag_y, tag_x+220, tag_y+50), 25, fill=(255, 0, 0))
    draw.text((tag_x+25, tag_y+10), "NOW PLAYING", fill="white", font=tag_font)

    # 🎵 Title
    title_text = trim_to_width(title, title_font, 550)
    draw.text((600, 200), title_text, fill="white", font=title_font)

    # underline
    draw.line((600, 260, 1000, 260), fill=(255, 0, 0), width=3)

    # 📊 Meta
    draw.text((600, 290), f"Duration: ", fill="white", font=meta_font)
    draw.text((760, 290), duration_text, fill="red", font=meta_font)

    draw.text((600, 330), f"Views: ", fill="white", font=meta_font)
    draw.text((720, 330), views, fill="red", font=meta_font)

    draw.text((600, 370), f"Player: ", fill="white", font=meta_font)
    draw.text((720, 370), f"@{player_username}", fill="red", font=meta_font)

    # 🔥 Progress Bar
    bar_x, bar_y = 600, 450
    bar_w = 500

    draw.rounded_rectangle((bar_x, bar_y, bar_x+bar_w, bar_y+12), 6, fill=(200, 200, 200))
    draw.rounded_rectangle((bar_x, bar_y, bar_x+bar_w//2, bar_y+12), 6, fill=(255, 0, 0))

    # Circle indicator
    draw.ellipse((bar_x+bar_w//2-6, bar_y-4, bar_x+bar_w//2+6, bar_y+16), fill="white")

    # ⚡ Branding
    brand = "Powered by Mr Thakur"
    w = tag_font.getlength(brand)
    draw.text((1280 - w - 40, 680), brand, fill="white", font=tag_font)

    try:
        os.remove(thumb_path)
    except:
        pass

    bg.save(cache_path)
    return cache_path
