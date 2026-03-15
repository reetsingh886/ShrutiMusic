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


def cut_text(text, font, max_w):
    while font.getlength(text) > max_w:
        text = text[:-1]
    return text + "..."


async def gen_thumb(videoid: str, player_username=None):

    if player_username is None:
        player_username = app.username

    cache = f"{CACHE_DIR}/{videoid}.png"
    if os.path.exists(cache):
        return cache

    try:
        search = VideosSearch(videoid, limit=1)
        data = (await search.next())["result"][0]

        title = data.get("title")
        duration = data.get("duration")
        views = data.get("viewCount")["short"]
        thumb = data.get("thumbnails")[0]["url"]

    except:
        title = "Unknown"
        duration = "Unknown"
        views = "Unknown"
        thumb = YOUTUBE_IMG_URL

    thumb_file = f"{CACHE_DIR}/thumb.png"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumb) as r:
                async with aiofiles.open(thumb_file, "wb") as f:
                    await f.write(await r.read())
    except:
        thumb_file = YOUTUBE_IMG_URL

    bg = Image.open(thumb_file).resize((1280, 720))
    bg = bg.filter(ImageFilter.GaussianBlur(40))

    overlay = Image.new("RGBA", (1280, 720), (255, 255, 255, 120))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)

    thumb_img = Image.open(thumb_file).resize((380, 380))

    cube = thumb_img.transform(
        (380, 380),
        Image.PERSPECTIVE,
        (1, 0.3, 0, 0.2, 1, 0, 0.001, 0.001),
        Image.BICUBIC,
    )

    bg.paste(cube, (130, 170))

    draw = ImageDraw.Draw(bg)

    try:
        title_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 50)
        meta_font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 32)
    except:
        title_font = meta_font = ImageFont.load_default()

    title = re.sub(r"\W+", " ", title)
    title = cut_text(title, title_font, 600)

    draw.text((580, 220), title, fill=(0, 0, 0), font=title_font)

    meta = (
        f"YouTube | {views}\n"
        f"Duration | {duration}\n"
        f"Player | @{player_username}"
    )

    draw.multiline_text(
        (580, 320),
        meta,
        fill=(0, 0, 0),
        font=meta_font,
        spacing=15
    )

    draw.rounded_rectangle(
        (580, 470, 980, 490),
        radius=8,
        fill=(220, 220, 220)
    )

    draw.rounded_rectangle(
        (580, 470, 780, 490),
        radius=8,
        fill=(0, 0, 0)
    )

    bg.save(cache)

    try:
        os.remove(thumb_file)
    except:
        pass

    return cache        
