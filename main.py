import pandas as pd
from tax_calculator import TaxCalculator
from tax_report import TaxReport
from transaction_loader import load_transactions

def main(tax_year: int):
    transactions = load_transactions(["C:/python/from_2025-01-01_to_2025-12-31_MTc3ODkyNjE2NTk5NA.csv", "C:/python/from_2024-07-08_to_2024-12-31_MTc3ODkyODQ2MTc5OQ.csv", "C:/python/from_2026-01-01_to_2026-05-17_MTc3OTAyMjMyMTExMQ.csv"])
    
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
    report.build_pdf(f"./tax_report_{tax_year}.pdf")

if __name__ == "__main__":
    main(2026)
