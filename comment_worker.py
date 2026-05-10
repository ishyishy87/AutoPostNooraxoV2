import pandas as pd

from config import MEMORY_FILE
from modules.logger import log
from modules.comment_reply import process_post_comments


COMMENT_SCAN_LIMIT = 21   # 3 posts daily x 7 days = 21


def clean_value(value):
    value = str(value).strip()

    if value.lower() in ["", "nan", "none", "null"]:
        return ""

    return value


def extract_post_id_from_url(post_url):
    post_url = clean_value(post_url)

    if "facebook.com/" not in post_url:
        return ""

    return post_url.split("facebook.com/")[-1].strip()


def main():
    log("AI comment worker started")

    try:
        memory = pd.read_csv(MEMORY_FILE)
    except Exception as e:
        log(f"Comment worker failed to read memory: {e}")
        raise SystemExit(1)

    if memory.empty:
        log("Comment worker stopped - memory empty")
        return

    latest_rows = memory.tail(COMMENT_SCAN_LIMIT)

    processed_count = 0

    for _, row in latest_rows.iterrows():
        title = clean_value(row.get("product_id", ""))
        price = clean_value(row.get("price", ""))

        # ===== FACEBOOK POST COMMENTS =====

        post_url = clean_value(row.get("post_url", ""))
        post_id = extract_post_id_from_url(post_url)

        if post_id:
            log(f"Scanning post comments: {post_id}")
            process_post_comments(post_id, title, price)
            processed_count += 1

        # ===== FACEBOOK REEL / VIDEO COMMENTS =====

        reel_id = clean_value(row.get("reel_id", ""))

        if reel_id:
            log(f"Scanning reel/video comments: {reel_id}")
            process_post_comments(reel_id, title, price)
            processed_count += 1

    log(f"AI comment worker completed. Sources scanned: {processed_count}")


if __name__ == "__main__":
    main()
