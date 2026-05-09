import re
import random

# =====================================================
# LOCAL AI MARKETING ENGINE
# No OpenAI API required.
# Title is never rewritten. It is used exactly as product.csv provides it.
# =====================================================

CATEGORY_KEYWORDS = {
    "tech": ["usb", "charger", "mobile", "phone", "speaker", "earbuds", "bluetooth", "led", "cable", "power", "watch", "smart"],
    "beauty": ["cream", "serum", "skin", "face", "makeup", "beauty", "hair", "lotion", "mask"],
    "fashion": ["shirt", "dress", "watch", "shoes", "bag", "wallet", "hoodie", "jeans", "fashion", "sandal"],
    "kitchen": ["kitchen", "knife", "cutter", "pan", "cook", "bottle", "mug", "spoon", "holder"],
    "home": ["lamp", "light", "home", "decor", "organizer", "cleaner", "storage", "rack"],
    "baby": ["baby", "kids", "toy", "child", "school", "student"],
    "fitness": ["gym", "fitness", "exercise", "protein", "yoga", "sports"],
}

CATEGORY_HASHTAGS = {
    "tech": ["#TechDeals", "#Gadgets", "#SmartShopping", "#MobileAccessories", "#Electronics"],
    "beauty": ["#BeautyFinds", "#GlowUp", "#Skincare", "#BeautyDeals", "#SelfCare"],
    "fashion": ["#FashionFinds", "#StyleDeals", "#OOTD", "#TrendyStyle", "#FashionSale"],
    "kitchen": ["#KitchenEssentials", "#HomeKitchen", "#SmartKitchen", "#KitchenTools"],
    "home": ["#HomeEssentials", "#HomeDecor", "#SmartHome", "#HomeFinds"],
    "baby": ["#BabyCare", "#KidsProducts", "#MomLife", "#BabyEssentials"],
    "fitness": ["#FitnessGear", "#WorkoutEssentials", "#GymLife", "#HealthyLifestyle"],
    "general": ["#ShopNow", "#OnlineShopping", "#Pakistan", "#Deals", "#Sale"]
}

def detect_category(title):
    text = str(title).lower()
    for category, words in CATEGORY_KEYWORDS.items():
        if any(w in text for w in words):
            return category
    return "general"

def extract_keywords(title):
    stopwords = {
        "and", "for", "with", "the", "new", "best", "pack", "pcs", "piece",
        "original", "premium", "high", "quality", "sale"
    }
    words = re.findall(r"[a-zA-Z0-9]+", str(title).lower())
    return [w for w in words if len(w) > 3 and w not in stopwords][:6]

def extract_benefits(title, category):
    text = str(title).lower()
    benefits = []

    benefit_rules = [
        (["wireless", "bluetooth"], "Wireless convenience"),
        (["fast", "quick"], "Fast performance"),
        (["portable", "mini"], "Easy to carry"),
        (["led", "light"], "Bright and stylish"),
        (["durable", "steel", "metal"], "Long-lasting quality"),
        (["water", "waterproof"], "Water-resistant design"),
        (["rechargeable", "battery"], "Rechargeable use"),
        (["organizer", "storage", "rack"], "Keeps things organized"),
        (["beauty", "skin", "cream", "serum"], "Daily self-care support"),
        (["kitchen", "cutter", "knife"], "Makes kitchen work easier"),
    ]

    for keys, benefit in benefit_rules:
        if any(k in text for k in keys):
            benefits.append(benefit)

    category_defaults = {
        "tech": ["Useful daily gadget", "Smart choice for everyday use", "Modern and practical"],
        "beauty": ["Enhances daily routine", "Good for self-care", "Fresh look and feel"],
        "fashion": ["Trendy daily style", "Easy to match", "Stylish appearance"],
        "kitchen": ["Saves time in kitchen", "Practical home helper", "Useful for daily cooking"],
        "home": ["Improves home setup", "Useful daily essential", "Neat and practical"],
        "baby": ["Helpful for parents", "Useful for kids", "Daily family essential"],
        "fitness": ["Supports active lifestyle", "Useful workout companion", "Motivating daily gear"],
        "general": ["Useful daily product", "Practical and affordable", "Easy choice for home use"],
    }

    for b in category_defaults.get(category, category_defaults["general"]):
        if b not in benefits:
            benefits.append(b)

    return benefits[:4]

def choose_hook_style(score):
    if score >= 70:
        return random.choice(["social_proof", "hot_pick", "fast_move"])
    if score >= 40:
        return random.choice(["problem_solution", "curiosity", "value"])
    return random.choice(["urgency", "discovery", "budget"])

