import duckdb
import os

DUCKDB_PATH = os.getenv("DUCKDB_PATH", "./data/forex.db")


def init_db():
    con = duckdb.connect(DUCKDB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS forex_rates (
            fetched_at      TIMESTAMPTZ,
            base_currency   VARCHAR,
            target_currency VARCHAR,
            rate            DOUBLE
        )
    """)
    con.close()


def insert_rates(rates_data: dict):
    con = duckdb.connect(DUCKDB_PATH)
    rows = [
        (rates_data["fetched_at"], rates_data["base_currency"], currency, rate)
        for currency, rate in rates_data["rates"].items()
    ]
    con.executemany(
        "INSERT INTO forex_rates (fetched_at, base_currency, target_currency, rate) VALUES (?, ?, ?, ?)",
        rows,
    )
    con.close()
