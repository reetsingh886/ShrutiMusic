import time

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from ShrutiMusic import app
from ShrutiMusic.misc import _boot_
from ShrutiMusic.utils.database import add_served_chat, add_served_user
from ShrutiMusic.utils.formatters import get_readable_time
from config import BANNED_USERS


# -------------------- PRIVATE START -------------------- #

@app.on_message(filters.command("start") & filters.private & ~BANNED_USERS)
async def start_pm(client, message: Message):

    await add_served_user(message.from_user.id)

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "ADD BOT TO GROUP",
                    url=f"https://t.me/{app.username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton("NETWORKS", callback_data="bot_stats"),
                InlineKeyboardButton("DEVELOPER", url="https://t.me/iamthakur007"),
            ],
            [
                InlineKeyboardButton("FUNCTIONS + COMMANDS", callback_data="help_back"),
            ],
        ]
    )

    caption = f"""
✧ HELLO {message.from_user.mention} ✨

❖ WELCOME TO {app.mention} ♪♪

➤ A SMART & ELEGANT MUSIC BOT BUILT FOR TELEGRAM VOICE CHATS.

✦ ENJOY : SMOOTH PLAYBACK • HD SOUND • NO LAG 🎧

✦ SOURCES : YOUTUBE • SPOTIFY • APPLE • SAAVN

➥ TAP HELP TO VIEW ALL COMMANDS & FEATURES.
"""

    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=caption,
        reply_markup=buttons
    )


# -------------------- GROUP START -------------------- #

@app.on_message(filters.command("start") & filters.group & ~BANNED_USERS)
async def start_gp(client, message: Message):

    uptime = int(time.time() - _boot_)

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "ADD BOT TO GROUP",
                    url=f"https://t.me/{app.username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton("NETWORKS", callback_data="bot_stats"),
                InlineKeyboardButton("DEVELOPER", url="https://t.me/iamthakur007"),
            ],
            [
                InlineKeyboardButton("FUNCTIONS + COMMANDS", callback_data="help_back"),
            ],
        ]
    )

    caption = f"""
HELLO 👋

I AM {app.mention}

⏱ UPTIME : {get_readable_time(uptime)}

USE /play TO PLAY MUSIC IN VC
"""

    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=caption,
        reply_markup=buttons
    )

    return await add_served_chat(message.chat.id)


# -------------------- WELCOME -------------------- #

@app.on_message(filters.new_chat_members)
async def welcome(client, message: Message):

    for member in message.new_chat_members:

        if member.id == app.id:

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "ADD BOT TO GROUP",
                            url=f"https://t.me/{app.username}?startgroup=true",
                        )
                    ],
                    [
                        InlineKeyboardButton("NETWORKS", callback_data="bot_stats"),
                        InlineKeyboardButton("DEVELOPER", url="https://t.me/iamthakur007"),
                    ],
                    [
                        InlineKeyboardButton("FUNCTIONS + COMMANDS", callback_data="help_back"),
                    ],
                ]
            )

            await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=f"THANKS FOR ADDING {app.mention} IN {message.chat.title}",
                reply_markup=buttons
            )

            await add_served_chat(message.chat.id)
