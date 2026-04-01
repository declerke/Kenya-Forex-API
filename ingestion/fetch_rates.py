import requests
from datetime import datetime, timezone

BASE_URL = "https://open.er-api.com/v6/latest/KES"
TARGET_CURRENCIES = ["USD", "EUR", "GBP", "CNY", "JPY"]


def fetch_kes_rates() -> dict:
    response = requests.get(BASE_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("result") != "success":
        raise ValueError(f"API returned unsuccessful result: {data.get('result')}")

    rates = {
        currency: data["rates"][currency]
        for currency in TARGET_CURRENCIES
        if currency in data["rates"]
    }

    missing = set(TARGET_CURRENCIES) - set(rates.keys())
    if missing:
        raise ValueError(f"API response missing expected currencies: {missing}")

    return {
        "base_currency": "KES",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "rates": rates,
    }
