from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, timedelta
from db import get_connection
from schemas import VolatilityResponse, TrendResponse

router = APIRouter()


@router.get("/volatility", response_model=list[VolatilityResponse])
def get_volatility(
    days: int = Query(7, ge=1, le=90, description="Rolling window in days"),
):
    cutoff = datetime.utcnow() - timedelta(days=days)
    con = get_connection()
    try:
        rows = con.execute("""
            SELECT
                target_currency,
                STDDEV(rate)   AS volatility,
                MIN(rate)      AS min_rate,
                MAX(rate)      AS max_rate,
                COUNT(*)       AS data_points
            FROM forex_rates
            WHERE fetched_at >= ?
            GROUP BY target_currency
            ORDER BY volatility DESC NULLS LAST
        """, [cutoff]).fetchall()
    finally:
        con.close()

    if not rows:
        raise HTTPException(status_code=404, detail="No data in the requested window.")

    return [
        {
            "currency": row[0],
            "volatility": row[1],
            "min_rate": row[2],
            "max_rate": row[3],
            "data_points": row[4],
            "window_days": days,
        }
        for row in rows
    ]


@router.get("/trends", response_model=list[TrendResponse])
def get_trends(
    currency: str = Query("USD", description="Target currency code"),
    windows: str = Query("7,14,30", description="Comma-separated moving average windows in days"),
):
    window_list = [int(w.strip()) for w in windows.split(",") if w.strip().isdigit()]
    if not window_list:
        raise HTTPException(status_code=400, detail="Invalid windows parameter.")

    currency = currency.upper()
    con = get_connection()
    results = []

    try:
        for window in window_list:
            cutoff = datetime.utcnow() - timedelta(days=window)
            row = con.execute("""
                SELECT AVG(rate) AS moving_average, COUNT(*) AS data_points
                FROM forex_rates
                WHERE target_currency = ?
                  AND fetched_at >= ?
            """, [currency, cutoff]).fetchone()

            results.append({
                "currency": currency,
                "window_days": window,
                "moving_average": row[0],
                "data_points": row[1],
            })
    finally:
        con.close()

    return results
