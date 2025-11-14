import csv
import datetime
import random
from pathlib import Path


def generate():
    random.seed(42)
    root = Path(__file__).resolve().parent

    products = [
        (1001, "Wireless Mouse", "Electronics", 19.99, "WM-1001"),
        (1002, "Mechanical Keyboard", "Electronics", 89.5, "MK-2100"),
        (1003, "USB-C Hub", "Accessories", 34.99, "UH-3102"),
        (1004, "Noise Cancelling Headphones", "Electronics", 149.0, "NH-4500"),
        (1005, 'Gaming Monitor 27"', "Electronics", 329.99, "GM-2701"),
        (1006, "Smartphone Stand", "Accessories", 15.25, "SS-1203"),
        (1007, "Portable SSD 1TB", "Storage", 129.99, "PS-1TB7"),
        (1008, "Fitness Tracker", "Wearables", 79.49, "FT-8802"),
        (1009, "Stainless Steel Water Bottle", "Home & Kitchen", 24.0, "WB-5501"),
        (1010, "Bluetooth Speaker", "Electronics", 59.99, "BS-6400"),
        (1011, "LED Desk Lamp", "Home & Office", 39.95, "DL-3301"),
        (1012, "Ergonomic Office Chair", "Furniture", 249.0, "OC-9104"),
        (1013, "4K Action Camera", "Photography", 199.5, "AC-7200"),
        (1014, "Electric Toothbrush", "Personal Care", 69.0, "ET-5100"),
        (1015, "Air Fryer 5qt", "Home Appliances", 119.99, "AF-5QT2"),
        (1016, "Yoga Mat", "Fitness", 32.0, "YM-2201"),
        (1017, "Wireless Charger Pad", "Accessories", 29.5, "WC-4300"),
        (1018, "Smart Thermostat", "Home Automation", 199.99, "ST-7800"),
        (1019, "Robot Vacuum", "Home Appliances", 349.0, "RV-9601"),
        (1020, "Coffee Grinder", "Home & Kitchen", 54.75, "CG-1402"),
    ]

    first_names = [
        "Liam",
        "Noah",
        "Oliver",
        "Elijah",
        "James",
        "William",
        "Benjamin",
        "Lucas",
        "Henry",
        "Alexander",
        "Emma",
        "Olivia",
        "Ava",
        "Sophia",
        "Isabella",
        "Mia",
        "Charlotte",
        "Amelia",
        "Harper",
        "Evelyn",
        "Mason",
        "Logan",
        "Ethan",
        "Jacob",
        "Michael",
        "Daniel",
        "Sebastian",
        "Jack",
        "Owen",
        "Samuel",
        "Victoria",
        "Grace",
        "Chloe",
        "Hazel",
        "Aurora",
        "Penelope",
        "Scarlett",
        "Madison",
        "Aria",
        "Layla",
        "Zoe",
        "Nora",
        "Lily",
        "Eleanor",
        "Hannah",
        "Lillian",
        "Addison",
        "Stella",
        "Paisley",
        "Skylar",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Rodriguez",
        "Martinez",
        "Hernandez",
        "Lopez",
        "Gonzalez",
        "Wilson",
        "Anderson",
        "Thomas",
        "Taylor",
        "Moore",
        "Jackson",
        "Martin",
        "Lee",
        "Perez",
        "Thompson",
        "White",
        "Harris",
        "Sanchez",
        "Clark",
        "Ramirez",
        "Lewis",
        "Robinson",
        "Walker",
        "Young",
        "Allen",
        "King",
        "Wright",
        "Scott",
        "Torres",
        "Nguyen",
        "Hill",
        "Flores",
        "Green",
        "Adams",
        "Nelson",
        "Baker",
        "Hall",
        "Rivera",
        "Campbell",
        "Mitchell",
        "Carter",
        "Roberts",
    ]
    countries = [
        "USA",
        "Canada",
        "UK",
        "Germany",
        "Australia",
        "France",
        "Spain",
        "India",
        "Brazil",
        "Netherlands",
    ]

    start_date = datetime.date.today() - datetime.timedelta(days=730)
    customers = []
    emails = set()
    for cid in range(2001, 2051):
        first = random.choice(first_names)
        last = random.choice(last_names)
        base_email = f"{first.lower()}.{last.lower()}@example.com"
        email = base_email
        counter = 1
        while email in emails:
            counter += 1
            email = f"{first.lower()}.{last.lower()}{counter}@example.com"
        emails.add(email)
        signup_offset = random.randint(0, 729)
        signup_date = start_date + datetime.timedelta(days=signup_offset)
        country = random.choice(countries)
        customers.append((cid, first, last, email, signup_date.isoformat(), country))

    order_statuses = ["Placed", "Completed", "Cancelled"]
    orders = []
    order_items = []
    order_id = 3001
    order_item_id = 4001
    for _ in range(200):
        cust = random.choice(customers)[0]
        order_date = datetime.date.today() - datetime.timedelta(
            days=random.randint(0, 364)
        )
        status = random.choices(order_statuses, weights=[3, 6, 1])[0]
        num_items = random.randint(1, 4)
        total = 0.0
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 3)
            unit_price = product[3]
            total += unit_price * quantity
            order_items.append(
                (order_item_id, order_id, product[0], quantity, unit_price)
            )
            order_item_id += 1
        total = round(total, 2)
        orders.append((order_id, cust, order_date.isoformat(), total, status))
        order_id += 1

    warehouses = ["East", "West"]
    inventory = []
    for product in products:
        product_id = product[0]
        assigned = random.sample(warehouses, k=random.randint(1, 2))
        for wh in assigned:
            stock = random.randint(20, 400)
            restock_date = datetime.date.today() - datetime.timedelta(
                days=random.randint(10, 120)
            )
            inventory.append((product_id, wh, stock, restock_date.isoformat()))

    def write_csv(filename, headers, rows):
        with open(root / filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    write_csv(
        "products.csv",
        ["product_id", "product_name", "category", "price", "sku"],
        products,
    )
    write_csv(
        "customers.csv",
        ["customer_id", "first_name", "last_name", "email", "signup_date", "country"],
        customers,
    )
    write_csv(
        "orders.csv",
        ["order_id", "customer_id", "order_date", "total_amount", "status"],
        orders,
    )
    write_csv(
        "order_items.csv",
        ["order_item_id", "order_id", "product_id", "quantity", "unit_price"],
        order_items,
    )
    write_csv(
        "inventory.csv",
        ["product_id", "warehouse", "stock_qty", "last_restock_date"],
        inventory,
    )


if __name__ == "__main__":
    generate()

