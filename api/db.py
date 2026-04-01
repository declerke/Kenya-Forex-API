import os
import duckdb
from fastapi import HTTPException

DUCKDB_PATH = os.getenv("DUCKDB_PATH", "./data/forex.db")

def get_connection():
    if not os.path.exists(DUCKDB_PATH):
        raise HTTPException(
            status_code=503,
            detail="Database not yet initialised. Trigger the forex_ingestion DAG in Airflow first.",
        )
    return duckdb.connect(DUCKDB_PATH, read_only=True)
