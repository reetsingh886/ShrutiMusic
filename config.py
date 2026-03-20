import os
import re
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# 🔹 BASIC
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "iamthakur007")
BOT_USERNAME = os.getenv("BOT_USERNAME", "")

MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0"))

# 🔹 HEROKU
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")

# 🔹 REPO
UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "main")

# 🔹 SUPPORT LINKS (PREMIUM FEEL)
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/BOTxBOOSTER")
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/BOTxBOOSTER")

INSTAGRAM = os.getenv("INSTAGRAM", "")
YOUTUBE = os.getenv("YOUTUBE", "")
GITHUB = os.getenv("GITHUB", "")
DONATE = os.getenv("DONATE", "")
PRIVACY_LINK = os.getenv("PRIVACY_LINK", "")

# 🔹 LIMITS
DURATION_LIMIT_MIN = int(os.getenv("DURATION_LIMIT", "300"))
PLAYLIST_FETCH_LIMIT = int(os.getenv("PLAYLIST_FETCH_LIMIT", "25"))

TG_AUDIO_FILESIZE_LIMIT = int(os.getenv("TG_AUDIO_FILESIZE_LIMIT", "104857600"))
TG_VIDEO_FILESIZE_LIMIT = int(os.getenv("TG_VIDEO_FILESIZE_LIMIT", "2145386496"))

# 🔹 SPOTIFY
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

# 🔹 SESSIONS
STRING1 = os.getenv("STRING_SESSION", "")
STRING2 = os.getenv("STRING_SESSION2")
STRING3 = os.getenv("STRING_SESSION3")
STRING4 = os.getenv("STRING_SESSION4")
STRING5 = os.getenv("STRING_SESSION5")

# 🔹 AUTO (FIXED BOOL)
AUTO_LEAVING_ASSISTANT = os.getenv("AUTO_LEAVING_ASSISTANT", "False") == "True"

# 🔥 🔹 PREMIUM IMAGE THEME (SHASHANK STYLE KEEP)
START_IMG_URL = os.getenv("START_IMG_URL", "https://files.catbox.moe/fh7vw7.jpg")
PING_IMG_URL = os.getenv("PING_IMG_URL", "https://files.catbox.moe/fh7vw7.jpg")

PLAYLIST_IMG_URL = "https://files.catbox.moe/lckxh6.jpg"
STATS_IMG_URL = "https://files.catbox.moe/smteo6.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/7enu2i.jpg"

TELEGRAM_AUDIO_URL = "https://files.catbox.moe/n6hkvd.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/ej1p7t.jpg"

SOUNCLOUD_IMG_URL = "https://files.catbox.moe/lckxh6.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/smteo6.jpg"

SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/7enu2i.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/n6hkvd.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/ej1p7t.jpg"

# 🔹 RUNTIME
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

TEMP_DB_FOLDER = "tempdb"

# 🔹 TIME CONVERTER
def time_to_seconds(time):
    return sum(int(x) * 60**i for i, x in enumerate(reversed(str(time).split(":"))))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")

# 🔹 VALIDATION (SAFE)
if SUPPORT_CHANNEL and not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("Invalid SUPPORT_CHANNEL URL")

if SUPPORT_GROUP and not re.match(r"(?:http|https)://", SUPPORT_GROUP):
    raise SystemExit("Invalid SUPPORT_GROUP URL")
