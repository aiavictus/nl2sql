import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "demo.db"


def get_schema():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    schema = []

    tables = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    ).fetchall()

    for table in tables:
        table_name = table["name"]

        columns = []
        for column in connection.execute(
            f"PRAGMA table_info('{table_name}')"
        ):
            columns.append(
                {
                    "name": column["name"],
                    "type": column["type"],
                    "primary_key": bool(column["pk"]),
                }
            )

        relationships = []
        for foreign_key in connection.execute(
            f"PRAGMA foreign_key_list('{table_name}')"
        ):
            relationships.append(
                {
                    "column": foreign_key["from"],
                    "references_table": foreign_key["table"],
                    "references_column": foreign_key["to"],
                }
            )

        schema.append(
            {
                "table": table_name,
                "columns": columns,
                "relationships": relationships,
            }
        )

    connection.close()
    return schema


if __name__ == "__main__":
    import json

    print(json.dumps(get_schema(), indent=2))