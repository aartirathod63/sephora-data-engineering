import csv
import random
from pathlib import Path
from datetime import date, timedelta

from faker import Faker


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

fake = Faker("en_IN")

# Make the generated dataset reproducible
random.seed(42)
Faker.seed(42)


# ---------------------------------------------------------
# Indian customer distribution
# ---------------------------------------------------------

CITY_DATA = [
    ("Pune", "Maharashtra", 25),
    ("Mumbai", "Maharashtra", 20),
    ("Bengaluru", "Karnataka", 18),
    ("New Delhi", "Delhi", 12),
    ("Hyderabad", "Telangana", 8),
    ("Chennai", "Tamil Nadu", 6),
    ("Ahmedabad", "Gujarat", 4),
    ("Kolkata", "West Bengal", 4),
    ("Gurugram", "Haryana", 2),
    ("Noida", "Uttar Pradesh", 1),
]


# ---------------------------------------------------------
# Loyalty tier distribution
# ---------------------------------------------------------

LOYALTY_TIERS = [
    ("Bronze", 50),
    ("Silver", 30),
    ("Gold", 15),
    ("Platinum", 5),
]


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def weighted_city_choice():
    """
    Select a city using the business-defined distribution.
    """

    cities = [
        city_data[0]
        for city_data in CITY_DATA
    ]

    weights = [
        city_data[2]
        for city_data in CITY_DATA
    ]

    return random.choices(
        cities,
        weights=weights,
        k=1
    )[0]


def get_state(city):
    """
    Return the state associated with a city.
    """

    city_state_mapping = {
        city_data[0]: city_data[1]
        for city_data in CITY_DATA
    }

    return city_state_mapping[city]


def weighted_loyalty_choice():
    """
    Select a loyalty tier using the business-defined distribution.
    """

    tiers = [
        tier[0]
        for tier in LOYALTY_TIERS
    ]

    weights = [
        tier[1]
        for tier in LOYALTY_TIERS
    ]

    return random.choices(
        tiers,
        weights=weights,
        k=1
    )[0]


# ---------------------------------------------------------
# Customer generator
# ---------------------------------------------------------

def generate_customers(count=5000):

    output_path = Path(
        "data/raw/customers.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "city",
        "state",
        "age",
        "gender",
        "signup_date",
        "loyalty_tier",
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

        for i in range(1, count + 1):

            # Select city based on business distribution
            city = weighted_city_choice()

            # Get corresponding state
            state = get_state(city)

            # Generate signup date
            signup_date = (
                date.today()
                - timedelta(
                    days=random.randint(
                        30,
                        1500
                    )
                )
            )

            # Generate realistic age
            age = random.randint(
                18,
                60
            )

            # Generate gender distribution
            gender = random.choices(
                [
                    "Female",
                    "Male",
                    "Other"
                ],
                weights=[
                    72,
                    25,
                    3
                ],
                k=1
            )[0]

            # Generate loyalty tier
            loyalty_tier = weighted_loyalty_choice()

            writer.writerow(
                {
                    "customer_id": f"C{i:05d}",
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "email": fake.email(),
                    "city": city,
                    "state": state,
                    "age": age,
                    "gender": gender,
                    "signup_date": signup_date,
                    "loyalty_tier": loyalty_tier,
                }
            )

    print(
        f"Created {output_path}"
    )

    print(
        f"Customers generated: {count}"
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    generate_customers()