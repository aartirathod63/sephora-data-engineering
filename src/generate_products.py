import csv
import random
from pathlib import Path


random.seed(42)


# =========================================================
# Product catalog configuration
# =========================================================

PRODUCT_TEMPLATES = [
    # Makeup
    ("Makeup", "Foundation", [
        "Liquid Foundation",
        "Hydrating Foundation",
        "Full Coverage Foundation",
        "Radiant Foundation",
    ]),
    ("Makeup", "Concealer", [
        "Liquid Concealer",
        "Brightening Concealer",
        "Full Coverage Concealer",
    ]),
    ("Makeup", "Blush", [
        "Powder Blush",
        "Liquid Blush",
        "Cream Blush",
    ]),
    ("Makeup", "Mascara", [
        "Volumizing Mascara",
        "Lengthening Mascara",
        "Waterproof Mascara",
    ]),
    ("Makeup", "Lipstick", [
        "Matte Lipstick",
        "Hydrating Lipstick",
        "Satin Lipstick",
    ]),
    ("Makeup", "Lip Gloss", [
        "Shimmer Lip Gloss",
        "Plumping Lip Gloss",
        "Hydrating Lip Gloss",
    ]),
    ("Makeup", "Lip Tint", [
        "Juicy Lip Tint",
        "Water Lip Tint",
        "Lip & Cheek Tint",
    ]),
    ("Makeup", "Eyeshadow", [
        "Eyeshadow Palette",
        "Mini Eyeshadow Palette",
        "Shimmer Eyeshadow",
    ]),

    # Skincare
    ("Skincare", "Cleanser", [
        "Gentle Cleanser",
        "Foaming Cleanser",
        "Hydrating Cleanser",
    ]),
    ("Skincare", "Moisturizer", [
        "Hydrating Moisturizer",
        "Gel Moisturizer",
        "Barrier Cream",
    ]),
    ("Skincare", "Serum", [
        "Vitamin C Serum",
        "Hyaluronic Acid Serum",
        "Niacinamide Serum",
        "Retinol Serum",
    ]),
    ("Skincare", "Face Mask", [
        "Clay Face Mask",
        "Hydrating Face Mask",
        "Overnight Face Mask",
    ]),
    ("Skincare", "Sunscreen", [
        "SPF 30 Sunscreen",
        "SPF 50 Sunscreen",
        "Invisible Sunscreen",
    ]),
    ("Skincare", "Eye Cream", [
        "Brightening Eye Cream",
        "Hydrating Eye Cream",
    ]),

    # Haircare
    ("Haircare", "Shampoo", [
        "Repair Shampoo",
        "Hydrating Shampoo",
        "Volume Shampoo",
    ]),
    ("Haircare", "Conditioner", [
        "Repair Conditioner",
        "Hydrating Conditioner",
        "Smoothing Conditioner",
    ]),
    ("Haircare", "Hair Mask", [
        "Repair Hair Mask",
        "Nourishing Hair Mask",
    ]),
    ("Haircare", "Hair Oil", [
        "Nourishing Hair Oil",
        "Scalp Treatment Oil",
    ]),
    ("Haircare", "Hair Serum", [
        "Anti-Frizz Hair Serum",
        "Smoothing Hair Serum",
    ]),

    # Fragrance
    ("Fragrance", "Eau de Parfum", [
        "Signature Eau de Parfum",
        "Floral Eau de Parfum",
        "Woody Eau de Parfum",
    ]),
    ("Fragrance", "Eau de Toilette", [
        "Fresh Eau de Toilette",
        "Citrus Eau de Toilette",
    ]),
    ("Fragrance", "Body Mist", [
        "Fragrance Body Mist",
        "Shimmer Body Mist",
    ]),

    # Bath & Body
    ("Bath & Body", "Body Lotion", [
        "Hydrating Body Lotion",
        "Nourishing Body Lotion",
    ]),
    ("Bath & Body", "Body Wash", [
        "Creamy Body Wash",
        "Refreshing Body Wash",
    ]),
    ("Bath & Body", "Body Scrub", [
        "Exfoliating Body Scrub",
        "Sugar Body Scrub",
    ]),
    ("Bath & Body", "Hand Cream", [
        "Nourishing Hand Cream",
        "Hydrating Hand Cream",
    ]),

    # Tools
    ("Tools & Brushes", "Makeup Brush", [
        "Foundation Brush",
        "Blush Brush",
        "Eyeshadow Brush",
        "Powder Brush",
    ]),
    ("Tools & Brushes", "Beauty Sponge", [
        "Makeup Sponge",
        "Blending Sponge",
    ]),
    ("Tools & Brushes", "Eyelash Curler", [
        "Professional Eyelash Curler",
    ]),

    # Nails
    ("Nails", "Nail Polish", [
        "Long Wear Nail Polish",
        "Gel Effect Nail Polish",
    ]),
    ("Nails", "Nail Care", [
        "Nail Strengthener",
        "Cuticle Oil",
    ]),

    # Accessories
    ("Beauty Accessories", "Travel Case", [
        "Beauty Travel Case",
        "Makeup Organizer",
    ]),
    ("Beauty Accessories", "Mirror", [
        "Compact Beauty Mirror",
        "LED Beauty Mirror",
    ]),
]


