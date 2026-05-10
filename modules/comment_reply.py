import os
import pandas as pd
import requests

from config import (
    ACCESS_TOKEN,
    COMMENT_MEMORY_FILE,
    COMMENT_REPLY_LIMIT,
    AI_COMMENT_REPLY_ENABLED,
)

from modules.logger import log
from modules.comment_ai import generate_comment_reply


def load_comment_memory():
    if not os.path.exists(COMMENT_MEMORY_FILE):
        df = pd.DataFrame(columns=["comment_id", "post_id", "reply", "date"])
        df.to_csv(COMMENT_MEMORY_FILE, index=False)
        return df

    return pd.read_csv(COMMENT_MEMORY_FILE)


def save_comment_memory(df):
    df.to_csv(COMMENT_MEMORY_FILE, index=False)


def get_post_comments(post_id):
    url = f"https://graph.facebook.com/v20.0/{post_id}/comments"

    params = {
        "fields": "id,message,from,created_time",
        "limit": COMMENT_REPLY_LIMIT,
        "access_token": ACCESS_TOKEN,
    }

    try:
        r = requests.get(url, params=params, timeout=30)
        data = r.json()

        if "data" not in data:
            log(f"Comment fetch failed: {data}")
            return []

        return data.get("data", [])

    except Exception as e:
        log(f"Comment fetch error: {e}")
        return []


def reply_to_comment(comment_id, reply_text):
    url = f"https://graph.facebook.com/v20.0/{comment_id}/comments"

    payload = {
        "message": reply_text,
        "access_token": ACCESS_TOKEN,
    }

    try:
        r = requests.post(url, data=payload, timeout=30)
        data = r.json()

        if "id" in data:
            log(f"AI comment reply sent: {comment_id}")
            return True

        log(f"AI comment reply failed: {data}")
        return False

    except Exception as e:
        log(f"AI comment reply error: {e}")
        return False


def process_post_comments(post_id, title="", price=""):
    if not AI_COMMENT_REPLY_ENABLED:
        log("AI comment reply skipped - disabled")
        return

    if not post_id:
        log("AI comment reply skipped - post_id missing")
        return

    memory = load_comment_memory()
    replied = set(memory["comment_id"].astype(str))

    comments = get_post_comments(post_id)

    if not comments:
        log("No comments found for AI reply")
        return

    new_rows = []

    for comment in comments:
        comment_id = str(comment.get("id", ""))
        message = str(comment.get("message", "")).strip()

        if not comment_id or not message:
            continue

        if comment_id in replied:
            continue

        reply = generate_comment_reply(message, title, price)

        ok = reply_to_comment(comment_id, reply)

        if ok:
            new_rows.append({
                "comment_id": comment_id,
                "post_id": post_id,
                "reply": reply,
                "date": str(pd.Timestamp.now()),
            })

    if new_rows:
        memory = pd.concat([memory, pd.DataFrame(new_rows)], ignore_index=True)
        save_comment_memory(memory)
        log(f"AI comment replies completed: {len(new_rows)}")
    else:
        log("No new comments required AI reply")
