import os
import pandas as pd

from config import PRODUCTS_FILE, POST_ONCE_PER_DAY, ROLLBACK_IF_REEL_FAILS, AUTO_COMMENT_ENABLED, ACCESS_TOKEN, PAGE_ID
from modules.logger import log
from modules.storage import already_ran_today, mark_run, load_memory, save_memory
from modules.csv_engine import normalize_columns, map_columns, safe_get
from modules.scoring import score_product
from modules.pricing import adjust_price
from modules.product_selector import select_product
from modules.image_downloader import download_image
from modules.local_ai import generate_caption, generate_hashtags, generate_auto_comment
from modules.facebook_api import (
    upload_images, post_carousel, upload_reel_video,
    delete_facebook_object, create_comment
)
from modules.reel_builder import create_reel_video
import modules.music as music_state


def stop_failed(message):
    """Stop workflow with non-zero exit so GitHub does not show false success."""
    log(message)
    raise SystemExit(1)


def collect_product_images(df, product, pid, img, col_map):
    image_files = []

    handle_col = "url handle" if "url handle" in df.columns else None
    image_col = col_map.get("image")

    product_rows = pd.DataFrame()

    if handle_col:
        product_rows = df[df[handle_col] == product.get(handle_col)]

    if product_rows.empty and "sku" in df.columns:
        product_rows = df[df["sku"] == pid]

    if "image position" in df.columns and not product_rows.empty:
        product_rows = product_rows.sort_values(by="image position")

    image_urls = product_rows[image_col].dropna().unique().tolist() if image_col and not product_rows.empty else []

    log(f"Found {len(image_urls)} images")

    for i, url in enumerate(image_urls[:4]):
        f = download_image(str(url), f"{pid}_{i}")
        if f:
            image_files.append(f)

    if not image_files:
        f = download_image(img, pid)
        if f:
            image_files.append(f)

    return image_files


def validate_environment():
    if not ACCESS_TOKEN:
        stop_failed("Failed: ACCESS_TOKEN secret is missing. Add it in GitHub Repository Settings > Secrets and variables > Actions.")

    if not PAGE_ID:
        stop_failed("Failed: PAGE_ID secret is missing. Add it in GitHub Repository Settings > Secrets and variables > Actions.")

    if not os.path.exists(PRODUCTS_FILE):
        stop_failed(f"Failed: {PRODUCTS_FILE} not found in repository root.")

def cleanup_video_folder():
    """
    Delete generated reel/video files after successful publishing.
    """

    video_dir = "videos"

    if not os.path.exists(video_dir):
        return

    deleted = 0

    for file_name in os.listdir(video_dir):

        file_path = os.path.join(video_dir, file_name)

        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted += 1
                log(f"Deleted video file: {file_path}")

        except Exception as e:
            log(f"Video cleanup failed for {file_path}: {e}")

    log(f"Video cleanup completed. Deleted files: {deleted}")

