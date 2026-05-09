import pandas as pd
from modules.scoring import score_product

def select_product(df, memory, col_map):
    posted = set(memory["product_id"].astype(str)) if "product_id" in memory.columns else set()
    sku_col = col_map.get("sku")

    available = df.copy()
    if sku_col:
        available = df[~df[sku_col].astype(str).isin(posted)]

    if available.empty:
        available = df.copy()

    available["score"] = available.apply(lambda x: score_product(x, col_map), axis=1)

    top = available.sort_values("score", ascending=False)
    return top.sample(1).iloc[0]
