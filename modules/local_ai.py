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


def generate_reel_scenes(title, price, score):
    category = detect_category(title)
    benefits = _roman_urdu_benefits(title, category)
    hook, hook_style = generate_hook(title, category, score)

    roman_hooks = [
        "Stop scrolling! Yeh deal dekhein",
        "Aap ke liye smart pick",
        "Daily use ke liye useful item",
        "Limited stock alert!",
        "Yeh product worth checking hai",
    ]

    scene_templates = [
        {
            "name": "cinematic_problem_solution",
            "scenes": [
                random.choice(roman_hooks),
                "Routine ko easy banaye",
                title,
                " • ".join(benefits[:3]),
                f"Rs {price} | Inbox to Order"
            ]
        },
        {
            "name": "premium_sales_pitch",
            "scenes": [
                "New arrival feel, smart price",
                "Quality aur value aik sath",
                title,
                random.choice(benefits),
                f"Cash on Delivery | Rs {price}"
            ]
        },
        {
            "name": "conversion_offer",
            "scenes": [
                "Aaj ka smart shopping pick",
                "Useful, practical, affordable",
                title,
                "Order before stock ends",
                f"Only Rs {price}"
            ]
        }
    ]

    selected = random.choice(scene_templates)
    meta = {
        "reel_style": selected["name"],
        "hook_style": hook_style,
        "category": category
    }

    return selected["scenes"], meta


def generate_auto_comment(title, price):
    comments = [
        f"Available now with Cash on Delivery. Inbox to order {title}.",
        f"Interested in {title}? Message us now for quick booking.",
        f"Price: Rs {price}. Inbox your city name to confirm delivery.",
        f"Order open now. Send message to book {title}.",
    ]
    return random.choice(comments)


def generate_voiceover_script(title, price, score):
    """
    Builds a Roman Urdu + English ecommerce voiceover script.
    The product title is preserved exactly as provided in products.csv.
    """
    category = detect_category(title)
    benefits = _roman_urdu_benefits(title, category)

    category_openers = {
        "tech": [
            "Agar aap daily tech routine ko easy banana chahte hain,",
            "Mobile aur gadgets ke liye smart upgrade chahiye?",
        ],
        "beauty": [
            "Apni daily self care routine ko thora aur better banayein,",
            "Fresh look aur simple care ke liye yeh pick dekhein,",
        ],
        "fashion": [
            "Apni style ko simple tareeqe se upgrade karein,",
            "Agar aap trendy aur practical choice dhoond rahe hain,",
        ],
        "kitchen": [
            "Kitchen ka kaam easy aur fast banana chahte hain?",
            "Daily kitchen routine ke liye yeh smart helper dekhein,",
        ],
        "home": [
            "Home setup ko neat aur smart banana chahte hain?",
            "Ghar ke daily use ke liye yeh practical pick hai,",
        ],
        "baby": [
            "Parents ke liye yeh aik useful daily pick hai,",
            "Kids aur family use ke liye yeh product check karein,",
        ],
        "fitness": [
            "Active lifestyle ke liye smart support chahiye?",
            "Workout aur daily routine ke liye yeh useful pick hai,",
        ],
        "general": [
            "Aap ke daily use ke liye aik smart product,",
            "Agar aap affordable aur useful item dhoond rahe hain,",
        ],
    }

    opener = random.choice(category_openers.get(category, category_openers["general"]))
    benefit_one = benefits[0] if benefits else "daily use ke liye practical"
    benefit_two = benefits[1] if len(benefits) > 1 else "easy to use"

    scripts = [
        f"{opener} try this: {title}. Is mein {benefit_one} aur {benefit_two} milta hai. Price sirf {price} rupees. Cash on Delivery available hai. Order karne ke liye abhi inbox karein.",
        f"Stop scrolling. Yeh {title} aap ke liye aik smart pick ho sakta hai. {benefit_one}, plus {benefit_two}. Sirf {price} rupees mein available. Inbox now to book your order.",
        f"Aaj ki useful deal: {title}. Yeh product {benefit_one} provide karta hai, aur daily routine mein kaafi helpful hai. Price only {price} rupees. Cash on Delivery ke sath order karein.",
    ]

    return random.choice(scripts)
