import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy.editor import (
    ImageClip, concatenate_videoclips, AudioFileClip,
    CompositeVideoClip, CompositeAudioClip
)
from moviepy.video.fx import all as vfx
from moviepy.audio.fx import all as afx

from config import (
    VIDEO_OUTPUT_DIR, VIDEO_SIZE, VIDEO_FPS, IMAGE_DURATION,
    MIN_SCENE_DURATION, MAX_SCENE_DURATION, VOICE_LEAD_SECONDS, VOICE_TAIL_SECONDS,
    VIDEO_BG_COLOR, TEXT_COLOR, REELS_ENABLED, KEN_BURNS_ENABLED,
    REEL_TRANSITION_SECONDS, ZOOM_START, ZOOM_END, PAN_PIXELS,
    VOICEOVER_VOLUME, MUSIC_VOLUME_WITH_VOICEOVER, MUSIC_VOLUME_WITHOUT_VOICEOVER,
    MUSIC_SPEED_FACTOR, MUSIC_FADEIN_SECONDS, MUSIC_FADEOUT_SECONDS,
    SUBTITLE_ENABLED
)
from modules.logger import log
from modules.music import download_random_music
from modules.local_ai import generate_reel_scenes, generate_voiceover_script
from modules.voiceover import create_voiceover


def _load_font(size):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except Exception:
        return ImageFont.load_default()


def _text_width(draw, text, font):
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0]
    except Exception:
        return draw.textsize(text, font=font)[0]


def _wrap_text(draw, text, font, max_width, max_lines=4):
    words = str(text).split()
    lines = []
    current = ""

    for word in words:
        test = (current + " " + word).strip()
        width = _text_width(draw, test, font)

        if width <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines[:max_lines]


def _draw_centered_text(draw, text, y, font, fill=TEXT_COLOR, max_width=940, shadow=True, max_lines=4):
    lines = _wrap_text(draw, text, font, max_width, max_lines=max_lines)
    line_height = font.size + 12 if hasattr(font, "size") else 35

    for i, line in enumerate(lines):
        w = _text_width(draw, line, font)
        x = (VIDEO_SIZE[0] - w) // 2
        yy = y + i * line_height

        if shadow:
            draw.text((x + 4, yy + 4), line, fill=(0, 0, 0), font=font)
        draw.text((x, yy), line, fill=fill, font=font)


def _category_accent(scene_index):
    accents = [
        (255, 196, 0),
        (0, 210, 255),
        (255, 78, 129),
        (64, 255, 155),
        (185, 120, 255),
    ]
    return accents[scene_index % len(accents)]


