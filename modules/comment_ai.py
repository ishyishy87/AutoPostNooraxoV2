import random
from modules.lead_funnel import is_lead_comment, generate_lead_reply

def detect_comment_intent(comment_text):
    text = str(comment_text).lower()

    if any(x in text for x in ["price", "rate", "kitna", "price?", "rs", "pkr"]):
        return "price"

    if any(x in text for x in ["available", "stock", "moujood", "hai?", "mil jay ga"]):
        return "availability"

    if any(x in text for x in ["cod", "cash", "delivery", "deliver", "parcel"]):
        return "delivery"

    if any(x in text for x in ["order", "book", "buy", "want", "chahiye", "inbox"]):
        return "order"

    if any(x in text for x in ["location", "city", "karachi", "lahore", "islamabad", "peshawar"]):
        return "location"

    return "general"


def generate_comment_reply(comment_text, title="", price=""):

    if is_lead_comment(comment_text):
        return generate_lead_reply(comment_text, title, price)
    intent = detect_comment_intent(comment_text)

    replies = {
        "price": [
            f"Ji price Rs {price} hai. Order ke liye inbox kar dein 😊",
            f"Price Rs {price} hai. Cash on Delivery available hai 😊",
            f"Ji Rs {price}. Booking ke liye inbox karein 😊",
        ],
        "availability": [
            "Ji available hai. Order ke liye inbox kar dein 😊",
            "Available hai. Cash on Delivery bhi available hai 😊",
            "Ji stock available hai. Apna city name inbox kar dein 😊",
        ],
        "delivery": [
            "Ji Cash on Delivery available hai. Apna city inbox kar dein 😊",
            "Delivery available hai. Booking ke liye inbox karein 😊",
            "COD available hai. Order confirm karne ke liye message karein 😊",
        ],
        "order": [
            "Ji order ke liye inbox kar dein. Team aapko guide kar degi 😊",
            "Booking ke liye inbox karein. Cash on Delivery available hai 😊",
            "Ji inbox karein, order confirm kar dete hain 😊",
        ],
        "location": [
            "Delivery different cities mein available hai. Apna city inbox kar dein 😊",
            "Apna city name inbox karein, delivery confirm kar dete hain 😊",
            "Ji delivery check karne ke liye city name inbox karein 😊",
        ],
        "general": [
            "Details ke liye inbox kar dein 😊",
            "Ji available hai. More details ke liye inbox karein 😊",
            "Order aur details ke liye message kar dein 😊",
        ],
    }

    return random.choice(replies[intent])
