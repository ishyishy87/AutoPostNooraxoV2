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
        "fields": "shares",
        "access_token": ACCESS_TOKEN,
    }

    shares = 0

    try:
        r = requests.get(url, params=params, timeout=30)
        data = r.json()

        if "shares" in data:
            shares = safe_int(data.get("shares", {}).get("count", 0))

    except Exception as e:
        log(f"Post share fetch error for {post_id}: {e}")

    reactions = get_count_from_edge(post_id, "reactions")
    comments = get_count_from_edge(post_id, "comments")

    return {
        "likes": reactions,
        "comments": comments,
        "shares": shares,
    }


def get_video_views(video_id):
    """
    Try to fetch video/reel views.
    Some metrics may not be available depending on permissions/object type.
    """

    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{video_id}/video_insights"

    params = {
        "metric": "total_video_views",
        "access_token": ACCESS_TOKEN,
    }

    try:
        r = requests.get(url, params=params, timeout=30)
        data = r.json()

        if "data" not in data:
            log(f"Video insights failed for {video_id}: {data}")
            return 0

        for item in data.get("data", []):
            if item.get("name") == "total_video_views":
                values = item.get("values", [])
                if values:
                    return safe_int(values[0].get("value", 0))

        return 0

    except Exception as e:
        log(f"Video insights error for {video_id}: {e}")
        return 0


def get_reel_basic_metrics(reel_id):
    comments = get_count_from_edge(reel_id, "comments")
    reactions = get_count_from_edge(reel_id, "reactions")
    views = get_video_views(reel_id)

    return {
        "reel_likes": reactions,
        "reel_comments": comments,
        "reel_views": views,
    }


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
