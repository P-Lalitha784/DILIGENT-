import csv
import sqlite3
from pathlib import Path


def load():
    root = Path(__file__).resolve().parent
    conn = sqlite3.connect(root / "ecom.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()

    cur.executescript(
        """
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS inventory;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            sku TEXT NOT NULL
        );

        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            signup_date TEXT NOT NULL,
            country TEXT NOT NULL
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );

        CREATE TABLE inventory (
            product_id INTEGER NOT NULL,
            warehouse TEXT NOT NULL,
            stock_qty INTEGER NOT NULL,
            last_restock_date TEXT NOT NULL,
            PRIMARY KEY (product_id, warehouse),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """
    )

    files = {
        "products": [
            "product_id",
            "product_name",
            "category",
            "price",
            "sku",
        ],
        "customers": [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "signup_date",
            "country",
        ],
        "orders": [
            "order_id",
            "customer_id",
            "order_date",
            "total_amount",
            "status",
        ],
        "order_items": [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
        ],
        "inventory": [
            "product_id",
            "warehouse",
            "stock_qty",
            "last_restock_date",
        ],
    }

    for table, headers in files.items():
        with open(root / f"{table}.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [tuple(row[h] for h in headers) for row in reader]
        placeholders = ",".join("?" for _ in headers)
        cur.executemany(
            f"INSERT INTO {table} ({','.join(headers)}) VALUES ({placeholders})", rows
        )

    conn.commit()

    for table in files:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"{table}: {count} rows")
        cur.execute(f"SELECT * FROM {table} LIMIT 5")
        for row in cur.fetchall():
            print(row)
        print("-" * 40)

    conn.close()


if __name__ == "__main__":
    load()


