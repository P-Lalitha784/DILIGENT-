import sqlite3
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    conn = sqlite3.connect(root / "ecom.db")
    cur = conn.cursor()

    print("Top products by revenue:")
    cur.execute(
        """
        SELECT
            p.product_id,
            p.product_name,
            SUM(oi.quantity) AS total_quantity_sold,
            ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue,
            COUNT(DISTINCT o.customer_id) AS distinct_customers
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_revenue DESC
        LIMIT 10;
        """
    )
    for row in cur.fetchall():
        print(row)

    print("\nSales per country:")
    cur.execute(
        """
        SELECT
            c.country,
            COUNT(*) AS total_orders,
            ROUND(SUM(o.total_amount), 2) AS total_revenue,
            ROUND(AVG(o.total_amount), 2) AS avg_order_value
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.country
        ORDER BY total_revenue DESC;
        """
    )
    for row in cur.fetchall():
        print(row)

    conn.close()


if __name__ == "__main__":
    main()


