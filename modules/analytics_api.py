import requests

from config import ACCESS_TOKEN
from modules.logger import log


GRAPH_VERSION = "v20.0"


def safe_int(value):
    try:
        return int(value)
    except Exception:
        return 0


def get_count_from_edge(object_id, edge):
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{object_id}/{edge}"

    params = {
        "summary": "true",
        "limit": 0,
        "access_token": ACCESS_TOKEN,
    }

    try:
        r = requests.get(url, params=params, timeout=30)
        data = r.json()

        if "summary" in data:
            return safe_int(data["summary"].get("total_count", 0))

        log(f"Analytics {edge} count failed for {object_id}: {data}")
        return 0

    except Exception as e:
        log(f"Analytics {edge} count error for {object_id}: {e}")
        return 0


def get_post_basic_metrics(post_id):
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{post_id}"

    params = {
        "fields": "likes.summary(true).limit(0),comments.summary(true).limit(0),shares",
        "access_token": ACCESS_TOKEN,
    }

    metrics = {
        "likes": 0,
        "comments": 0,
        "shares": 0,
    }

    try:
        r = requests.get(url, params=params, timeout=30)
        data = r.json()

        if "error" in data:
            log(f"Post metrics fetch failed for {post_id}: {data}")
            return metrics

        metrics["likes"] = safe_int(
            data.get("likes", {}).get("summary", {}).get("total_count", 0)
        )

        metrics["comments"] = safe_int(
            data.get("comments", {}).get("summary", {}).get("total_count", 0)
        )

        metrics["shares"] = safe_int(
            data.get("shares", {}).get("count", 0)
        )

        return metrics

    except Exception as e:
        log(f"Post metrics fetch error for {post_id}: {e}")
        return metrics


def get_video_views(video_id):
    metrics_to_try = [
        "fb_reels_total_plays",
        "blue_reels_play_count",
        "post_impressions_unique",
    ]

    for metric in metrics_to_try:
        url = f"https://graph.facebook.com/{GRAPH_VERSION}/{video_id}/video_insights"

        params = {
            "metric": metric,
            "access_token": ACCESS_TOKEN,
        }

        try:
            r = requests.get(url, params=params, timeout=30)
            data = r.json()

            if "data" not in data:
                log(f"Video insight metric unavailable for {video_id} | {metric}")
                continue

            for item in data.get("data", []):
                values = item.get("values", [])
                if values:
                    value = safe_int(values[0].get("value", 0))
                    if value > 0:
                        log(f"Reel views/plays found using metric {metric}: {value}")
                        return value

        except Exception as e:
            log(f"Video insight skipped for {video_id} | {metric}: {e}")

    return 0

def get_reel_basic_metrics(reel_id):
    metrics = {
        "reel_likes": 0,
        "reel_comments": 0,
        "reel_views": 0,
    }

    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{reel_id}"

    params = {
        "fields": "likes.summary(true).limit(0),comments.summary(true).limit(0)",
        "access_token": ACCESS_TOKEN,
    }

    try:
        r = requests.get(url, params=params, timeout=30)
        data = r.json()

        if "error" in data:
            log(f"Reel metrics fetch failed for {reel_id}: {data}")
        else:
            metrics["reel_likes"] = safe_int(
                data.get("likes", {}).get("summary", {}).get("total_count", 0)
            )

            metrics["reel_comments"] = safe_int(
                data.get("comments", {}).get("summary", {}).get("total_count", 0)
            )

    except Exception as e:
        log(f"Reel metrics fetch error for {reel_id}: {e}")

    metrics["reel_views"] = get_video_views(reel_id)

    return metrics


def calculate_engagement_score(row):
    likes = safe_int(row.get("likes", 0))
    comments = safe_int(row.get("comments", 0))
    shares = safe_int(row.get("shares", 0))

    reel_likes = safe_int(row.get("reel_likes", 0))
    reel_comments = safe_int(row.get("reel_comments", 0))
    reel_views = safe_int(row.get("reel_views", 0))

    score = (
        likes
        + reel_likes
        + comments * 3
        + reel_comments * 3
        + shares * 5
        + int(reel_views * 0.05)
    )

    return score
