import os
from random import randint
from typing import Union

from pyrogram.types import InlineKeyboardMarkup

import config
from ShrutiMusic import Carbon, YouTube, app
from ShrutiMusic.core.call import Nand
from ShrutiMusic.misc import db
from ShrutiMusic.utils.database import add_active_video_chat, is_active_chat
from ShrutiMusic.utils.exceptions import AssistantErr
from ShrutiMusic.utils.inline import aq_markup, close_markup, stream_markup
from ShrutiMusic.utils.pastebin import NandBin
from ShrutiMusic.utils.stream.queue import put_queue, put_queue_index
from ShrutiMusic.utils.thumbnails import gen_thumb

async def stream(
_,
mystic,
user_id,
result,
chat_id,
user_name,
original_chat_id,
video: Union[bool, str] = None,
streamtype: Union[bool, str] = None,
spotify: Union[bool, str] = None,
forceplay: Union[bool, str] = None,
):
if not result:
return

if forceplay:
    await Nand.force_stop_stream(chat_id)

if streamtype == "youtube":
    vidid = result["vidid"]
    title = result["title"].title()
    duration_min = result["duration_min"]
    thumbnail = result["thumb"]
    status = True if video else None

    try:
        file_path, direct = await YouTube.download(
            vidid, mystic, videoid=True, video=status
        )
    except:
        raise AssistantErr(_["play_14"])

    if await is_active_chat(chat_id):
        await put_queue(
            chat_id,
            original_chat_id,
            file_path if direct else f"vid_{vidid}",
            title,
            duration_min,
            user_name,
            vidid,
            user_id,
            "video" if video else "audio",
        )
    else:
        db[chat_id] = []

        await Nand.join_call(
            chat_id,
            original_chat_id,
            file_path,
            video=status,
            image=thumbnail,
        )

        await put_queue(
            chat_id,
            original_chat_id,
            file_path,
            title,
            duration_min,
            user_name,
            vidid,
            user_id,
            "video" if video else "audio",
        )

        img = await gen_thumb(vidid)
        button = stream_markup(_, chat_id)

        await app.send_photo(
            original_chat_id,
            photo=img,
            caption=_["stream_1"].format(
                f"https://t.me/{app.username}?start=info_{vidid}",
                title[:23],
                duration_min,
                user_name,
            ),
            reply_markup=InlineKeyboardMarkup(button),
            has_spoiler=True
        )      
