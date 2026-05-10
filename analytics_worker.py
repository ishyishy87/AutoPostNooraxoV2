import pandas as pd

from config import ANALYTICS_ENABLED, ANALYTICS_SCAN_LIMIT, ANALYTICS_MEMORY_FILE
from modules.logger import log
from modules.analytics_api import (
    get_post_basic_metrics,
    get_reel_basic_metrics,
    calculate_engagement_score,
)


def clean_value(value):
    value = str(value).strip()

    if value.lower() in ["", "nan", "none", "null"]:
        return ""

    # Fix pandas converting Facebook IDs into float-like / decimal-like strings
    # Example: 1293782798975525.0 → 1293782798975525
    # Example: 2152037468894511.2 → 2152037468894511
    if "." in value:
        left, right = value.split(".", 1)
        if left.isdigit() and right.isdigit():
            value = left

    return value

def extract_post_id_from_url(post_url):
    post_url = clean_value(post_url)

    if "facebook.com/" not in post_url:
        return ""

    return post_url.split("facebook.com/")[-1].strip()


def ensure_columns(memory):
    required_columns = {
        "likes": 0,
        "comments": 0,
        "shares": 0,
        "reel_likes": 0,
        "reel_comments": 0,
        "reel_views": 0,
        "engagement_score": 0,
        "analytics_updated_at": "",
    }

    for col, default in required_columns.items():
        if col not in memory.columns:
            memory[col] = default

    return memory


def main():
    log("AI Analytics worker started")

    if not ANALYTICS_ENABLED:
        log("AI Analytics skipped - disabled")
        return

    try:
        memory = pd.read_csv(ANALYTICS_MEMORY_FILE, dtype=str)
    except Exception as e:
        log(f"AI Analytics failed to read memory: {e}")
        raise SystemExit(1)

    if memory.empty:
        log("AI Analytics stopped - memory empty")
        return

    memory = ensure_columns(memory)

    latest_indexes = memory.tail(ANALYTICS_SCAN_LIMIT).index

    updated = 0

    for idx in latest_indexes:
        row = memory.loc[idx]

        post_url = clean_value(row.get("post_url", ""))
        post_id = extract_post_id_from_url(post_url)

        reel_id = clean_value(row.get("reel_id", ""))

        if post_id:
            log(f"Analytics scanning post: {post_id}")
            post_metrics = get_post_basic_metrics(post_id)

            memory.at[idx, "likes"] = post_metrics["likes"]
            memory.at[idx, "comments"] = post_metrics["comments"]
            memory.at[idx, "shares"] = post_metrics["shares"]

        if reel_id:
            log(f"Analytics scanning reel/video: {reel_id}")
            reel_metrics = get_reel_basic_metrics(reel_id)

            memory.at[idx, "reel_likes"] = reel_metrics["reel_likes"]
            memory.at[idx, "reel_comments"] = reel_metrics["reel_comments"]
            memory.at[idx, "reel_views"] = reel_metrics["reel_views"]

        memory.at[idx, "engagement_score"] = calculate_engagement_score(memory.loc[idx])
        memory.at[idx, "analytics_updated_at"] = str(pd.Timestamp.now())

        updated += 1

    memory.to_csv(ANALYTICS_MEMORY_FILE, index=False)

    log(f"AI Analytics completed. Rows updated: {updated}")


if __name__ == "__main__":
    main()
