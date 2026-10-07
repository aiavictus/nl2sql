import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.llm import AVAILABLE_MODELS, DEFAULT_MODEL
from app.nl2sql import generate_sql
from app.db import execute_select

app = FastAPI(title="Local NL2SQL")

STATIC_DIR = PROJECT_ROOT / "app" / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class SQLRequest(BaseModel):
    question: str
    model: str = DEFAULT_MODEL

@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate-sql")
def generate(request: SQLRequest):
    if request.model not in AVAILABLE_MODELS:
        return {
            "success": False,
            "model": request.model,
            "sql": None,
            "message": "Unknown model."
        }

    try:
        return generate_sql(
            request.question,
            model=request.model,
        )
    except Exception as exc:
        return {
            "success": False,
            "model": request.model,
            "sql": None,
            "message": f"Generation error: {exc}"
        }


@app.get("/models")
def models():
    return {
        "models": list(AVAILABLE_MODELS.keys()),
        "default": DEFAULT_MODEL,
    }

class SQLExecuteRequest(BaseModel):
    sql: str


@app.post("/execute-sql")
def execute_sql(request: SQLExecuteRequest):
    try:
        return execute_select(request.sql)
    except Exception as exc:
        return {
            "success": False,
            "columns": [],
            "rows": [],
            "row_count": 0,
            "message": f"Execution error: {exc}",
        }