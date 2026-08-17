import csv
import random
from pathlib import Path
from datetime import date, timedelta


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

random.seed(42)

NUMBER_OF_ORDERS = 50000


# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------

def load_csv(file_path):
    """
    Load a CSV file and return a list of dictionaries.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return list(
            csv.DictReader(file)
        )


def random_order_date():
    """
    Generate an order date within the last 2 years.
    """

    days_ago = random.randint(
        0,
        730
    )

    return (
        date.today()
        - timedelta(days=days_ago)
    )


def choose_channel():
    """
    Simulate online vs physical-store purchases.
    """

    return random.choices(
        [
            "Online",
            "Physical Store"
        ],
        weights=[
            55,
            45
        ],
        k=1
    )[0]


def choose_payment_method():
    """
    Simulate common Indian payment methods.
    """

    return random.choices(
        [
            "UPI",
            "Credit Card",
            "Debit Card",
            "Net Banking",
            "Wallet"
        ],
        weights=[
            45,
            25,
            15,
            10,
            5
        ],
        k=1
    )[0]


def choose_order_status():
    """
    Simulate realistic order outcomes.
    """

    return random.choices(
        [
            "Completed",
            "Cancelled",
            "Returned"
        ],
        weights=[
            90,
            6,
            4
        ],
        k=1
    )[0]


# ---------------------------------------------------------
# Main order generator
# ---------------------------------------------------------

def generate_orders():

    customers_path = (
        "data/raw/customers.csv"
    )

    stores_path = (
        "data/raw/stores.csv"
    )

    output_path = Path(
        "data/raw/orders.csv"
    )

    # -----------------------------------------------------
    # Load master data
    # -----------------------------------------------------

    customers = load_csv(
        customers_path
    )

    stores = load_csv(
        stores_path
    )

    customer_ids = [
        customer["customer_id"]
        for customer in customers
    ]

    store_ids = [
        store["store_id"]
        for store in stores
    ]

    # -----------------------------------------------------
    # Generate orders
    # -----------------------------------------------------

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "order_id",
        "customer_id",
        "store_id",
        "order_date",
        "channel",
        "payment_method",
        "order_status",
    ]

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

        for i in range(
            1,
            NUMBER_OF_ORDERS + 1
        ):

            order_id = f"O{i:06d}"

            customer_id = random.choice(
                customer_ids
            )

            channel = choose_channel()

            # Online orders don't require a physical store.
            if channel == "Online":
                store_id = "ONLINE"

            else:
                store_id = random.choice(
                    store_ids
                )

            writer.writerow(
                {
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "store_id": store_id,
                    "order_date": random_order_date(),
                    "channel": channel,
                    "payment_method": choose_payment_method(),
                    "order_status": choose_order_status(),
                }
            )

    print(
        f"Created {output_path}"
    )

    print(
        f"Orders generated: {NUMBER_OF_ORDERS}"
    )


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    generate_orders()