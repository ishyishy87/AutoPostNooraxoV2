import os
import requests
from config import ACCESS_TOKEN, PAGE_ID
from modules.logger import log

GRAPH_VERSION = "v18.0"

def _safe_json_response(response):
    try:
        return response.json()
    except Exception:
        return {"error": {"message": response.text, "status_code": response.status_code}}

def upload_images(image_paths):
    ids = []

    for path in image_paths:
        if not os.path.exists(path):
            log(f"Image missing: {path}")
            continue

        url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PAGE_ID}/photos"

        try:
            with open(path, "rb") as img:
                r = requests.post(url, files={"source": img}, data={
                    "published": "false",
                    "access_token": ACCESS_TOKEN
                }, timeout=120)

            data = _safe_json_response(r)

            if "id" in data:
                ids.append(data["id"])
                log(f"Image uploaded successfully: {data['id']}")
            else:
                log(f"Image upload failed | HTTP {r.status_code}: {data}")

        except Exception as e:
            log(f"Image upload exception for {path}: {e}")

    return ids

def post_carousel(image_ids, caption_text):
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PAGE_ID}/feed"

    attached = [{"media_fbid": i} for i in image_ids]

    try:
        r = requests.post(url, json={
            "message": caption_text,
            "attached_media": attached,
            "access_token": ACCESS_TOKEN
        }, timeout=120)

        data = _safe_json_response(r)
        post_id = data.get("id")

        if post_id:
            log(f"Carousel post published successfully: {post_id}")
        else:
            log(f"Carousel post failed | HTTP {r.status_code}: {data}")

        return data, f"https://facebook.com/{post_id}" if post_id else None

    except Exception as e:
        log(f"Carousel post exception: {e}")
        return {"error": str(e)}, None

def upload_reel_video(video_path, caption_text):
    if not video_path or not os.path.exists(video_path):
        log("Reel upload skipped - video file not found")
        return None

    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PAGE_ID}/videos"

    try:
        with open(video_path, "rb") as video:
            r = requests.post(url, files={
                "source": video
            }, data={
                "description": caption_text,
                "access_token": ACCESS_TOKEN
            }, timeout=300)

        data = _safe_json_response(r)

        if "id" in data:
            log(f"Reel/video uploaded successfully: {data['id']}")
        else:
            log(f"Reel/video upload failed | HTTP {r.status_code}: {data}")

        return data

    except Exception as e:
        log(f"Reel/video upload exception: {e}")
        return {"error": str(e)}

def create_comment(post_id, comment_text):
    if not post_id:
        return None

    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{post_id}/comments"

    try:
        r = requests.post(url, data={
            "message": comment_text,
            "access_token": ACCESS_TOKEN
        }, timeout=60)

        data = _safe_json_response(r)

        if "id" in data:
            log(f"Auto comment posted: {data['id']}")
        else:
            log(f"Auto comment failed | HTTP {r.status_code}: {data}")

        return data

    except Exception as e:
        log(f"Auto comment error: {e}")
        return None

def delete_facebook_object(object_id):
    if not object_id:
        return False

    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{object_id}"

    try:
        r = requests.delete(url, data={
            "access_token": ACCESS_TOKEN
        }, timeout=60)

        data = _safe_json_response(r)
        log(f"Rollback delete response for {object_id} | HTTP {r.status_code}: {data}")

        return data.get("success") is True

    except Exception as e:
        log(f"Rollback delete failed for {object_id}: {e}")
        return False