def prepare_reel_scene_image(image_path, scene_text, title="", price="", scene_index=0, output_size=VIDEO_SIZE):
    img = Image.open(image_path).convert("RGB")

    # Premium blurred fill background.
    bg = img.copy()
    bg.thumbnail(output_size)
    background = Image.new("RGB", output_size, VIDEO_BG_COLOR)
    bx = (output_size[0] - bg.width) // 2
    by = (output_size[1] - bg.height) // 2
    background.paste(bg, (bx, by))
    background = background.filter(ImageFilter.GaussianBlur(28))

    # Dark cinematic overlay.
    overlay = Image.new("RGBA", output_size, (0, 0, 0, 92))
    background = Image.alpha_composite(background.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(background)

    accent = _category_accent(scene_index)

    # Product image card.
    product = img.copy()
    product.thumbnail((output_size[0] - 120, int(output_size[1] * 0.58)))

    card_w = product.width + 40
    card_h = product.height + 40
    card_x = (output_size[0] - card_w) // 2
    card_y = 405 + ((900 - product.height) // 2)

    # soft glow
    glow_pad = 18
    draw.rounded_rectangle(
        (card_x - glow_pad, card_y - glow_pad, card_x + card_w + glow_pad, card_y + card_h + glow_pad),
        radius=48,
        fill=(accent[0] // 5, accent[1] // 5, accent[2] // 5),
    )
    draw.rounded_rectangle(
        (card_x, card_y, card_x + card_w, card_y + card_h),
        radius=38,
        fill=(255, 255, 255),
        outline=accent,
        width=7
    )

    px = card_x + 20
    py = card_y + 20
    background.paste(product, (px, py))

    # Top hook panel.
    draw.rounded_rectangle((90, 70, output_size[0] - 90, 205), radius=34, fill=(10, 10, 18), outline=accent, width=3)

    # Bottom title/CTA panel.
    draw.rounded_rectangle((140, 1625, output_size[0] - 140, 1815), radius=34, fill=(10, 10, 18), outline=accent, width=3)

    scene_font = _load_font(52)
    title_font = _load_font(34)
    price_font = _load_font(66)
    small_font = _load_font(32)

    # Main scene text works like animated subtitle panel.
    short_scene_text = str(scene_text).split(".")[0][:28]
    _draw_centered_text(draw, short_scene_text, 105, scene_font, fill=(255, 255, 255), max_lines=1)

    # Product title is preserved exactly from CSV.
    if scene_index == 0:
        _draw_centered_text(draw, str(title)[:42], 1655, title_font, fill=(255, 255, 255), max_lines=2)

    if scene_index >= 3:
        _draw_centered_text(draw, f"Rs {price}", 1685, price_font, fill=accent, max_lines=1)
    else:
        _draw_centered_text(draw, "COD Available", 1705, small_font, fill=accent, max_lines=1)

    # Small progress indicator.
    total_dots = 5
    dot_y = 1855
    start_x = (output_size[0] - (total_dots * 28)) // 2
    for i in range(total_dots):
        fill = accent if i == scene_index % total_dots else (90, 90, 100)
        draw.ellipse((start_x + i * 28, dot_y, start_x + i * 28 + 12, dot_y + 12), fill=fill)

    prepared_path = f"reel_scene_{scene_index}_{os.path.basename(image_path)}"
    background.save(prepared_path, quality=95)

    return prepared_path


def _apply_motion_effects(base_clip, scene_index):
    duration = base_clip.duration

    if KEN_BURNS_ENABLED:
        direction = -1 if scene_index % 2 == 0 else 1

        animated = (
            base_clip
            .resize(lambda t: ZOOM_START + ((ZOOM_END - ZOOM_START) * (t / max(duration, 0.1))))
            .set_position(lambda t: (
                int(direction * PAN_PIXELS * (t / max(duration, 0.1))),
                "center"
            ))
        )

        clip = CompositeVideoClip([animated], size=VIDEO_SIZE)
    else:
        clip = CompositeVideoClip([base_clip.set_position(("center", "center"))], size=VIDEO_SIZE)

    clip = clip.fx(vfx.fadein, REEL_TRANSITION_SECONDS).fx(vfx.fadeout, REEL_TRANSITION_SECONDS)
    return clip


def _safe_audio_duration(audio_path):
    if not audio_path:
        return 0
    try:
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        audio.close()
        return duration
    except Exception as e:
        log(f"Could not read voiceover duration: {e}")
        return 0


def _calculate_scene_duration(scene_count, voiceover_path):
    voice_duration = _safe_audio_duration(voiceover_path)

    if voice_duration <= 0:
        return IMAGE_DURATION

    # Add lead/tail and compensate for negative transition padding.
    target_total = voice_duration + VOICE_LEAD_SECONDS + VOICE_TAIL_SECONDS
    transition_gain = max(0, scene_count - 1) * REEL_TRANSITION_SECONDS
    raw_duration = (target_total + transition_gain) / max(scene_count, 1)

    return max(MIN_SCENE_DURATION, min(MAX_SCENE_DURATION, raw_duration))


def _build_audio_track(video, voiceover_path, music_path):
    audio_layers = []

    if music_path:
        try:
            music = AudioFileClip(music_path)

            # Create a slower emotional music feel. If speed effect fails, continue normal.
            try:
                if MUSIC_SPEED_FACTOR and MUSIC_SPEED_FACTOR != 1:
                    music = music.fx(afx.speedx, MUSIC_SPEED_FACTOR)
                    log(f"Background music slowed with factor: {MUSIC_SPEED_FACTOR}")
            except Exception as e:
                log(f"Music speed adjustment skipped: {e}")

            music = music.fx(afx.audio_loop, duration=video.duration)

            if voiceover_path:
                music = music.volumex(MUSIC_VOLUME_WITH_VOICEOVER)
            else:
                music = music.volumex(MUSIC_VOLUME_WITHOUT_VOICEOVER)

            try:
                music = music.fx(afx.audio_fadein, MUSIC_FADEIN_SECONDS).fx(afx.audio_fadeout, MUSIC_FADEOUT_SECONDS)
            except Exception:
                pass

            audio_layers.append(music.set_start(0))
            log("Slow low-volume background music added to reel audio mix")

        except Exception as e:
            log(f"Music attach failed: {e}")

    if voiceover_path:
        try:
            voice = AudioFileClip(voiceover_path).volumex(VOICEOVER_VOLUME)
            voice = voice.set_start(VOICE_LEAD_SECONDS)

            if voice.duration + VOICE_LEAD_SECONDS > video.duration:
                max_voice = max(0.1, video.duration - VOICE_LEAD_SECONDS)
                voice = voice.subclip(0, max_voice).set_start(VOICE_LEAD_SECONDS)

            audio_layers.append(voice)
            log(f"Roman Urdu + English AI voiceover added | Duration: {voice.duration}")

        except Exception as e:
            log(f"Voiceover attach failed: {e}")

    if not audio_layers:
        return video

    return video.set_audio(CompositeAudioClip(audio_layers).set_duration(video.duration))


def create_reel_video(image_files, title, price, score):
    if not REELS_ENABLED:
        log("Reels video skipped - disabled")
        return None, {}

    if not image_files:
        log("Reels video skipped - no images found")
        return None, {}

    os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)

    scenes, scene_meta = generate_reel_scenes(title, price, score)
    voiceover_script = generate_voiceover_script(title, price, score)

    voiceover_path = create_voiceover(voiceover_script)
    scene_duration = _calculate_scene_duration(len(scenes), voiceover_path)

    log(f"Voice-aware scene duration selected: {scene_duration:.2f}s")
    log(f"Voiceover script: {voiceover_script}")

    clips = []

    for i, scene_text in enumerate(scenes):
        image_path = image_files[i % len(image_files)]

        prepared_img = prepare_reel_scene_image(
            image_path=image_path,
            scene_text=scene_text,
            title=title,
            price=price,
            scene_index=i
        )

        base_clip = ImageClip(prepared_img).set_duration(scene_duration)
        clip = _apply_motion_effects(base_clip, i)
        clips.append(clip)

    video = concatenate_videoclips(
        clips,
        method="compose",
        padding=-REEL_TRANSITION_SECONDS
    )

    output_path = os.path.join(
        VIDEO_OUTPUT_DIR,
        f"reel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    )

    music_path = download_random_music()
    video = _build_audio_track(video, voiceover_path, music_path)

    video.write_videofile(
        output_path,
        fps=VIDEO_FPS,
        codec="libx264",
        audio=True,
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True
    )

    if video.audio:
        log("Final reel has audio before upload")
    else:
        log("WARNING: Final reel has NO audio before upload")

    scene_meta["voiceover_enabled"] = bool(voiceover_path)
    scene_meta["voiceover_style"] = "roman_urdu_english_neural"
    scene_meta["voiceover_script"] = voiceover_script
    scene_meta["scene_duration"] = scene_duration
    scene_meta["motion_effects"] = "ken_burns_zoom_pan_fade_glow_card" if KEN_BURNS_ENABLED else "fade_only"
    scene_meta["subtitles"] = "scene_text_overlays" if SUBTITLE_ENABLED else "disabled"

    log(f"Cinematic reel video created: {output_path}")

    return output_path, scene_meta
