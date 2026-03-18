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

if streamtype == "playlist":
    msg = f"{_['play_19']}\n\n"
    count = 0

    for search in result:
        if int(count) == config.PLAYLIST_FETCH_LIMIT:
            continue
        try:
            title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(
                search, False if spotify else True
            )
        except:
            continue

        if str(duration_min) == "None":
            continue
        if duration_sec > config.DURATION_LIMIT:
            continue

        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            count += 1
            msg += f"{count}. {title[:70]}\n"
            msg += f"{_['play_20']} {position}\n\n"
        else:
            if not forceplay:
                db[chat_id] = []

            status = True if video else None

            try:
                file_path, direct = await YouTube.download(
                    vidid, mystic, video=status, videoid=True
                )
            except:
                raise AssistantErr(_["play_14"])

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
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )

            img = await gen_thumb(vidid)
            button = stream_markup(_, chat_id)

            run = await app.send_photo(
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

            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"

    if count == 0:
        return
    else:
        link = await NandBin(msg)
        lines = msg.count("\n")
        car = os.linesep.join(msg.split(os.linesep)[:17]) if lines >= 17 else msg

        carbon = await Carbon.generate(car, randint(100, 10000000))
        upl = close_markup(_)

        return await app.send_photo(
            original_chat_id,
            photo=carbon,
            caption=_["play_21"].format(position, link),
            reply_markup=upl,
            has_spoiler=True
        )
