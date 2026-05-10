import os
import urllib.parse
import pandas as pd

from config import (
    BUSINESS_WHATSAPP_NUMBER,
    LEAD_MEMORY_FILE,
    WHATSAPP_LEAD_FUNNEL_ENABLED,
    LEAD_TRIGGER_WORDS,
)

from modules.logger import log


def is_lead_comment(comment_text):
    """
    Detect if comment has buyer intent.
    """

    if not WHATSAPP_LEAD_FUNNEL_ENABLED:
        return False

    text = str(comment_text).lower()

    return any(word in text for word in LEAD_TRIGGER_WORDS)


def build_whatsapp_order_link(title="", price="", source="facebook_comment"):
    """
    Build WhatsApp click-to-chat link with pre-filled message.
    """

    msg = f"""
Assalam o Alaikum,
I want to order this product.

Product: {title}
Price: Rs {price}
Source: {source}
""".strip()

    encoded_msg = urllib.parse.quote(msg)

    return f"https://wa.me/{BUSINESS_WHATSAPP_NUMBER}?text={encoded_msg}"


def generate_lead_reply(comment_text, title="", price=""):
    """
    Generate AI-style Roman Urdu reply with WhatsApp order link.
    """

    wa_link = build_whatsapp_order_link(
        title=title,
        price=price,
        source="facebook_comment"
    )

    text = str(comment_text).lower()

    if any(x in text for x in ["price", "rate", "kitna"]):
        return f"Ji price Rs {price} hai 😊 Order confirm karne ke liye WhatsApp karein: {wa_link}"

    if any(x in text for x in ["available", "stock"]):
        return f"Ji available hai 😊 Fast booking ke liye WhatsApp par message karein: {wa_link}"

    if any(x in text for x in ["cod", "cash", "delivery"]):
        return f"Ji Cash on Delivery available hai 🚚 Order ke liye WhatsApp karein: {wa_link}"

    if any(x in text for x in ["order", "book", "buy", "interested", "want", "chahiye"]):
        return f"Zaroor 😊 Order confirm karne ke liye WhatsApp link open karein: {wa_link}"

    return f"Details aur order ke liye WhatsApp karein 😊 {wa_link}"


def load_lead_memory():
    if not os.path.exists(LEAD_MEMORY_FILE):
        df = pd.DataFrame(columns=[
            "comment_id",
            "post_id",
            "title",
            "price",
            "whatsapp_link",
            "date"
        ])
        df.to_csv(LEAD_MEMORY_FILE, index=False)
        return df

    return pd.read_csv(LEAD_MEMORY_FILE)


def save_lead_memory(df):
    df.to_csv(LEAD_MEMORY_FILE, index=False)


def save_lead(comment_id, post_id, title, price, whatsapp_link):
    memory = load_lead_memory()

    if comment_id in set(memory["comment_id"].astype(str)):
        return

    row = pd.DataFrame([{
        "comment_id": comment_id,
        "post_id": post_id,
        "title": title,
        "price": price,
        "whatsapp_link": whatsapp_link,
        "date": str(pd.Timestamp.now())
    }])

    memory = pd.concat([memory, row], ignore_index=True)
    save_lead_memory(memory)

    log(f"Lead saved from comment: {comment_id}")
