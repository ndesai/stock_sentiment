from typing import List, Optional
from pydantic import BaseModel, Field


class PriceRange(BaseModel):
    high: float
    low: float


class StockDetails(BaseModel):
    ticker: str
    full_name: str
    current_price: float
    market_cap: str
    sector_industry: str
    # Using an alias because variables cannot start with numbers in Python
    high_low_52_week: PriceRange = Field(..., alias="52_week_high_low")
    pe_ratio: float
    volume: str
    recent_dividend: str


class NewsImpactAnalysis(BaseModel):
    outlook: str
    estimated_price_impact_pct: str
    reasoning: str


class PotentialProfitRisks(BaseModel):
    long_position: str
    short_position: str
    key_risks: str


class StockAnalysis(BaseModel):
    details: StockDetails
    impact_theory: str
    news_impact_analysis: NewsImpactAnalysis
    potential_profit_risks: PotentialProfitRisks
    confidence_rating: str
    justification: str

    class Config:
        # This allows you to populate the model using the original JSON keys
        populate_by_name = True


class StockAnalysisList(BaseModel):
    stocks: List[StockAnalysis]


class Email(BaseModel):
    """
    Email configuration
    """

    sender_email: str
    sender_password: str
    mailing_list: str
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587


class Debug(BaseModel):
    """
    Debug configuration
    """

    enabled: bool
    prompt: str
    verbose: bool
