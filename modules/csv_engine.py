import pandas as pd

def normalize_columns(df):
    df.columns = df.columns.str.strip().str.lower()
    return df

def map_columns(df):
    mapping = {}
    for col in df.columns:
        if col in ["title", "product title", "name", "product_name"]:
            mapping["title"] = col
        elif col in ["price", "cost", "amount", "sale price"]:
            mapping["price"] = col
        elif col in ["sku", "id", "product id", "product_id"]:
            mapping["sku"] = col
        elif col in ["image src", "image", "image_url", "img", "photo"]:
            mapping["image"] = col
    return mapping

def safe_get(row, col_map, key, default=""):
    col = col_map.get(key)
    if not col:
        return default
    val = row.get(col, default)
    if pd.isna(val):
        return default
    return val
