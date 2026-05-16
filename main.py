import pandas as pd
from tax_calculator import TaxCalculator
from tax_report import TaxReport
from transaction_loader import load_transactions

def main(tax_year: int):
    transactions = load_transactions(["INPUT"])
    
    unique_currencies = list(pd.unique(transactions["Currency (Price / share)"]))
    transactions["Year"] = pd.to_datetime(transactions["Time"]).dt.year
    unique_years = pd.unique(transactions["Year"])
    
    calc = TaxCalculator(unique_currencies, unique_years, tax_year)
    report = TaxReport()
    for ticker, group in transactions.groupby("Ticker"):
        sorted_transactions = group.sort_values(by="Time")
        result = calc.process_ticker(ticker, sorted_transactions)
        report.add(result)

    report.print_summary()

if __name__ == "__main__":
    main(2025)
