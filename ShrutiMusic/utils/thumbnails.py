# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
#
# All rights reserved.
#
# This code is the intellectual property of Nand Yaduwanshi.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: badboy809075@gmail.com
#
# ATLEAST GIVE CREDITS IF YOU STEALING :
# ELSE NO FURTHER PUBLIC THUMBNAIL UPDATES

import os
import re
import random
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL
from ShrutiMusic import app

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# 👉 यहाँ अपनी image लगाओ
CUSTOM_THUMB = "https://files.catbox.moe/jioaei.jpg"

DUAL_TONES = [
    ((20, 20, 20), (240, 240, 240)),
    ((25, 30, 45), (250, 250, 250)),
    ((15, 40, 65), (230, 230, 230)),
    ((55, 10, 80), (255, 245, 255))
]


def trim_to_width(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> str:
    ellipsis = "…"
    try:
        if font.getlength(text) <= max_w:
            return text
        for i in range(len(text) - 1, 0, -1):
            if font.getlength(text[:i] + ellipsis) <= max_w:
                return text[:i] + ellipsis
    except:
        return text[:max_w // 10] + "…" if len(text) > max_w // 10 else text
    return ellipsis


async def gen_thumb(videoid: str, player_username: str = None):

    # 👉 अगर custom image चाहिए तो सीधे वही return
    if CUSTOM_THUMB:
        return CUSTOM_THUMB

    if player_username is None:
        player_username = app.username

    cache_path = os.path.join(CACHE_DIR, f"{videoid}_hexagon.png")
    if os.path.exists(cache_path):
        return cache_path

    try:
        results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
        search = await results.next()
        data = search.get("result", [])[0]

        title = re.sub(r"\W+", " ", data.get("title", "Unknown Title")).title()
        thumbnail = data.get("thumbnails", [{}])[0].get("url", YOUTUBE_IMG_URL)
        duration = data.get("duration")
        views = data.get("viewCount", {}).get("short", "Unknown Views")

    except:
        title, thumbnail, duration, views = "Unknown", YOUTUBE_IMG_URL, None, "Unknown"

    thumb_path = os.path.join(CACHE_DIR, f"thumb_{videoid}.png")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as r:
                if r.status == 200:
                    async with aiofiles.open(thumb_path, "wb") as f:
                        await f.write(await r.read())
    except:
        return YOUTUBE_IMG_URL

    bg = Image.open(thumb_path).resize((1280, 720)).convert("RGB")
    bg = bg.filter(ImageFilter.GaussianBlur(30)).convert("RGBA")

    overlay = Image.new("RGBA", (1280, 720), (255, 255, 255, 40))
    bg = Image.alpha_composite(bg, overlay)

    draw = ImageDraw.Draw(bg)

    try:
        title_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 44)
    except:
        title_font = ImageFont.load_default()

    draw.text((700, 200), title, fill=(0, 0, 0), font=title_font)

    try:
        os.remove(thumb_path)
    except:
        pass

    bg.save(cache_path)
    return cache_path
        