BRANDS = [
    "Sephora Collection",
    "NARS",
    "Benefit Cosmetics",
    "Laneige",
    "Clinique",
    "The Ordinary",
    "Kérastase",
    "Sol de Janeiro",
    "Fenty Beauty",
    "Huda Beauty",
    "MAC",
    "Too Faced",
    "Rare Beauty",
    "Estée Lauder",
    "Dior",
]


# Approximate INR price ranges by category.
# These are synthetic ranges modeled on premium beauty retail,
# not claimed to be exact live Sephora India prices.

PRICE_RANGES = {
    "Makeup": (900, 6500),
    "Skincare": (800, 7000),
    "Haircare": (1000, 6500),
    "Fragrance": (2500, 15000),
    "Bath & Body": (700, 4500),
    "Tools & Brushes": (500, 3500),
    "Nails": (500, 2200),
    "Beauty Accessories": (500, 3000),
}


SIZE_OPTIONS = [
    "5 ml",
    "7 ml",
    "10 ml",
    "15 ml",
    "30 ml",
    "50 ml",
    "75 ml",
    "100 ml",
    "150 ml",
    "200 ml",
]


# =========================================================
# Generate products
# =========================================================

def generate_products(count=150):

    output_path = Path(
        "data/raw/products.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "product_id",
        "product_name",
        "brand",
        "category",
        "subcategory",
        "mrp_inr",
        "rating",
        "review_count",
        "size",
        "stock_quantity",
    ]

    products = []

    product_number = 1001

    while len(products) < count:

        category, subcategory, names = random.choice(
            PRODUCT_TEMPLATES
        )

        name = random.choice(names)
        brand = random.choice(BRANDS)

        product_name = f"{brand} {name}"

        min_price, max_price = PRICE_RANGES[
            category
        ]

        mrp = random.randrange(
            min_price,
            max_price + 1,
            50
        )

        rating = round(
            random.uniform(3.8, 4.9),
            1
        )

        review_count = random.randint(
            25,
            5000
        )

        stock_quantity = random.randint(
            20,
            500
        )

        product = {
            "product_id": f"P{product_number}",
            "product_name": product_name,
            "brand": brand,
            "category": category,
            "subcategory": subcategory,
            "mrp_inr": mrp,
            "rating": rating,
            "review_count": review_count,
            "size": random.choice(SIZE_OPTIONS),
            "stock_quantity": stock_quantity,
        }

        products.append(product)

        product_number += 1

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(products)

    print(
        f"Created {output_path}"
    )

    print(
        f"Products generated: {len(products)}"
    )


if __name__ == "__main__":
    generate_products()