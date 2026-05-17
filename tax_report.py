from data import Result, Lot
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

class TaxReport:
    def __init__(self):
        self.results: list[Result] = []
        self.styles = getSampleStyleSheet()

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

        print(f"\n=== Summary ===")
        print(f"Total spent: {round(total_spent, 2)}, Total gain: {round(total_gain, 2)}")
        print(f"Net capital result: {round(total_result, 2)}, Tax owed: {capital_tax}")
        print(f"Dividends gross: {round(total_divs, 2)}, "
              f"Polish 19% tax: {round(total_polish_div_tax, 2)}, "
              f"Foreign deduction: {round(total_foreign_ded, 2)}, "
              f"Dividend tax owed: {dividend_tax_owed}")
        
    def render_lot(self, ticker: str, lot: Lot):
        story = []
        story.append(Paragraph(f"<b>{ticker} — sold {lot.sale.time}</b>", self.styles["Heading3"]))

        data = [["Purchase date", "Rate", "Shares", "Cost (PLN)"]]
        for p in lot.purchases:
            data.append([p.time, f"{p.rate:.4f}", f"{p.shares:.6f}",
                        f"{p.shares * p.price:,.2f}"])
        data.append(["", "", "Proceeds",        f"{lot.proceeds:,.2f}"])
        data.append(["", "", "Cost basis",      f"{lot.cost_basis:,.2f}"])
        data.append(["", "", "Capital result",  f"{lot.proceeds - lot.cost_basis:,.2f}"])

        table = Table(data, colWidths=[35*mm, 20*mm, 30*mm, 30*mm], repeatRows=1)
        table.setStyle(TableStyle([]))
        story.append(table)
        story.append(Spacer(1, 8*mm))
        return story


    def build_pdf(self, path: str):
        doc = SimpleDocTemplate(path, pagesize=A4)
        story = []
        for r in self.results:
            for lot in r.lots:
                story.extend(self.render_lot(r.ticker, lot))
        doc.build(story)