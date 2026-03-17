import math
from pyrogram.types import InlineKeyboardButton
from ShrutiMusic.utils.formatters import time_to_seconds
from config import BOT_USERNAME


# ================= TRACK ================= #

def track_markup(_, videoid, user_id, ptype, channel, fplay):
    try:
        return [
            [
                InlineKeyboardButton(
                    text=_["P_B_1"],
                    callback_data=f"NandPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
                ),
                InlineKeyboardButton(
                    text=_["P_B_2"],
                    callback_data=f"NandPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data=f"forceclose {videoid}|{user_id}",
                ),
            ],
        ]
    except:
        return []


# ================= STREAM ================= #

def stream_markup(_, videoid, user_id, channel, fplay):
    try:
        return [
            [
                InlineKeyboardButton(
                    text=_["P_B_1"],
                    callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                ),
                InlineKeyboardButton(
                    text=_["P_B_2"],
                    callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data=f"forceclose {videoid}|{user_id}",
                ),
            ],
        ]
    except:
        return []


# ================= PLAYLIST ================= #

def playlist_markup(_, videoid, user_id, channel, fplay):
    return stream_markup(_, videoid, user_id, channel, fplay)


# ================= LIVE ================= #

def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    try:
        return [
            [
                InlineKeyboardButton(
                    text=_["P_B_3"],
                    callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data=f"forceclose {videoid}|{user_id}",
                ),
            ],
        ]
    except:
        return []


# ================= SLIDER ================= #

def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    try:
        query = str(query)[:20]

        return [
            [
                InlineKeyboardButton(
                    text=_["P_B_1"],
                    callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                ),
                InlineKeyboardButton(
                    text=_["P_B_2"],
                    callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="◁",
                    callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data=f"forceclose {query}|{user_id}",
                ),
                InlineKeyboardButton(
                    text="▷",
                    callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                ),
            ],
        ]
    except:
        return []


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

    try:
        return [
            [
                InlineKeyboardButton(
                    text=f"{played} {bar} {dur}",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
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
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data=f"forceclose {chat_id}",
                )
            ],
        ]
    except:
        return []
