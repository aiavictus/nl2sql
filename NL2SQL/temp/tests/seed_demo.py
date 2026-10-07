import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import sqlite3

from app.db import DB_PATH


connection = sqlite3.connect(DB_PATH)

try:
    connection.executemany(
        """
        INSERT OR IGNORE INTO customers
        (customer_id, name, city, status)
        VALUES (?, ?, ?, ?)
        """,
        [
            (1, "Arun", "Chennai", "Active"),
            (2, "Priya", "Bengaluru", "Active"),
            (3, "Rahul", "Mumbai", "Inactive"),
            (4, "Divya", "Chennai", "Active"),
        ],
    )

    connection.executemany(
        """
        INSERT OR IGNORE INTO products
        (product_id, product_name, category, price)
        VALUES (?, ?, ?, ?)
        """,
        [
            (1, "Laptop", "Electronics", 75000),
            (2, "Keyboard", "Electronics", 2500),
            (3, "Office Chair", "Furniture", 12000),
            (4, "Monitor", "Electronics", 18000),
        ],
    )

    connection.executemany(
        """
        INSERT OR IGNORE INTO orders
        (order_id, customer_id, product_id, order_date, quantity, total_amount)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (1, 1, 1, "2026-09-01", 1, 75000),
            (2, 1, 2, "2026-09-03", 2, 5000),
            (3, 2, 3, "2026-09-05", 1, 12000),
            (4, 4, 4, "2026-09-08", 2, 36000),
        ],
    )

    connection.commit()
    print("Demo data seeded successfully.")

finally:
    connection.close()