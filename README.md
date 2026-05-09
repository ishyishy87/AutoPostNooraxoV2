# Facebook AI Cinematic Business Engine

This project converts your Facebook product automation into a modular AI-style ecommerce media engine.

## What is included

- Facebook carousel product post
- Facebook reel upload
- Rollback if reel fails after post creation
- Local AI marketing captions
- Local AI hashtags
- Local AI product benefits
- Viral reel scene structure
- Real animated reel effects
- Roman Urdu + English neural AI voiceover
- Slow low-volume background music
- Auto comment after post publication
- Memory tracking
- GitHub Actions friendly setup

## Voiceover

Primary voice engine:

```python
VOICE_ENGINE = "edge"
EDGE_TTS_VOICE = "en-IN-NeerjaNeural"
EDGE_TTS_RATE = "-8%"
```

This creates a clearer Roman Urdu + English ecommerce voiceover such as:

```text
Stop scrolling. Yeh product aap ke liye smart pick ho sakta hai. Price sirf 999 rupees. Cash on Delivery available hai.
```

Fallback engine:

```python
gTTS
```

If Edge TTS fails, the script still creates voiceover using gTTS.

## Audio mix

Voice is intentionally louder than music:

```python
VOICEOVER_VOLUME = 1.35
MUSIC_VOLUME_WITH_VOICEOVER = 0.10
MUSIC_SPEED_FACTOR = 0.92
```

This makes the background music slow and soft while the AI voice remains clear.

## Title safety

The product title is never rewritten. It is used exactly as stored in `products.csv`.

## Required secrets

Set these in GitHub repository secrets:

```text
ACCESS_TOKEN
PAGE_ID
```

## Requirements

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```
