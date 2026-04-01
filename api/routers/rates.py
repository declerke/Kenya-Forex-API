from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
from db import get_connection
from schemas import LiveRatesResponse, HistoryResponse

router = APIRouter()


@router.get("/live", response_model=LiveRatesResponse)
def get_live_rates():
    con = get_connection()
    try:
        rows = con.execute("""
            SELECT target_currency, rate, fetched_at
            FROM forex_rates
            WHERE fetched_at = (SELECT MAX(fetched_at) FROM forex_rates)
            ORDER BY target_currency
        """).fetchall()
    finally:
        con.close()

    if not rows:
        raise HTTPException(status_code=404, detail="No rate data available yet. Run the Airflow DAG first.")

    return {
        "base_currency": "KES",
        "fetched_at": rows[0][2],
        "rates": {row[0]: row[1] for row in rows},
    }


@router.get("/history", response_model=list[HistoryResponse])
def get_history(
    currency: str = Query("USD", description="Target currency code (USD, EUR, GBP, CNY, JPY)"),
    days: int = Query(30, ge=1, le=365, description="Number of days of history to return"),
):
    cutoff = datetime.utcnow() - timedelta(days=days)
    con = get_connection()
    try:
        rows = con.execute("""
            SELECT fetched_at, rate
            FROM forex_rates
            WHERE target_currency = ?
              AND fetched_at >= ?
            ORDER BY fetched_at ASC
        """, [currency.upper(), cutoff]).fetchall()
    finally:
        con.close()

    return [{"fetched_at": row[0], "rate": row[1], "currency": currency.upper()} for row in rows]
