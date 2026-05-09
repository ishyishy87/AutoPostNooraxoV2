import os
import random
import tempfile
from datetime import datetime
import requests
from config import MUSIC_ENABLED, OPEN_MUSIC_URLS
from modules.logger import log

LAST_SELECTED_MUSIC_URL = ""

def download_random_music():
    global LAST_SELECTED_MUSIC_URL

    if not MUSIC_ENABLED:
        log("Music skipped - disabled")
        return None

    if not OPEN_MUSIC_URLS:
        log("Music skipped - no music URLs configured")
        return None

    music_url = random.choice(OPEN_MUSIC_URLS)
    LAST_SELECTED_MUSIC_URL = music_url

    log(f"Selected online music: {music_url}")

    try:
        r = requests.get(music_url, stream=True, timeout=25)

        if r.status_code != 200:
            log(f"Music download failed: HTTP {r.status_code}")
            return None

        music_path = os.path.join(
            tempfile.gettempdir(),
            f"music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        )

        with open(music_path, "wb") as f:
            for chunk in r.iter_content(1024):
                if chunk:
                    f.write(chunk)

        log(f"Music downloaded: {music_path}")
        return music_path

    except Exception as e:
        log(f"Music download error: {e}")
        return None
