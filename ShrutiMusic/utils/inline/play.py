import math
from pyrogram.types import InlineKeyboardButton
from ShrutiMusic.utils.formatters import time_to_seconds
from config import BOT_USERNAME


# ================= DIRECT PLAYER ================= #

def track_markup(*args):
    chat_id = args[1] if len(args) > 1 else 0

    return [
        [
            InlineKeyboardButton("▶", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton("⏸", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton("↻", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton("⏭", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton("▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton("≡ CLOSE ≡", callback_data=f"forceclose {chat_id}")
        ],
    ]


def stream_markup(*args):
    return track_markup(*args)


def playlist_markup(*args):
    return track_markup(*args)


def livestream_markup(*args):
    chat_id = args[1] if len(args) > 1 else 0

    return [
        [
            InlineKeyboardButton("🔴 LIVE", callback_data=f"ADMIN Live|{chat_id}")
        ],
        [
            InlineKeyboardButton("≡ CLOSE ≡", callback_data=f"forceclose {chat_id}")
        ],
    ]


# ================= SLIDER ================= #

def slider_markup(*args):
    chat_id = args[2] if len(args) > 2 else 0

    return [
        [
            InlineKeyboardButton("◁", callback_data=f"ADMIN Back|{chat_id}"),
            InlineKeyboardButton("✖ CLOSE", callback_data=f"forceclose {chat_id}"),
            InlineKeyboardButton("▷", callback_data=f"ADMIN Next|{chat_id}"),
        ],
    ]


# ================= TIMER ================= #

def stream_markup_timer(_, chat_id, played, dur):
    try:
        played_sec = time_to_seconds(played)
        duration_sec = time_to_seconds(dur)

        percentage = (played_sec / duration_sec) * 100 if duration_sec else 0
        umm = int(percentage)

        if 0 < umm <= 10:
            bar = "◉—————————"
        elif 10 < umm <= 20:
            bar = "—◉————————"
        elif 20 < umm <= 30:
            bar = "——◉———————"
        elif 30 < umm <= 40:
            bar = "———◉——————"
        elif 40 < umm <= 50:
            bar = "————◉—————"
        elif 50 < umm <= 60:
            bar = "—————◉————"
        elif 60 < umm <= 70:
            bar = "——————◉———"
        elif 70 < umm <= 80:
            bar = "———————◉——"
        elif 80 < umm <= 95:
            bar = "————————◉—"
        else:
            bar = "—————————◉"

    except:
        played = "0:00"
        dur = "0:00"
        bar = "◉—————————"

    return [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton("▶", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton("⏸", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton("↻", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton("⏭", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton("▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(
                text="≡ CLOSE ≡",
                callback_data=f"forceclose {chat_id}"
            )
        ],
        ]
