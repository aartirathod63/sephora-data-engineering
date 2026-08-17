import csv
from pathlib import Path


STORES = [
    {
        "store_id": "ST001",
        "store_name": "Sephora Phoenix Marketcity Pune",
        "city": "Pune",
        "state": "Maharashtra",
        "mall": "Phoenix Marketcity",
        "area": "Viman Nagar",
        "store_type": "Physical Store",
    },
    {
        "store_id": "ST002",
        "store_name": "Sephora Phoenix Mall of the Millennium",
        "city": "Pune",
        "state": "Maharashtra",
        "mall": "Phoenix Mall of the Millennium",
        "area": "Wakad",
        "store_type": "Physical Store",
    },
    {
        "store_id": "ST003",
        "store_name": "Sephora Mumbai",
        "city": "Mumbai",
        "state": "Maharashtra",
        "mall": "Premium Retail Location",
        "area": "Mumbai",
        "store_type": "Physical Store",
    },
    {
        "store_id": "ST004",
        "store_name": "Sephora Bengaluru",
        "city": "Bengaluru",
        "state": "Karnataka",
        "mall": "Premium Retail Location",
        "area": "Bengaluru",
        "store_type": "Physical Store",
    },
    {
        "store_id": "ST005",
        "store_name": "Sephora Delhi",
        "city": "New Delhi",
        "state": "Delhi",
        "mall": "Premium Retail Location",
        "area": "New Delhi",
        "store_type": "Physical Store",
    },
]


def generate_stores():
    output_path = Path("data/raw/stores.csv")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=STORES[0].keys()
        )

        writer.writeheader()
        writer.writerows(STORES)

    print(f"Created {output_path}")
    print(f"Stores generated: {len(STORES)}")


if __name__ == "__main__":
    generate_stores()