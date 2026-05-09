import os
import asyncio
import tempfile
from datetime import datetime

from config import (
    VOICEOVER_ENABLED, VOICE_ENGINE,
    EDGE_TTS_VOICE, EDGE_TTS_RATE, EDGE_TTS_VOLUME,
    GTTS_LANG, GTTS_SLOW
)
from modules.logger import log

LAST_VOICEOVER_PATH = ""
LAST_VOICEOVER_ENGINE = ""

async def _edge_tts_save(script_text, voice_path):
    import edge_tts

    communicate = edge_tts.Communicate(
        text=str(script_text),
        voice=EDGE_TTS_VOICE,
        rate=EDGE_TTS_RATE,
        volume=EDGE_TTS_VOLUME
    )
    await communicate.save(voice_path)


def _create_edge_voiceover(script_text, voice_path):
    asyncio.run(_edge_tts_save(script_text, voice_path))
    return voice_path


def _create_gtts_voiceover(script_text, voice_path):
    from gtts import gTTS

    tts = gTTS(
        text=str(script_text),
        lang=GTTS_LANG,
        slow=GTTS_SLOW
    )
    tts.save(voice_path)
    return voice_path


def create_voiceover(script_text):
    """
    Creates a Roman Urdu + English AI-style voiceover.
    Primary engine: Edge TTS neural voice.
    Fallback engine: gTTS.
    No OpenAI API is used.
    """
    global LAST_VOICEOVER_PATH, LAST_VOICEOVER_ENGINE

    if not VOICEOVER_ENABLED:
        log("Voiceover skipped - disabled")
        return None

    if not script_text or not str(script_text).strip():
        log("Voiceover skipped - empty script")
        return None

    voice_path = os.path.join(
        tempfile.gettempdir(),
        f"voiceover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    )

    # Try neural Edge TTS first.
    if str(VOICE_ENGINE).lower() == "edge":
        try:
            _create_edge_voiceover(script_text, voice_path)
            LAST_VOICEOVER_PATH = voice_path
            LAST_VOICEOVER_ENGINE = "edge_tts"
            log(f"Neural AI voiceover created with Edge TTS: {voice_path}")
            return voice_path
        except Exception as e:
            log(f"Edge TTS voiceover failed, falling back to gTTS: {e}")

    # Fallback.
    try:
        _create_gtts_voiceover(script_text, voice_path)
        LAST_VOICEOVER_PATH = voice_path
        LAST_VOICEOVER_ENGINE = "gtts_fallback"
        log(f"Fallback AI voiceover created with gTTS: {voice_path}")
        return voice_path
    except Exception as e:
        log(f"Voiceover creation failed: {e}")
        return None