def main():
    log("Automation started")

    validate_environment()

    POST_ONCE_PER_DAY = False
    if POST_ONCE_PER_DAY and already_ran_today():
        log("Skipped - already ran today. No new post created.")
        return

    # ===== STEP 1: PRODUCT SELECTION =====

    try:
        df = pd.read_csv(PRODUCTS_FILE)
    except Exception as e:
        stop_failed(f"Failed: Could not read {PRODUCTS_FILE}: {e}")

    if df.empty:
        stop_failed("Failed: products.csv is empty.")

    df = normalize_columns(df)

    memory = load_memory()
    col_map = map_columns(df)

    if "title" not in col_map:
        stop_failed("Failed: Product title column not found. Required column: title/product title/name/product_name")

    if "image" not in col_map:
        stop_failed("Failed: Product image column not found. Required column: image src/image/image_url/img/photo")

    product = select_product(df, memory, col_map)

    pid = str(safe_get(product, col_map, "sku")).strip()
    if not pid:
        pid = str(product.name)

    title = safe_get(product, col_map, "title", "No Title")  # TITLE STAYS EXACTLY AS CSV
    price = safe_get(product, col_map, "price", 0)
    img = safe_get(product, col_map, "image")

    score = score_product(product, col_map)
    final_price = adjust_price(price, score)

    image_files = collect_product_images(df, product, pid, img, col_map)

    if not image_files:
        stop_failed("Failed: No product images found/downloaded. Automation stopped.")

    log(f"Step 1 Completed: Product selected | Product ID: {pid} | Title: {title} | Score: {score}")

    # ===== STEP 2: LOCAL AI MARKETING CONTENT =====

    post_caption, caption_meta = generate_caption(title, final_price, score)
    post_hashtags, hashtag_style = generate_hashtags(title, caption_meta["category"])

    cap = post_caption + "\n\n" + post_hashtags

    reel_caption, _ = generate_caption(title, final_price, score)
    reel_hashtags, _ = generate_hashtags(title, caption_meta["category"])
    reel_caption = reel_caption + "\n\n" + reel_hashtags

    auto_comment_text = generate_auto_comment(title, final_price)

    log(
        "Step 2 Completed: Local AI content generated | "
        f"Category: {caption_meta['category']} | Hook: {caption_meta['hook_style']}"
    )

    # ===== STEP 3: PREPARE MEDIA =====

    image_ids = upload_images(image_files)
    log(f"Uploaded images: {len(image_ids)}")

    if not image_ids:
        stop_failed("Failed: No images uploaded to Facebook. Check ACCESS_TOKEN, PAGE_ID, and app permissions.")

    reel_video_path, reel_meta = create_reel_video(image_files, title, final_price, score)

    if not reel_video_path or not os.path.exists(reel_video_path):
        stop_failed("Failed: Reel video creation failed. Automation stopped.")

    log(f"Step 3 Completed: Facebook images uploaded and reel created | Reel style: {reel_meta.get('reel_style', '')}")

    # ===== STEP 4: PUBLISH POST + REEL =====

    result, post_url = post_carousel(image_ids, cap)
    post_id = result.get("id") if result else None

    if not post_id:
        stop_failed(f"Failed: Facebook carousel post failed: {result}")

    reel_result = upload_reel_video(reel_video_path, reel_caption)
    reel_id = reel_result.get("id") if reel_result else None

    if not reel_id:
        log(f"Failed: Reel upload failed: {reel_result}")

        if ROLLBACK_IF_REEL_FAILS:
            delete_facebook_object(post_id)
            log("Rollback completed: Carousel post deleted because reel failed")

        stop_failed("Failed: Reel upload failed after carousel post. Workflow stopped after rollback attempt.")

    if AUTO_COMMENT_ENABLED:
        create_comment(post_id, auto_comment_text)

    log("Step 4 Completed: Facebook post and reel published successfully")

    # ===== STEP 5: MEMORY UPDATE =====

    new_row = pd.DataFrame([{
        "product_id": pid,
        "status": "posted",
        "price": final_price,
        "post_url": post_url,
        "reel_id": reel_id,
        "likes": 0,
        "comments": 0,
        "shares": 0,
        "score": score,
        "category": caption_meta["category"],
        "caption_style": caption_meta["caption_style"],
        "hook_style": caption_meta["hook_style"],
        "hashtag_style": hashtag_style,
        "music_url": music_state.LAST_SELECTED_MUSIC_URL,
        "date": str(pd.Timestamp.now())
    }])

    memory = pd.concat([memory, new_row], ignore_index=True)
    save_memory(memory)

    mark_run()
    log("Step 5 Completed: Memory updated and run locked")

# ===== STEP 6: CLEANUP =====

    cleanup_video_folder()

    log("Step 6 Completed: Video folder cleaned")

    log("Automation finished successfully")
    


if __name__ == "__main__":
    main()
