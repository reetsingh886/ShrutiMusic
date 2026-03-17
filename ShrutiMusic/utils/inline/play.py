import math
from pyrogram.types import InlineKeyboardButton
from ShrutiMusic.utils.formatters import time_to_seconds
from config import BOT_USERNAME


# ================= SAFE EXTRACT ================= #

def safe_get(args, index, default=None):
    try:
        return args[index]
    except:
        return default


# ================= TRACK ================= #

def track_markup(*args):
    videoid = safe_get(args, 1)
    user_id = safe_get(args, 2)
    ptype = safe_get(args, 3)
    channel = safe_get(args, 4)
    fplay = safe_get(args, 5)

    return [
        [
            InlineKeyboardButton(
                text="▶ Audio",
                callback_data=f"NandPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="🎥 Video",
                callback_data=f"NandPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="✖ Close",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


# ================= STREAM ================= #

def stream_markup(*args):
    videoid = safe_get(args, 1)
    user_id = safe_get(args, 2)
    channel = safe_get(args, 3)
    fplay = safe_get(args, 4)

    return [
        [
            InlineKeyboardButton(
                text="▶ Audio",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="🎥 Video",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="✖ Close",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


# ================= PLAYLIST ================= #

def playlist_markup(*args):
    return stream_markup(*args)


# ================= LIVE ================= #

def livestream_markup(*args):
    videoid = safe_get(args, 1)
    user_id = safe_get(args, 2)
    mode = safe_get(args, 3)
    channel = safe_get(args, 4)
    fplay = safe_get(args, 5)

    return [
        [
            InlineKeyboardButton(
                text="🔴 Live",
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="✖ Close",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


# ================= SLIDER ================= #

def slider_markup(*args):
    videoid = safe_get(args, 1)
    user_id = safe_get(args, 2)
    query = str(safe_get(args, 3, ""))[:20]
    query_type = safe_get(args, 4)
    channel = safe_get(args, 5)
    fplay = safe_get(args, 6)

    return [
        [
            InlineKeyboardButton(
                text="▶ Audio",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="🎥 Video",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="✖ Close",
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]


# ================= TIMER ================= #

def stream_markup_timer(*args):
    chat_id = safe_get(args, 1)
    played = safe_get(args, 2, "0:00")
    dur = safe_get(args, 3, "0:00")

    try:
        played_sec = time_to_seconds(played)
        duration_sec = time_to_seconds(dur)

        percentage = (played_sec / duration_sec) * 100 if duration_sec else 0
        umm = int(percentage)

        bars = [
            "◉—————————","—◉————————","——◉———————","———◉——————",
            "————◉—————","—————◉————","——————◉———","———————◉——",
            "————————◉—","—————————◉"
        ]
        bar = bars[min(len(bars)-1, umm//10)]

    except:
        bar = "◉—————————"

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
            InlineKeyboardButton("✖ Close", callback_data=f"forceclose {chat_id}")
        ],
    ]
