from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    action: str
    time: datetime
    year: int
    ticker: str
    shares: float
    price: float
    currency: str
    withholding: float = 0.0


@dataclass 
class Result:
    ticker: str
    total_spend: float = 0.0
    total_gain: float = 0.0
    dividends_gross: float = 0.0
    polish_dividend_tax: float = 0.0
    foreign_tax_deduction: float = 0.0

    @property
    def capital_result(self) -> float:
        return round(self.total_gain - self.total_spend, 2)