def generate_hook(title, category, score):
    style = choose_hook_style(score)

    hooks = {
        "social_proof": [
            "People are loving this pick!",
            "This product is getting attention!",
            "A smart choice for daily use!"
        ],
        "hot_pick": [
            "Hot product alert!",
            "This one deserves a look!",
            "Trending pick for today!"
        ],
        "fast_move": [
            "Stock can move fast!",
            "Do not miss this deal!",
            "Grab it before it is gone!"
        ],
        "problem_solution": [
            "Need an easier daily solution?",
            "Small product, big daily use!",
            "Make your routine simpler today!"
        ],
        "curiosity": [
            "Most people ignore this useful item!",
            "You may need this more than you think!",
            "This simple item can be very useful!"
        ],
        "value": [
            "Useful product at a smart price!",
            "Practical, affordable, and worth checking!",
            "A budget-friendly daily essential!"
        ],
        "urgency": [
            "Limited offer for today!",
            "Available now while stock lasts!",
            "Order before stock runs out!"
        ],
        "discovery": [
            "New useful find for your home!",
            "Daily-use product worth trying!",
            "A simple product with real value!"
        ],
        "budget": [
            "Smart shopping starts here!",
            "Good value without overthinking!",
            "Affordable pick for everyday use!"
        ],
    }

    return random.choice(hooks[style]), style

def generate_caption(title, price, score):
    category = detect_category(title)
    benefits = extract_benefits(title, category)
    hook, hook_style = generate_hook(title, category, score)

    opening_lines = [
        "Upgrade your daily routine with this useful find.",
        "A practical product selected for smart shoppers.",
        "Simple, useful, and ready to order.",
        "Make everyday life easier with this pick.",
    ]

    ctas = [
        "📩 Inbox now to place your order",
        "💬 Message us for quick booking",
        "🛒 Order now via inbox",
        "📦 Book yours today — Cash on Delivery available",
    ]

    benefit_text = "\n".join([f"✅ {b}" for b in benefits[:3]])

    caption_text = f"""
{hook}

🔥 {title}
💸 Price: Rs {price}

{random.choice(opening_lines)}

{benefit_text}

🚚 Cash on Delivery Available
{random.choice(ctas)}
""".strip()

    meta = {
        "category": category,
        "hook_style": hook_style,
        "caption_style": "local_ai_benefit_caption"
    }

    return caption_text, meta

def generate_hashtags(title, category=None):
    category = category or detect_category(title)
    keywords = extract_keywords(title)

    common = [
        "#ShopNow", "#OnlineShopping", "#Pakistan", "#Deals", "#Sale",
        "#CashOnDelivery", "#TrendingProducts", "#DailyUse", "#BestFinds",
        "#AffordableShopping"
    ]

    category_tags = CATEGORY_HASHTAGS.get(category, CATEGORY_HASHTAGS["general"])

    dynamic_tags = []
    for word in keywords:
        tag = "#" + re.sub(r"[^a-zA-Z0-9]", "", word.title())
        if len(tag) > 2:
            dynamic_tags.append(tag)

    final = list(set(random.sample(common, min(6, len(common))) + random.sample(category_tags, min(3, len(category_tags))) + dynamic_tags[:4]))
    random.shuffle(final)

    return " ".join(final[:13]), "category_dynamic"

def _roman_urdu_benefits(title, category):
    text = str(title).lower()
    benefits = []

    rules = [
        (["wireless", "bluetooth"], "wireless comfort"),
        (["fast", "quick"], "fast performance"),
        (["portable", "mini"], "easy carry design"),
        (["led", "light"], "bright stylish look"),
        (["durable", "steel", "metal"], "strong build quality"),
        (["water", "waterproof"], "water resistant support"),
        (["rechargeable", "battery"], "long battery support"),
        (["organizer", "storage", "rack"], "clean organized setup"),
        (["beauty", "skin", "cream", "serum"], "daily self care support"),
        (["kitchen", "cutter", "knife"], "kitchen ka kaam easy"),
        (["charger", "cable", "usb"], "charging routine easy"),
        (["speaker", "earbuds", "sound"], "clear sound experience"),
    ]

    for keys, benefit in rules:
        if any(k in text for k in keys):
            benefits.append(benefit)

    defaults = {
        "tech": ["daily use ke liye smart choice", "modern aur practical", "easy to use"],
        "beauty": ["daily routine ke liye useful", "fresh look and feel", "self care ke liye acha"],
        "fashion": ["style ko upgrade kare", "daily wear ke liye trendy", "premium look"],
        "kitchen": ["kitchen work ko easy banaye", "time saving helper", "daily cooking support"],
        "home": ["home setup ko neat banaye", "daily use essential", "smart home helper"],
        "baby": ["parents ke liye helpful", "kids ke liye useful", "family essential"],
        "fitness": ["active lifestyle support", "workout routine ke liye useful", "daily motivation"],
        "general": ["daily use ke liye practical", "affordable smart pick", "ghar ke liye useful"],
    }

    for b in defaults.get(category, defaults["general"]):
        if b not in benefits:
            benefits.append(b)

    return benefits[:4]


