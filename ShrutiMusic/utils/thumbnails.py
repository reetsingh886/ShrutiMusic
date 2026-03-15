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
import aiohttp
import aiofiles
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL
from ShrutiMusic import app

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)


def truncate(text, font, max_width):
    while font.getlength(text) > max_width:
        text = text[:-1]
    return text + "..."


async def gen_thumb(videoid: str, player_username=None):

    if player_username is None:
        player_username = app.username

    cache = f"{CACHE_DIR}/{videoid}.png"
    if os.path.exists(cache):
        return cache

    try:
        results = VideosSearch(videoid, limit=1)
        data = (await results.next())["result"][0]

        title = data["title"]
        duration = data["duration"]
        views = data["viewCount"]["short"]
        thumb = data["thumbnails"][0]["url"]

    except:
        title = "Unknown"
        duration = "Unknown"
        views = "Unknown"
        thumb = YOUTUBE_IMG_URL

    thumb_path = f"{CACHE_DIR}/thumb_{videoid}.png"

    async with aiohttp.ClientSession() as session:
        async with session.get(thumb) as r:
            async with aiofiles.open(thumb_path, "wb") as f:
                await f.write(await r.read())

    bg = Image.open(thumb_path).resize((1280, 720)).convert("RGB")
    bg = bg.filter(ImageFilter.GaussianBlur(35))

    overlay = Image.new("RGBA", (1280, 720), (255, 255, 255, 120))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)

    thumb_img = Image.open(thumb_path).resize((360, 360))

    cube = thumb_img.transform(
        (360, 360),
        Image.PERSPECTIVE,
        (1, 0.2, 0, 0.2, 1, 0, 0.001, 0.001),
        Image.BICUBIC,
    )

    bg.paste(cube, (120, 180))

    draw = ImageDraw.Draw(bg)

    try:
        title_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 45)
        meta_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 30)
    except:
        title_font = meta_font = ImageFont.load_default()

    title = re.sub(r"\W+", " ", title)
    title = truncate(title, title_font, 600)

    draw.text((560, 220), title, fill="black", font=title_font)

    meta = (
        f"YouTube | {views}\n"
        f"Duration | {duration}\n"
        f"Player | @{player_username}"
    )

    draw.multiline_text(
        (560, 320),
        meta,
        fill="black",
        font=meta_font,
        spacing=15
    )

    draw.rounded_rectangle(
        (560, 450, 950, 470),
        radius=10,
        fill=(200, 200, 200)
    )

    draw.rounded_rectangle(
        (560, 450, 750, 470),
        radius=10,
        fill=(0, 0, 0)
    )

    bg.save(cache)

    try:
        os.remove(thumb_path)
    except:
        pass

    return cache
