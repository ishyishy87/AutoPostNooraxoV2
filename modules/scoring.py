import re
from modules.csv_engine import safe_get

def score_product(row, col_map):
    score = 0
    title = str(safe_get(row, col_map, "title", "")).lower()

    if any(x in title for x in ["new", "hot", "sale", "best", "premium", "smart", "wireless"]):
        score += 10

    if safe_get(row, col_map, "image"):
        score += 5

    try:
        price = float(re.sub(r"[^\d.]", "", str(safe_get(row, col_map, "price", 0))) or 0)
        if price < 50:
            score += 10
        elif price < 100:
            score += 5
        elif price < 1000:
            score += 3
    except Exception:
        pass

    return score
