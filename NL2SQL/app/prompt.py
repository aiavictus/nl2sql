def build_sql_prompt(schema: str, question: str) -> str:
    return f"""
You convert natural-language questions into SQL for the database schema below.

Before generating SQL, internally determine:

1. What information the user wants.
2. Which tables and columns are required.
3. Which foreign-key relationships are required.
4. Which filters, grouping, aggregation, ordering, limits, or ranking
   operations are required.
5. Whether the request can be answered reliably from the provided schema.

Use the meaning of the user's natural language to determine the appropriate
SQL operation. Do not require the user to name database columns explicitly
when the intended column can be determined from the schema.

Use foreign-key relationships when related tables are needed.

If the request is genuinely ambiguous or cannot be answered reliably from
the schema, return exactly:
CLARIFICATION_REQUIRED: <short question>

Rules:

- Use only tables, columns, and relationships present in the schema.
- Never invent tables, columns, values, or relationships.
- Generate exactly one SQL SELECT statement.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
  ATTACH, DETACH, or PRAGMA.
- Do not execute SQL.
- Do not explain your reasoning.
- Return only the SQL statement or the CLARIFICATION_REQUIRED response.

Database schema:
{schema}

User question:
{question}
""".strip()