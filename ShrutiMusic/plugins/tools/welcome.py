import os
from unidecode import unidecode
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import filters, enums
from pyrogram.types import *
from logging import getLogger

from ShrutiMusic import app
from ShrutiMusic.utils.database import db

LOGGER = getLogger(__name__)

# DB
try:
    wlcm = db.welcome
except:
    from ShrutiMusic.utils.database import welcome as wlcm


class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None


# 🔵 Circle DP (same logic)
def circle(pfp, size=(450, 450)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


# 💖 Pink Welcome Image (ONLY CHANGE)
def welcomepic(pic, user, chat, id, uname):
    background = Image.open("ShrutiMusic/assets/welcome.png").convert("RGBA")

    try:
        pfp = Image.open(pic).convert("RGBA")
    except:
        pfp = Image.open("ShrutiMusic/assets/upic.png").convert("RGBA")

    pfp = circle(pfp)
    pfp = pfp.resize((380, 380))

    draw = ImageDraw.Draw(background)

    font_big = ImageFont.truetype('ShrutiMusic/assets/font.ttf', size=80)
    font_small = ImageFont.truetype('ShrutiMusic/assets/font.ttf', size=45)

    uname = f"@{uname}" if uname else "Not Set"

    # 💕 Pink Text
    draw.text((120, 220), "WELCOME", fill="#ff6fa5", font=font_big)
    draw.text((120, 330), f"Name: {unidecode(user)}", fill="#ff6fa5", font=font_small)
    draw.text((120, 400), f"ID: {id}", fill="#ff6fa5", font=font_small)
    draw.text((120, 470), f"Username: {uname}", fill="#ff6fa5", font=font_small)

    # 🔵 DP position
    background.paste(pfp, (880, 170), pfp)

    path = f"downloads/welcome#{id}.png"
    background.save(path)

    return path


# 🔧 Command (same logic)
@app.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(_, message: Message):
    usage = "❖ ᴜsᴀɢᴇ ➥ /welcome [on|off]"

    if len(message.command) == 1:
        return await message.reply_text(usage)

    chat_id = message.chat.id
    user = await app.get_chat_member(chat_id, message.from_user.id)

    if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        A = await wlcm.find_one({"chat_id": chat_id})
        state = message.text.split(None, 1)[1].strip().lower()

        if state == "on":
            if A and not A.get("disabled", False):
                return await message.reply_text("✦ Special Welcome Already Enabled")

            await wlcm.update_one({"chat_id": chat_id}, {"$set": {"disabled": False}}, upsert=True)
            await message.reply_text(f"✦ Enabled Special Welcome in {message.chat.title}")

        elif state == "off":
            if A and A.get("disabled", False):
                return await message.reply_text("✦ Special Welcome Already Disabled")

            await wlcm.update_one({"chat_id": chat_id}, {"$set": {"disabled": True}}, upsert=True)
            await message.reply_text(f"✦ Disabled Special Welcome in {message.chat.title}")

        else:
            await message.reply_text(usage)

    else:
        await message.reply("✦ Only Admins Can Use This Command")


# 🔥 Welcome Handler (same logic)
@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    A = await wlcm.find_one({"chat_id": chat_id})

    if A and A.get("disabled", False):
        return

    if (
        not member.new_chat_member
        or member.new_chat_member.status in {"banned", "left", "restricted"}
        or member.old_chat_member
    ):
        return

    user = member.new_chat_member.user if member.new_chat_member else member.from_user

    try:
        pic = await app.download_media(
            user.photo.big_file_id,
            file_name=f"downloads/pp{user.id}.png"
        )
    except AttributeError:
        pic = "ShrutiMusic/assets/upic.png"

    if temp.MELCOW.get(f"welcome-{member.chat.id}") is not None:
        try:
            await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
        except Exception as e:
            LOGGER.error(e)

    try:
        welcomeimg = welcomepic(
            pic, user.first_name, member.chat.title, user.id, user.username
        )

        temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption=f"""🌟 <b>ᴡᴇʟᴄᴏᴍᴇ {user.mention}!</b>

📋 ɢʀᴏᴜᴘ: {member.chat.title}
🆔 ʏᴏᴜʀ ɪᴅ: {user.id}
👤 ᴜsᴇʀɴᴀᴍᴇ: @{user.username if user.username else "ɴᴏᴛ sᴇᴛ"}

ʜᴏᴘᴇ ʏᴏᴜ ғɪɴᴅ ɢᴏᴏᴅ ᴠɪʙᴇs, ɴᴇᴡ ғʀɪᴇɴᴅs, ᴀɴᴅ ʟᴏᴛs ᴏғ ғᴜɴ ʜᴇʀᴇ! 🌟""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🎵 ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🎵",
                            url=f"https://t.me/{app.username}?startgroup=True"
                        )
                    ]
                ]
            ),
        )

    except Exception as e:
        LOGGER.error(e)

    try:
        os.remove(f"downloads/welcome#{user.id}.png")
        os.remove(f"downloads/pp{user.id}.png")
    except Exception:
        pass
