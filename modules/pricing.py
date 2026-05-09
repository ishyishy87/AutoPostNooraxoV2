import re

def profit_optimizer(price, score):
    base = float(re.sub(r"[^\d.]", "", str(price)) or 0)

    multiplier = 1.5

    if score >= 80:
        multiplier += 0.35
        strategy = "WINNER_SCALE"
    elif score >= 60:
        multiplier += 0.25
        strategy = "STRONG_PROFIT"
    elif score >= 40:
        multiplier += 0.15
        strategy = "BALANCED_GROWTH"
    elif score >= 25:
        multiplier += 0.30
        strategy = "RISK_PROFIT"
    else:
        multiplier += 0.45
        strategy = "MAX_MARGIN_LOW_DEMAND"

    multiplier = max(1.2, min(multiplier, 2.5))
    return base * multiplier, strategy

def adjust_price(price, score):
    final_price, _ = profit_optimizer(price, score)
    final_price = int(final_price)

    if final_price > 100:
        final_price = (final_price // 100) * 100 - 1
    elif final_price > 10:
        final_price = (final_price // 10) * 10 - 1

    return max(final_price, 1)
