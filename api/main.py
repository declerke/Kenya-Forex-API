from fastapi import FastAPI
from routers import rates, analytics

app = FastAPI(
    title="Kenya Forex Intelligence API",
    description="Real-time and historical KES exchange rate analytics powered by DuckDB",
    version="1.0.0",
)

app.include_router(rates.router, prefix="/rates", tags=["Rates"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
