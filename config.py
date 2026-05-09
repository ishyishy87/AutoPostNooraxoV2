import os

# ================= CORE FILES =================

PRODUCTS_FILE = "products.csv"
MEMORY_FILE = "memory.csv"
LOG_FILE = "run_log.txt"
RUN_LOCK_FILE = "run_lock.txt"

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

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

# ================= AI CINEMATIC VOICEOVER =================

VOICEOVER_ENABLED = True

# ================= EDGE TTS =================
# Pakistani Female Neural Voice
# Human-like Roman Urdu + English ecommerce narration

VOICE_ENGINE = "edge"

EDGE_TTS_VOICE = "ur-PK-UzmaNeural"

# Slightly slower for premium selling feel
EDGE_TTS_RATE = "-5%"

# Stronger clearer female voice
EDGE_TTS_VOLUME = "+25%"

# ================= GTTS FALLBACK =================

GTTS_LANG = "ur"
GTTS_SLOW = False

# ================= FINAL AUDIO MIX =================
# Voice should dominate
# Music should stay cinematic and soft

VOICEOVER_VOLUME = 1.45

MUSIC_VOLUME_WITH_VOICEOVER = 0.08

MUSIC_VOLUME_WITHOUT_VOICEOVER = 0.30

# Slightly slower music for cinematic emotional feel
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
