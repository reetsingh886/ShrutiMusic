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
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL
from ShrutiMusic import app

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)


async def gen_thumb(videoid: str, player_username=None):

    if player_username is None:
        player_username = app.username

    cache = f"{CACHE_DIR}/{videoid}.png"
    if os.path.exists(cache):
        return cache

    try:
        search = VideosSearch(videoid, limit=1)
        data = (await search.next())["result"][0]

        title = data["title"]
        duration = data["duration"]
        thumb = data["thumbnails"][0]["url"]

    except:
        title = "Unknown"
        duration = "Unknown"
        thumb = YOUTUBE_IMG_URL

    thumb_file = f"{CACHE_DIR}/thumb.png"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumb) as r:
                async with aiofiles.open(thumb_file, "wb") as f:
                    await f.write(await r.read())
    except:
        return YOUTUBE_IMG_URL

    bg = Image.open(thumb_file).resize((900, 500))
    bg = bg.filter(ImageFilter.GaussianBlur(20))

    overlay = Image.new("RGBA", (900, 500), (255, 255, 255, 120))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)

    thumb_img = Image.open(thumb_file).resize((250, 250))
    bg.paste(thumb_img, (60, 120))

    draw = ImageDraw.Draw(bg)

    try:
        font_big = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 40)
        font_small = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 28)
    except:
        font_big = font_small = ImageFont.load_default()

    draw.text((350, 150), title[:40], fill=(0,0,0), font=font_big)

    meta = f"Duration : {duration}\nPlayer : @{player_username}"

    draw.multiline_text(
        (350, 230),
        meta,
        fill=(0,0,0),
        font=font_small,
        spacing=10
    )

    bg.save(cache)

    try:
        os.remove(thumb_file)
    except:
        pass

    return cache
