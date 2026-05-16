from data import Result

class TaxReport:
    def __init__(self):
        self.results: list[Result] = []

    def add(self, result: Result) -> None:
        self.results.append(result)

    def print_summary(self):
        total_spent = sum(r.total_spend for r in self.results)
        total_gain = sum(r.total_gain for r in self.results)
        total_result = sum(r.capital_result for r in self.results)
        total_divs = sum(r.dividends_gross for r in self.results)
        total_polish_div_tax = sum(r.polish_dividend_tax for r in self.results)
        total_foreign_ded = sum(r.foreign_tax_deduction for r in self.results)

        capital_tax = round(total_result * 0.19, 2) if total_result > 0 else 0
        dividend_tax_owed = max(0, round(total_polish_div_tax - total_foreign_ded, 2))

        for r in self.results:
            print(f"{r.ticker}: spent={r.total_spend}, gain={r.total_gain}, "
                  f"result={r.capital_result}, divs={r.dividends_gross}")

        print(f"\n=== Summary ===")
        print(f"Total spent: {round(total_spent, 2)}, Total gain: {round(total_gain, 2)}")
        print(f"Net capital result: {round(total_result, 2)}, Tax owed: {capital_tax}")
        print(f"Dividends gross: {round(total_divs, 2)}, "
              f"Polish 19% tax: {round(total_polish_div_tax, 2)}, "
              f"Foreign deduction: {round(total_foreign_ded, 2)}, "
              f"Dividend tax owed: {dividend_tax_owed}")