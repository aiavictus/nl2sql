import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import sqlite3

from app.schema import get_schema
from app.validator import validate_sql


DB_PATH = PROJECT_ROOT / "data" / "demo.db"


def execute_select(sql: str) -> dict:
    schema = get_schema()

    valid, message = validate_sql(sql, schema)

    if not valid:
        return {
            "success": False,
            "columns": [],
            "rows": [],
            "row_count": 0,
            "message": message,
        }

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute(sql)

        columns = [description[0] for description in cursor.description]
        rows = [dict(row) for row in cursor.fetchall()]

        return {
            "success": True,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "message": "Query executed successfully.",
        }

    except sqlite3.Error as exc:
        return {
            "success": False,
            "columns": [],
            "rows": [],
            "row_count": 0,
            "message": f"Database error: {exc}",
        }

    finally:
        connection.close()


if __name__ == "__main__":
    print(execute_select("SELECT name, city FROM customers"))
    print(execute_select("DELETE FROM customers"))