def _short_benefit_for_reel(title, category):
    """
    One very short product benefit for clean, product-first reels.
    Text overlay must stay minimal; voiceover explains the detail.
    """

    benefits = _roman_urdu_benefits(title, category)
    preferred = {
        "tech": ["Smart Gadget", "Easy Use", "Daily Tech"],
        "beauty": ["Soft Glow", "Self Care", "Fresh Look"],
        "fashion": ["Premium Look", "Trendy Style", "Smart Style"],
        "kitchen": ["Kitchen Helper", "Easy Cooking", "Time Saver"],
        "home": ["Home Helper", "Neat Setup", "Daily Essential"],
        "baby": ["Kids Pick", "Family Use", "Daily Care"],
        "fitness": ["Active Life", "Workout Pick", "Stay Fit"],
        "general": ["Daily Use", "Smart Pick", "Best Value"],
    }

    # Prefer category-specific short phrases.
    if category in preferred:
        return random.choice(preferred[category])

    # Fallback: shorten extracted benefit.
    if benefits:
        words = benefits[0].split()[:3]
        return " ".join(words).title()

    return "Smart Pick"


def generate_reel_scenes(title, price, score):
    """
    Voice-first reel scene engine.
    Keep reel text very short so the product stays dominant.
    Title is NOT rewritten; it is intentionally not placed as a full overlay on every scene.
    """

    category = detect_category(title)
    hook, hook_style = generate_hook(title, category, score)
    short_benefit = _short_benefit_for_reel(title, category)

    first_scene_options = [
        "Aaj Ki Pick",
        "Smart Pick",
        "New Find",
        "Worth It",
        "Dekhein Zara",
    ]

    cta_options = [
        "Inbox Now",
        "Order Now",
        "COD Available",
        "Limited Stock",
    ]

    scenes = [
        random.choice(first_scene_options),
        "Premium Look",
        short_benefit,
        f"Rs {price}",
        random.choice(cta_options),
    ]

    meta = {
        "reel_style": "voice_first_product_focused_minimal_text",
        "hook_style": hook_style,
        "category": category,
        "scene_count": len(scenes),
    }

    return scenes, meta


def generate_auto_comment(title, price):
    comments = [
        f"Available now with Cash on Delivery. Inbox to order {title}.",
        f"Interested in {title}? Message us now for quick booking.",
        f"Price: Rs {price}. Inbox your city name to confirm delivery.",
        f"Order open now. Send message to book {title}.",
    ]
    return random.choice(comments)


def generate_voiceover_script(title, price, score=None):
    """
    ElevenLabs-ready Roman Urdu + English ecommerce voice script.
    Short, conversational, female-ad style.
    Title remains exactly from products.csv.
    """

    category = detect_category(title)
    benefits = _roman_urdu_benefits(title, category)

    b1 = benefits[0] if len(benefits) > 0 else "daily use ke liye practical"
    b2 = benefits[1] if len(benefits) > 1 else "premium look aur smart value"

    openers = [
        "Assalam o Alaikum!",
        "Aaj ki smart pick dekhein.",
        "Yeh product aap ke kaam aa sakta hai.",
    ]

    soft_hooks = [
        "Agar aap kuch useful aur stylish dhoond rahe hain,",
        "Agar aap daily use ke liye smart choice chahte hain,",
        "Agar aap quality ke sath value bhi chahte hain,",
    ]

    product_lines = [
        f"to yeh {title} aap ke liye acha option ho sakta hai.",
        f"to {title} zaroor check karein.",
        f"to yeh {title} aap ki routine ko easy bana sakta hai.",
    ]

    closing_lines = [
        "Cash on Delivery available hai.",
        "Order ke liye abhi inbox karein.",
        "Stock limited hai, is liye jaldi message karein.",
    ]

    # Extra punctuation and line breaks help ElevenLabs create natural pauses.
    return f"""
{random.choice(openers)}

{random.choice(soft_hooks)}
{random.choice(product_lines)}

Is mein milta hai... {b1}.
Aur sath hi... {b2}.

Price sirf Rs {price}.

{random.choice(closing_lines)}
""".strip()
