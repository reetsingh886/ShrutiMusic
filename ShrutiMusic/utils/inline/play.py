import math
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ShrutiMusic.utils.formatters import time_to_seconds
from config import BOT_USERNAME


def build(buttons):
    return InlineKeyboardMarkup(buttons)


def track_markup(*args):
    try:
        _, videoid, user_id, channel, fplay = args[:5]
    except:
        return None

    buttons = [
        [
            InlineKeyboardButton("▶ Audio", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton("🎥 Video", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}"),
        ],
        [
            InlineKeyboardButton("✖ Close", callback_data=f"forceclose {videoid}|{user_id}")
        ],
    ]
    return build(buttons)


def stream_markup(*args):
    return track_markup(*args)


def playlist_markup(*args):
    return track_markup(*args)


def livestream_markup(*args):
    try:
        _, videoid, user_id, mode, channel, fplay = args[:6]
    except:
        return None

    buttons = [
        [
            InlineKeyboardButton("🔴 Live Stream", callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton("✖ Close", callback_data=f"forceclose {videoid}|{user_id}")
        ],
    ]
    return build(buttons)


def slider_markup(*args):
    try:
        _, videoid, user_id, query, query_type, channel, fplay = args[:7]
    except:
        return None

    query = str(query)[:20]

    buttons = [
        [
            InlineKeyboardButton("▶ Audio", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton("🎥 Video", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}"),
        ],
        [
            InlineKeyboardButton("◁", callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
            InlineKeyboardButton("✖ Close", callback_data=f"forceclose {query}|{user_id}"),
            InlineKeyboardButton("▷", callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
        ],
    ]
    return build(buttons)


def stream_markup_timer(_, chat_id, played, dur):
    try:
        played_sec = time_to_seconds(played)
        duration_sec = time_to_seconds(dur)

        percentage = (played_sec / duration_sec) * 100 if duration_sec != 0 else 0
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
        bar = "◉—————————"
        played = "0:00"
        dur = "0:00"

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton("▶", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton("⏸", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton("⏮", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton("⏭", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton("⏹", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton("✖ Close", callback_data=f"forceclose {chat_id}")
        ],
    ]
    return build(buttons)
