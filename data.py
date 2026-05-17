from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Allocation:
    action: str
    shares: float
    price: float
    time: str
    rate: float

@dataclass
class Consumed:
    shares: float
    price: float
    time: str
    rate: float

@dataclass
class Lot:
    purchases: list[Consumed]
    sale: Allocation

    @property
    def cost_basis(self) -> float:
        return sum(p.shares * p.price for p in self.purchases)

    @property
    def proceeds(self) -> float:
        return self.sale.shares * self.sale.price

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
    lots: list[Lot] = field(default_factory=list)
    total_spend: float = 0.0
    total_gain: float = 0.0
    dividends_gross: float = 0.0
    polish_dividend_tax: float = 0.0
    foreign_tax_deduction: float = 0.0

    @property
    def capital_result(self) -> float:
        return round(self.total_gain - self.total_spend, 2)

