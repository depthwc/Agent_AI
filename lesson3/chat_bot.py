from google import genai
from google.genai import types
import sqlite3
from typing import Any, Dict
import os
from dotenv import load_dotenv


load_dotenv(".env")


client = genai.Client(api_key=os.getenv(GEMAI))


DB_PATH = "data.db"  

def get_connection():
    return sqlite3.connect(DB_PATH)


def list_tables() -> Dict[str, Any]:
    """List available tables in the SQLite database."""
    query = """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        tables = [row[0] for row in cursor.fetchall()]

    return {"tables": tables, "count": len(tables)}


def describe_table(table: str) -> Dict[str, Any]:
    """Describe columns for a given table name."""
    query = f"PRAGMA table_info({table});"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    if not rows:
        return {"error": f"Unknown table '{table}'.", "hint": "Call list_tables() first."}

    columns = [
        {
            "name": row[1],           
            "type": row[2],           
            "nullable": row[3] == 0,  
        }
        for row in rows
    ]

    return {"table": table, "columns": columns}


def tool_db(query: str) -> Dict[str, Any]:
    """Run read-only SELECT SQL query."""
    if not query.strip().lower().startswith("select"):
        return {"error": "Only SELECT queries are allowed."}

    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    if not rows:
        return "No results found."

    results = [dict(row) for row in rows]
    return {"results": results}


# Gemini tool configuration
config = types.GenerateContentConfig(
    tools=[tool_db, describe_table, list_tables]
)

# Gemini prompt
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What are the names of products?",
    config=config,
)

print(response.text)
