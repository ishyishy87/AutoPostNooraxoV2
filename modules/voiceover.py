import os
import requests
from datetime import datetime

from config import (
    VOICEOVER_ENABLED,
    VOICE_ENGINE,
    ELEVENLABS_API_KEY,
    ELEVENLABS_VOICE_ID,
    ELEVENLABS_MODEL,
    ELEVENLABS_OUTPUT_FORMAT,
    ELEVENLABS_STABILITY,
    ELEVENLABS_SIMILARITY_BOOST,
    ELEVENLABS_STYLE,
    ELEVENLABS_USE_SPEAKER_BOOST,
)
from modules.logger import log


def create_voiceover(script_text):
    """
    Creates human-like AI voiceover using ElevenLabs.
    Returns local mp3 path or None.
    """

    if not VOICEOVER_ENABLED:
        log("Voiceover skipped - disabled")
        return None

    if VOICE_ENGINE != "elevenlabs":
        log(f"Voiceover skipped - unsupported engine: {VOICE_ENGINE}")
        return None

    if not ELEVENLABS_API_KEY:
        log("Voiceover skipped - ELEVENLABS_API_KEY missing")
        return None

    if not ELEVENLABS_VOICE_ID or ELEVENLABS_VOICE_ID == "UT6USLtoAlXHj5k4sOLY":
        log("Voiceover skipped - ELEVENLABS_VOICE_ID missing")
        return None

    script_text = str(script_text).strip()

    if not script_text:
        log("Voiceover skipped - empty script")
        return None

    output_path = f"voiceover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"

    url = (
        f"https://api.elevenlabs.io/v1/text-to-speech/"
        f"{ELEVENLABS_VOICE_ID}?output_format={ELEVENLABS_OUTPUT_FORMAT}"
    )

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    payload = {
        "text": script_text,
        "model_id": ELEVENLABS_MODEL,
        "voice_settings": {
            "stability": ELEVENLABS_STABILITY,
            "similarity_boost": ELEVENLABS_SIMILARITY_BOOST,
            "style": ELEVENLABS_STYLE,
            "use_speaker_boost": ELEVENLABS_USE_SPEAKER_BOOST,
        },
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code != 200:
            log(f"ElevenLabs voiceover failed: HTTP {response.status_code} | {response.text[:500]}")
            return None

        with open(output_path, "wb") as f:
            f.write(response.content)

        if not os.path.exists(output_path) or os.path.getsize(output_path) < 1000:
            log("ElevenLabs voiceover failed - output file too small")
            return None

        log(f"ElevenLabs voiceover created: {output_path}")
        return output_path

    except Exception as e:
        log(f"ElevenLabs voiceover error: {e}")
        return None