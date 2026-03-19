import os
from unidecode import unidecode
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import filters, enums
from pyrogram.types import *
from logging import getLogger

from ShrutiMusic import app
from ShrutiMusic.utils.database import db

LOGGER = getLogger(__name__)

# Welcome DB
try:
    wlcm = db.welcome
except:
    from ShrutiMusic.utils.database import welcome as wlcm


# Temp Storage
class temp:
    MELCOW = {}


# Circle SP
def circle(pfp, size=(450, 450)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", pfp.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + pfp.size, fill=255)
    pfp.putalpha(mask)
    return pfp


# Create Welcome Image
def welcomepic(pic, user, chat, id, uname):
    background = Image.open("ShrutiMusic/assets/welcome.png").convert("RGBA")

    try:
        pfp = Image.open(pic).convert("RGBA")
    except:
        pfp = Image.open("ShrutiMusic/assets/upic.png").convert("RGBA")

    pfp = circle(pfp)

    draw = ImageDraw.Draw(background)

    font = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 45)
    font2 = ImageFont.truetype("ShrutiMusic/assets/font.ttf", 90)

    # Safe username
    uname = f"@{uname}" if uname else "Not Set"

    draw.text((65, 250), f"NAME : {unidecode(user)}", fill="white", font=font)
    draw.text((65, 340), f"ID : {id}", fill="white", font=font)
    draw.text((65, 430), f"USERNAME : {uname}", fill="white", font=font)

    # DP Position
    background.paste(pfp, (767, 133), pfp)

    path = f"downloads/welcome_{id}.png"
    background.save(path)

    return path


# Command ON/OFF
@app.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /welcome on | off")

    chat_id = message.chat.id
    user = await app.get_chat_member(chat_id, message.from_user.id)

    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply("Only Admin Can Use This")

    state = message.command[1].lower()

    if state == "on":
        await wlcm.update_one({"chat_id": chat_id}, {"$set": {"disabled": False}}, upsert=True)
        await message.reply_text("✅ Welcome Enabled")

    elif state == "off":
        await wlcm.update_one({"chat_id": chat_id}, {"$set": {"disabled": True}}, upsert=True)
        await message.reply_text("❌ Welcome Disabled")


# Main Welcome Handler
@app.on_chat_member_updated(filters.group)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id

    data = await wlcm.find_one({"chat_id": chat_id})
    if data and data.get("disabled", False):
        return

    if member.new_chat_member and member.new_chat_member.status == "member":
        user = member.new_chat_member.user

        # Download DP
        try:
            pic = await app.download_media(user.photo.big_file_id, file_name=f"downloads/pp{user.id}.png")
        except:
            pic = "ShrutiMusic/assets/upic.png"

        # Remove old welcome
        if temp.MELCOW.get(chat_id):
            try:
                await temp.MELCOW[chat_id].delete()
            except:
                pass

        try:
            img = welcomepic(pic, user.first_name, member.chat.title, user.id, user.username)

            temp.MELCOW[chat_id] = await app.send_photo(
                chat_id,
                photo=img,
                caption=f"""✨ Welcome {user.mention} ❤️

📌 Group: {member.chat.title}
🆔 ID: {user.id}
👤 Username: @{user.username if user.username else "Not Set"}""",
            )

        except Exception as e:
            LOGGER.error(e)

        # Cleanup
        try:
            if os.path.exists(img):
                os.remove(img)
            if os.path.exists(f"downloads/pp{user.id}.png"):
                os.remove(f"downloads/pp{user.id}.png")
        except:
            pass
