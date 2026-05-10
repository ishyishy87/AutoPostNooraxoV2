import os

# ================= CORE FILES =================

PRODUCTS_FILE = "products.csv"
MEMORY_FILE = "memory.csv"
LOG_FILE = "run_log.txt"
RUN_LOCK_FILE = "run_lock.txt"

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

# ================= WHATSAPP ALERTS =================

WHATSAPP_ALERT_ENABLED = True

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_TO_NUMBER = os.getenv("WHATSAPP_TO_NUMBER")

# ================= AI COMMENT REPLY =================

AI_COMMENT_REPLY_ENABLED = True

COMMENT_REPLY_LIMIT = 10

COMMENT_MEMORY_FILE = "comment_memory.csv"

COMMENT_REPLY_SIGNATURE = "😊"

# ================= WHATSAPP LEAD FUNNEL =================

WHATSAPP_LEAD_FUNNEL_ENABLED = True

# Use international format without +, spaces, or dashes
BUSINESS_WHATSAPP_NUMBER = "923169250202"

LEAD_MEMORY_FILE = "lead_memory.csv"

LEAD_TRIGGER_WORDS = [
    "price", "rate", "kitna", "available", "stock",
    "order", "book", "buy", "interested", "details",
    "cod", "cash", "delivery", "inbox", "want", "chahiye"
]

# ================= AUTOMATION =================

POST_ONCE_PER_DAY = True
ROLLBACK_IF_REEL_FAILS = True
AUTO_COMMENT_ENABLED = True

# ================= VIDEO / REELS =================

REELS_ENABLED = True
VIDEO_OUTPUT_DIR = "videos"
VIDEO_SIZE = (1080, 1920)
VIDEO_FPS = 24

# Scene timing is now voice-aware. These values are safe limits.
IMAGE_DURATION = 3.2
MIN_SCENE_DURATION = 2.8
MAX_SCENE_DURATION = 5.2
VOICE_LEAD_SECONDS = 0.35
VOICE_TAIL_SECONDS = 0.8

VIDEO_BG_COLOR = (8, 8, 12)
TEXT_COLOR = "white"

# Keep effects safe for GitHub runner.
KEN_BURNS_ENABLED = True

# ================= ONLINE MUSIC =================

MUSIC_ENABLED = True

OPEN_MUSIC_URLS = [
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-13.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-14.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-16.mp3",
]


# ================= ELEVENLABS VOICEOVER =================

VOICEOVER_ENABLED = True

VOICE_ENGINE = "elevenlabs"

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Replace this with your selected ElevenLabs female voice ID
ELEVENLABS_VOICE_ID = "UT6USLtoAlXHj5k4sOLY"

ELEVENLABS_MODEL = "eleven_multilingual_v2"

ELEVENLABS_OUTPUT_FORMAT = "mp3_44100_128"

ELEVENLABS_STABILITY = 0.48
ELEVENLABS_SIMILARITY_BOOST = 0.78
ELEVENLABS_STYLE = 0.45
ELEVENLABS_USE_SPEAKER_BOOST = True

# Final mix
VOICEOVER_VOLUME = 1.25
MUSIC_VOLUME_WITH_VOICEOVER = 0.05
MUSIC_VOLUME_WITHOUT_VOICEOVER = 0.28

MUSIC_SPEED_FACTOR = 0.92
MUSIC_FADEIN_SECONDS = 1.0
MUSIC_FADEOUT_SECONDS = 1.5

# ================= REAL ANIMATED REEL EFFECTS =================

REEL_TRANSITION_SECONDS = 0.35
ZOOM_START = 1.00
ZOOM_END = 1.10
PAN_PIXELS = 42
SUBTITLE_ENABLED = True
SUBTITLE_STYLE = "roman_urdu_english"
