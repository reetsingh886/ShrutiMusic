import random
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app
from ShrutiMusic.core.call import Nand
from ShrutiMusic.utils import bot_sys_stats
from ShrutiMusic.utils.decorators.language import language
from ShrutiMusic.utils.inline import supp_markup
from config import BANNED_USERS


# 🔥 Random Images (Shashank Style)
PING_PICS = [
    "https://files.catbox.moe/fh7vw7.jpg",
    "https://files.catbox.moe/lckxh6.jpg",
    "https://files.catbox.moe/smteo6.jpg",
    "https://files.catbox.moe/7enu2i.jpg",
    "https://files.catbox.moe/n6hkvd.jpg",
    "https://files.catbox.moe/ej1p7t.jpg"
]


@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()

    response = await message.reply_photo(
        photo=random.choice(PING_PICS),  # 🔥 random image
        caption=_["ping_1"].format(app.mention),
    )

    pytgping = await Nand.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000

    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
