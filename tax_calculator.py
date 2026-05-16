import pandas as pd
from data import Transaction, Result
from nbp_provider import NBPRateProvider
from fifo import FIFO
from datetime import datetime

class TaxCalculator:
    POLISH_TAX_RATE = 0.19

    def __init__(self, currencies: list[str], years: list[str], tax_year: str) -> None:
        self.nbp_provider = NBPRateProvider.preload(years, currencies)
        self.tax_year = tax_year

    @staticmethod
    def _make_transaction(row) -> Transaction:
        currency = row._5
        price = row._4
        if currency == "GBX":
            currency = "GBP"
            price = price / 100
    
        return Transaction(
            action=row.Action,
            time=row.Time.split(" ")[0],
            year=row.Year,
            ticker=row.Ticker,
            shares = round(row._3, 6),
            price=price,
            currency=currency,
            withholding=row._6 if "dividend" in row.Action.lower() else 0.0
        )
    
    @staticmethod
    def _apply_dividend(tx: Transaction, rate: float, result: Result):
        gross_pln = round(tx.shares * tx.price * rate, 2)
        withholding_pln = round(tx.withholding * rate, 2)
        polish_tax = round(gross_pln * TaxCalculator.POLISH_TAX_RATE, 2)
        max_deduction = round(gross_pln * 0.15, 2)
        deduction = min(withholding_pln, max_deduction)

        result.dividends_gross += gross_pln
        result.polish_dividend_tax += polish_tax
        result.foreign_tax_deduction += deduction

    @staticmethod
    def _normalize_result(result: Result) -> Result:
        result.total_spend = round(result.total_spend, 2)
        result.total_gain = round(result.total_gain, 2)
        result.dividends_gross = round(result.dividends_gross, 2)
        result.polish_dividend_tax = round(result.polish_dividend_tax, 2)
        result.foreign_tax_deduction = round(result.foreign_tax_deduction, 2)
        return result

    def process_ticker(self, ticker: str, transactions: pd.DataFrame) -> Result:
        result = Result(ticker=ticker)
        memory = FIFO()

        for transaction in transactions.itertuples(index=False):
            tx = self._make_transaction(transaction)
            if tx.year > self.tax_year:
                break

            rate = self.nbp_provider.get_rate(tx.currency, tx.time)
            if rate is None:
                print(f"Couldn't find rate for transaction on {tx.time} for {tx.ticker}")
                continue

            price_pln = tx.price * rate

            if "buy" in tx.action.lower():
                memory.buy(tx.shares, price_pln)
            elif "sell" in tx.action.lower():
                cost = memory.sell(tx.shares)
                if tx.year < self.tax_year:
                    continue

                result.total_gain += tx.shares * price_pln
                result.total_spend += cost

            elif "dividend" in tx.action.lower():
                if tx.year < self.tax_year:
                    continue

                self._apply_dividend(tx, rate, result)
   
        return self._normalize_result(result)
