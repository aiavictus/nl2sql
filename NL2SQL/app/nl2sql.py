import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import re

from app.llm import ask_llm, DEFAULT_MODEL
from app.prompt import build_sql_prompt
from app.schema import get_schema
from app.validator import validate_sql


FORBIDDEN_SQL = re.compile(
    r"\b("
    r"INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|DETACH|PRAGMA"
    r")\b",
    re.IGNORECASE,
)


def contains_unsafe_sql_request(question: str) -> bool:
    return bool(FORBIDDEN_SQL.search(question))


def clean_sql(sql: str) -> str:
    sql = sql.strip()

    # Remove common markdown code fences.
    if sql.startswith("```"):
        lines = sql.splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        sql = "\n".join(lines).strip()

    # Remove Qwen-style closing thinking marker if present.
    if "</think>" in sql:
        sql = sql.split("</think>", 1)[1].strip()

    # If the model included explanatory text before SQL,
    # keep only the first SELECT statement.
    select_position = sql.upper().find("SELECT")

    if select_position > 0:
        sql = sql[select_position:].strip()

    return sql


def generate_sql(
    question: str,
    model: str = DEFAULT_MODEL,
) -> dict:

    schema = get_schema()
    normalized_question = question.strip().lower()

    if not normalized_question:
        return {
            "success": False,
            "model": model,
            "sql": None,
            "message": "Question cannot be empty.",
        }

    # Deterministic safety gate.
    if contains_unsafe_sql_request(question):
        return {
            "success": False,
            "model": model,
            "sql": None,
            "message": "Only SELECT queries are allowed.",
        }

    # List tables.
    if normalized_question in {
        "list all tables",
        "list tables",
        "show all tables",
        "show tables",
    }:
        table_names = [table["table"] for table in schema]

        return {
            "success": True,
            "model": model,
            "sql": None,
            "message": "Available tables: " + ", ".join(table_names),
        }

    # Describe table.
    if normalized_question.startswith(("describe ", "show columns for ")):
        if normalized_question.startswith("describe "):
            table_name = normalized_question[len("describe "):].strip()
        else:
            table_name = normalized_question[
                len("show columns for "):
            ].strip()

        table = next(
            (
                table
                for table in schema
                if table["table"].lower() == table_name
            ),
            None,
        )

        if table is None:
            return {
                "success": False,
                "model": model,
                "sql": None,
                "message": f"Unknown table: {table_name}",
            }

        columns = ", ".join(
            f'{column["name"]} ({column["type"]})'
            for column in table["columns"]
        )

        return {
            "success": True,
            "model": model,
            "sql": None,
            "message": f"{table['table']}: {columns}",
        }

    prompt = build_sql_prompt(
        json.dumps(schema, indent=2),
        question,
    )

    sql = clean_sql(
        ask_llm(prompt, model=model)
    )

    if sql.startswith("CLARIFICATION_REQUIRED:"):
        return {
            "success": False,
            "model": model,
            "sql": None,
            "message": sql,
        }

    valid, message = validate_sql(sql, schema)

    return {
        "success": valid,
        "model": model,
        "sql": sql if valid else None,
        "message": message,
    }


if __name__ == "__main__":
    result = generate_sql(
        "Show all customer names.",
        model=DEFAULT_MODEL,
    )

    print(json.dumps(result, indent=2))