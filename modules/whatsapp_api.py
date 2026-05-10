import requests

from config import (
    WHATSAPP_ALERT_ENABLED,
    WHATSAPP_TOKEN,
    WHATSAPP_PHONE_NUMBER_ID,
    WHATSAPP_TO_NUMBER,
)

from modules.logger import log


def send_whatsapp_message(message):
    if not WHATSAPP_ALERT_ENABLED:
        log("WhatsApp alert skipped - disabled")
        return None

    if not WHATSAPP_TOKEN:
        log("WhatsApp alert skipped - WHATSAPP_TOKEN missing")
        return None

    if not WHATSAPP_PHONE_NUMBER_ID:
        log("WhatsApp alert skipped - WHATSAPP_PHONE_NUMBER_ID missing")
        return None

    if not WHATSAPP_TO_NUMBER:
        log("WhatsApp alert skipped - WHATSAPP_TO_NUMBER missing")
        return None

    url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": WHATSAPP_TO_NUMBER,
        "type": "text",
        "text": {
            "preview_url": True,
            "body": message,
        },
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        data = r.json()

        if r.status_code in [200, 201] and "messages" in data:
            log(f"WhatsApp alert sent successfully: {data}")
        else:
            log(f"WhatsApp alert failed: HTTP {r.status_code} | {data}")

        return data

    except Exception as e:
        log(f"WhatsApp alert error: {e}")
        return None
