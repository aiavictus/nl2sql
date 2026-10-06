## README.md

# Local NL2SQL

 Offline local web application that converts natural language questions into SQL.

 ## Features

 - Fully local execution
- No cloud API dependency
- Natural language to SQL generation
- Multiple local LLM options:
  - `llama3.2`
  - `gemma3`
  - `qwen3`
- SQL validation before output
- Blocks unsafe SQL operations
- Generates SQL only (does not execute queries)

 ## Project Structure

```
NL2SQL/
│
├── app/
│   ├── api.py
│   ├── llm.py
│   ├── nl2sql.py
│   ├── prompt.py
│   ├── schema.py
│   ├── validator.py
│   └── static/
│       └── index.html
│
├── data/
│   └── demo.db
│
├── tests/
│   ├── evaluate.py
│   └── evaluation_cases.json
│
├── .venv/
└── run.bat
```

 ## Requirements

 - Windows
- Python
- Ollama
- Installed local models

 Check installed models:

```
ollama list
```

 ## Run Application

 Double-click:

```
run.bat
```

 Or run from the command prompt:

```
python -m uvicorn app.api:app --host 127.0.0.1 --port 8000
```

 Open the application in your browser:

```
http://127.0.0.1:8000
```

 ## Demo Database

 Database:

```
data/demo.db
```

 ### `customers`

 | Column | Type | Key |
| --- | --- | --- |
| `customer_id` | INTEGER | PK |
| `name` | TEXT |  |
| `city` | TEXT |  |
| `status` | TEXT |  |

### `products`

 | Column | Type | Key |
| --- | --- | --- |
| `product_id` | INTEGER | PK |
| `product_name` | TEXT |  |
| `category` | TEXT |  |
| `price` | REAL |  |

### `orders`

 | Column | Type | Key |
| --- | --- | --- |
| `order_id` | INTEGER | PK |
| `customer_id` | INTEGER | FK → `customers.customer_id` |
| `product_id` | INTEGER | FK → `products.product_id` |
| `order_date` | TEXT |  |
| `quantity` | INTEGER |  |
| `total_amount` | REAL |  |

### Relationships

```
customers
    │
    │ customer_id
    ▼
orders
    │
    │ product_id
    ▼
products
```

 More specifically:

```
customers.customer_id
        │
        │ 1-to-many
        ▼
orders.customer_id

products.product_id
        │
        │ 1-to-many
        ▼
orders.product_id
```

 ## Example Questions

 The application can answer questions such as:

```
Show all customers
```

```
Find customers from Chennai
```

```
List products below 100
```

```
Show customer names with their orders
```

```
Show orders with quantity greater than 2
```

```
Find customers whose total spending is greater than the average customer spending
```

 ## Safety

 The application generates SQL but does not execute the generated query.

 The SQL validator:

 - Allows only `SELECT` queries
- Rejects `INSERT`
- Rejects `UPDATE`
- Rejects `DELETE`
- Rejects `DROP`
- Rejects `ALTER`
- Rejects `CREATE`
- Validates tables and columns against the known database schema

 ## Testing

 Run the evaluation suite:

```
python tests\evaluate.py
```

 The evaluation covers:

 - Valid SQL generation
- Ambiguous questions
- Invalid schema requests
- Unsafe SQL blocking
- Natural-language-to-SQL accuracy

 ## File Naming Convention

 Use the standard uppercase filename:

```
README.md
```

 Instead of:

```
readme.md
```

 On Windows, filenames are generally case-insensitive, but `README.md` is the conventional name used by Git repositories and development projects.

 ## Next Steps

 After completing the README:

 1. Add a `.gitignore` file.
2. Exclude `.venv/` from version control.
3. Decide whether `data/demo.db` should be committed.
4. Remove unnecessary temporary files.
5. Verify that `run.bat` starts the application correctly.
6. Test the application from a clean copy of the project.