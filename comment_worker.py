import pandas as pd

from config import MEMORY_FILE
from modules.logger import log
from modules.comment_reply import process_post_comments


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

    latest_rows = memory.tail(5)

    for _, row in latest_rows.iterrows():
        post_url = str(row.get("post_url", ""))
        title = str(row.get("product_id", ""))
        price = str(row.get("price", ""))

        if "facebook.com/" not in post_url:
            continue

        post_id = post_url.split("facebook.com/")[-1].strip()

        process_post_comments(post_id, title, price)

    log("AI comment worker completed")


if __name__ == "__main__":
    main()
