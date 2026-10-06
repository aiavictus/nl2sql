import sqlglot
from sqlglot import exp


def validate_sql(sql: str, schema: list) -> tuple[bool, str]:
    sql = sql.strip()

    if not sql:
        return False, "Empty SQL."

    try:
        statements = sqlglot.parse(sql, dialect="sqlite")
    except Exception as exc:
        return False, f"Invalid SQL: {exc}"

    if len(statements) != 1:
        return False, "Only one SQL statement is allowed."

    statement = statements[0]

    if not isinstance(statement, exp.Select):
        return False, "Only SELECT statements are allowed."

    schema_map = {
        table["table"]: {
            column["name"]
            for column in table["columns"]
        }
        for table in schema
    }

    aliases = {}

    for table in statement.find_all(exp.Table):
        table_name = table.name

        if table_name not in schema_map:
            return False, f"Unknown table: {table_name}"

        if table.alias:
            aliases[table.alias] = table_name

    select_aliases = {
        expression.output_name
        for expression in statement.expressions
        if expression.output_name
    }

    for column in statement.find_all(exp.Column):
        column_name = column.name
        table_name = column.table

        if not table_name and column_name in select_aliases:
            continue

        if table_name:
            actual_table = aliases.get(table_name, table_name)

            if actual_table not in schema_map:
                return False, f"Unknown table: {table_name}"

            if column_name not in schema_map[actual_table]:
                return False, f"Unknown column: {table_name}.{column_name}"

        else:
            matches = [
                table
                for table, columns in schema_map.items()
                if column_name in columns
            ]

            if not matches:
                return False, f"Unknown column: {column_name}"

    return True, "SQL is valid."