import os
import pandas as pd
from datetime import datetime
from config import MEMORY_FILE, RUN_LOCK_FILE

MEMORY_COLUMNS = [
    "product_id", "status", "price", "post_url", "reel_id",
    "likes", "comments", "shares", "score", "category",
    "caption_style", "hook_style", "hashtag_style", "music_url", "date"
]

def already_ran_today():
    if not os.path.exists(RUN_LOCK_FILE):
        return False
    return open(RUN_LOCK_FILE).read().strip() == str(datetime.now().date())

def mark_run():
    with open(RUN_LOCK_FILE, "w", encoding="utf-8") as f:
        f.write(str(datetime.now().date()))

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        df = pd.DataFrame(columns=MEMORY_COLUMNS)
        df.to_csv(MEMORY_FILE, index=False)
        return df

    df = pd.read_csv(MEMORY_FILE)

    for col in MEMORY_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    return df

def save_memory(df):
    df.to_csv(MEMORY_FILE, index=False)
