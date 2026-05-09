import os
import requests
from config import ACCESS_TOKEN, PAGE_ID
from modules.logger import log

def upload_images(image_paths):
    ids = []

    for path in image_paths:
        if not os.path.exists(path):
            log(f"Image missing: {path}")
            continue

        url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/photos"

        with open(path, "rb") as img:
            r = requests.post(url, files={"source": img}, data={
                "published": "false",
                "access_token": ACCESS_TOKEN
            })

        data = r.json()

        if "id" in data:
            ids.append(data["id"])
        else:
            log(f"Image upload failed: {data}")

    return ids

def post_carousel(image_ids, caption_text):
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/feed"

    attached = [{"media_fbid": i} for i in image_ids]

    r = requests.post(url, json={
        "message": caption_text,
        "attached_media": attached,
        "access_token": ACCESS_TOKEN
    })

    data = r.json()
    post_id = data.get("id")

    return data, f"https://facebook.com/{post_id}" if post_id else None

def upload_reel_video(video_path, caption_text):
    if not video_path or not os.path.exists(video_path):
        log("Reel upload skipped - video file not found")
        return None

    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/videos"

    with open(video_path, "rb") as video:
        r = requests.post(url, files={
            "source": video
        }, data={
            "description": caption_text,
            "access_token": ACCESS_TOKEN
        })

    data = r.json()

    if "id" in data:
        log(f"Reel/video uploaded successfully: {data['id']}")
    else:
        log(f"Reel/video upload failed: {data}")

    return data

def create_comment(post_id, comment_text):
    if not post_id:
        return None

    url = f"https://graph.facebook.com/v18.0/{post_id}/comments"

    try:
        r = requests.post(url, data={
            "message": comment_text,
            "access_token": ACCESS_TOKEN
        })

        data = r.json()

        if "id" in data:
            log(f"Auto comment posted: {data['id']}")
        else:
            log(f"Auto comment failed: {data}")

        return data

    except Exception as e:
        log(f"Auto comment error: {e}")
        return None

def delete_facebook_object(object_id):
    if not object_id:
        return False

    url = f"https://graph.facebook.com/v18.0/{object_id}"

    try:
        r = requests.delete(url, data={
            "access_token": ACCESS_TOKEN
        })

        data = r.json()
        log(f"Rollback delete response for {object_id}: {data}")

        return data.get("success") is True

    except Exception as e:
        log(f"Rollback delete failed for {object_id}: {e}")
        return False
