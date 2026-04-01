from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class LiveRatesResponse(BaseModel):
    base_currency: str
    fetched_at: datetime
    rates: Dict[str, float]

class HistoryResponse(BaseModel):
    currency: str
    fetched_at: datetime
    rate: float

class VolatilityResponse(BaseModel):
    currency: str
    volatility: float | None
    min_rate: float
    max_rate: float
    data_points: int
    window_days: int

class TrendResponse(BaseModel):
    currency: str
    window_days: int
    moving_average: float | None
    data_points: int
