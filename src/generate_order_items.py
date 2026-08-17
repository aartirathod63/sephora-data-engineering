import csv
import random
from pathlib import Path


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

random.seed(42)

MIN_ITEMS_PER_ORDER = 1
MAX_ITEMS_PER_ORDER = 4


# ---------------------------------------------------------
# CSV loader
# ---------------------------------------------------------

def load_csv(file_path):
    """
    Load a CSV file into a list of dictionaries.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return list(
            csv.DictReader(file)
        )


# ---------------------------------------------------------
# Discount logic
# ---------------------------------------------------------

def choose_discount():
    """
    Generate a realistic retail discount.

    Most products receive small discounts,
    while some promotional orders receive
    larger discounts.
    """

    return random.choices(
        [
            0,
            5,
            10,
            15,
            20,
            25,
            30
        ],
        weights=[
            25,
            15,
            25,
            15,
            10,
            7,
            3
        ],
        k=1
    )[0]


# ---------------------------------------------------------
# Main generator
# ---------------------------------------------------------

def generate_order_items():

    orders_path = (
        "data/raw/orders.csv"
    )

    products_path = (
        "data/raw/products.csv"
    )

    output_path = Path(
        "data/raw/order_items.csv"
    )

    # -----------------------------------------------------
    # Load master/transaction data
    # -----------------------------------------------------

    orders = load_csv(
        orders_path
    )

    products = load_csv(
        products_path
    )

    # -----------------------------------------------------
    # Convert product prices
    # -----------------------------------------------------

    products_data = []

    for product in products:

        products_data.append(
            {
                "product_id": product["product_id"],
                "mrp_inr": float(product["mrp_inr"])
            }
        )

    # -----------------------------------------------------
    # Output configuration
    # -----------------------------------------------------

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price_inr",
        "discount_percent",
        "discount_amount_inr",
        "line_total_inr",
    ]

    # -----------------------------------------------------
    # Generate order items
    # -----------------------------------------------------

    item_counter = 1

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

        for order in orders:

            order_id = order["order_id"]

            number_of_items = random.randint(
                MIN_ITEMS_PER_ORDER,
                MAX_ITEMS_PER_ORDER
            )

            # Select unique products within the order
            selected_products = random.sample(
                products_data,
                number_of_items
            )

            for product in selected_products:

                product_id = product[
                    "product_id"
                ]

                mrp = product[
                    "mrp_inr"
                ]

                quantity = random.randint(
                    1,
                    3
                )

                discount_percent = choose_discount()

                discount_amount = (
                    mrp
                    * quantity
                    * discount_percent
                    / 100
                )

                line_total = (
                    mrp * quantity
                    - discount_amount
                )

                writer.writerow(
                    {
                        "order_item_id": (
                            f"OI{item_counter:07d}"
                        ),
                        "order_id": order_id,
                        "product_id": product_id,
                        "quantity": quantity,
                        "unit_price_inr": round(
                            mrp,
                            2
                        ),
                        "discount_percent": (
                            discount_percent
                        ),
                        "discount_amount_inr": round(
                            discount_amount,
                            2
                        ),
                        "line_total_inr": round(
                            line_total,
                            2
                        ),
                    }
                )

                item_counter += 1

    print(
        f"Created {output_path}"
    )

    print(
        f"Order items generated: "
        f"{item_counter - 1}"
    )


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    generate_order_items()