import yfinance as yf
from typing import Dict, List

class FinancialDataFetcher:
    def __init__(self):
        print("Financial Data Fetcher initialized")

    def get_stock_data(self, ticker: str) -> dict:
        try:
            if not ticker.endswith(".NS"):
                ticker = ticker + ".NS"
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                "ticker": ticker,
                "current_price": info.get("currentPrice", "N/A"),
                "market_cap": info.get("marketCap", "N/A"),
                "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
                "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
                "pe_ratio": info.get("trailingPE", "N/A"),
                "revenue": info.get("totalRevenue", "N/A"),
                "net_profit": info.get("netIncomeToCommon", "N/A"),
                "debt_to_equity": info.get("debtToEquity", "N/A"),
                "roe": info.get("returnOnEquity", "N/A")
            }
        except Exception as e:
            print(f"Stock data fetch error for {ticker}: {e}")
            return {}

    def get_multiple_stocks(self, tickers: list) -> dict:
        all_data = {}
        for ticker in tickers:
            print(f"Fetching data for: {ticker}")
            all_data[ticker] = self.get_stock_data(ticker)
        return all_data

    def format_for_report(self, stock_data: dict) -> str:
        report = ""
        for ticker, data in stock_data.items():
            if not data:
                continue
            report += f"\n### {ticker} Financial Data\n"
            report += "| **Metric** | **Value** |\n| --- | --- |\n"
            report += f"| Current Price | {data.get('current_price', 'N/A')} |\n"
            mc = data.get('market_cap', 'N/A')
            if isinstance(mc, (int, float)):
                mc = round(mc / 1e7, 2)
            report += f"| Market Cap (Cr) | {mc} |\n"
            report += f"| 52-Week High | {data.get('52_week_high', 'N/A')} |\n"
            report += f"| 52-Week Low | {data.get('52_week_low', 'N/A')} |\n"
            report += f"| P/E Ratio | {data.get('pe_ratio', 'N/A')} |\n"
            rev = data.get('revenue', 'N/A')
            if isinstance(rev, (int, float)):
                rev = round(rev / 1e7, 2)
            report += f"| Revenue (Cr) | {rev} |\n"
            np_ = data.get('net_profit', 'N/A')
            if isinstance(np_, (int, float)):
                np_ = round(np_ / 1e7, 2)
            report += f"| Net Profit (Cr) | {np_} |\n"
            roe = data.get('roe', 'N/A')
            if isinstance(roe, (int, float)):
                roe = round(roe * 100, 2)
            report += f"| ROE (%) | {roe} |\n"
            report += f"| Debt to Equity | {data.get('debt_to_equity', 'N/A')} |\n"
        return report

    def get_sector_kpis(self, ticker: str, sector: str) -> dict:
        try:
            if not ticker.endswith(".NS"):
                ticker = ticker + ".NS"
            stock = yf.Ticker(ticker)
            info = stock.info

            def pct(val):
                return round(val * 100, 2) if val else "N/A"

            base = {
                "sector": sector,
                "ticker": ticker,
                "profit_margin": pct(info.get("profitMargins")),
                "operating_margin": pct(info.get("operatingMargins")),
                "revenue_growth": pct(info.get("revenueGrowth")),
                "return_on_equity": pct(info.get("returnOnEquity")),
                "total_employees": info.get("fullTimeEmployees", "N/A"),
                "price_to_earnings": info.get("trailingPE", "N/A"),
            }

            sector_extras = {
                "IT": {
                    "gross_margin": pct(info.get("grossMargins")),
                    "revenue_per_share": info.get("revenuePerShare", "N/A"),
                },
                "Pharma": {
                    "rd_expense": info.get("researchDevelopment", "N/A"),
                    "gross_margin": pct(info.get("grossMargins")),
                },
                "Banking": {
                    "return_on_assets": pct(info.get("returnOnAssets")),
                    "book_value": info.get("bookValue", "N/A"),
                    "price_to_book": info.get("priceToBook", "N/A"),
                },
                "Energy": {
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                    "ebitda": info.get("ebitda", "N/A"),
                    "ebitda_margins": pct(info.get("ebitdaMargins")),
                },
                "FMCG": {
                    "gross_margin": pct(info.get("grossMargins")),
                    "dividend_yield": pct(info.get("dividendYield")),
                },
                "Auto": {
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                    "earnings_growth": pct(info.get("earningsGrowth")),
                },
                "Telecom": {
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                    "ebitda": info.get("ebitda", "N/A"),
                    "ebitda_margins": pct(info.get("ebitdaMargins")),
                    "free_cashflow": info.get("freeCashflow", "N/A"),
                },
                "RealEstate": {
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                    "book_value": info.get("bookValue", "N/A"),
                    "price_to_book": info.get("priceToBook", "N/A"),
                },
                "Metals": {
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                    "ebitda": info.get("ebitda", "N/A"),
                    "ebitda_margins": pct(info.get("ebitdaMargins")),
                },
                "Insurance": {
                    "return_on_assets": pct(info.get("returnOnAssets")),
                    "book_value": info.get("bookValue", "N/A"),
                    "price_to_book": info.get("priceToBook", "N/A"),
                    "earnings_growth": pct(info.get("earningsGrowth")),
                },
                "Cement": {
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                    "ebitda_margins": pct(info.get("ebitdaMargins")),
                    "gross_margin": pct(info.get("grossMargins")),
                },
                "Chemicals": {
                    "gross_margin": pct(info.get("grossMargins")),
                    "rd_expense": info.get("researchDevelopment", "N/A"),
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                },
                "Consumer": {
                    "gross_margin": pct(info.get("grossMargins")),
                    "dividend_yield": pct(info.get("dividendYield")),
                    "earnings_growth": pct(info.get("earningsGrowth")),
                },
                "Infrastructure": {
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                    "ebitda": info.get("ebitda", "N/A"),
                    "book_value": info.get("bookValue", "N/A"),
                },
                "Media": {
                    "gross_margin": pct(info.get("grossMargins")),
                    "earnings_growth": pct(info.get("earningsGrowth")),
                    "free_cashflow": info.get("freeCashflow", "N/A"),
                },
                "Aviation": {
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                    "ebitda_margins": pct(info.get("ebitdaMargins")),
                },
                "Retail": {
                    "gross_margin": pct(info.get("grossMargins")),
                    "earnings_growth": pct(info.get("earningsGrowth")),
                },
                "Hospitality": {
                    "gross_margin": pct(info.get("grossMargins")),
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                    "return_on_assets": pct(info.get("returnOnAssets")),
                },
                "Agriculture": {
                    "gross_margin": pct(info.get("grossMargins")),
                    "revenue_growth": pct(info.get("revenueGrowth")),
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                },
                "Defense": {
                    "revenue_growth": pct(info.get("revenueGrowth")),
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                },
            }

            extras = sector_extras.get(sector, {})
            base.update(extras)
            return base

        except Exception as e:
            print(f"KPI fetch error for {ticker}: {e}")
            return {}

    def format_kpis_for_report(self, kpi_data: dict) -> str:
        if not kpi_data:
            return "No KPI data available."
        report = f"\n### {kpi_data.get('ticker', '')} — {kpi_data.get('sector', '')} KPIs\n"
        report += "| **KPI** | **Value** |\n| --- | --- |\n"
        skip = {"sector", "ticker"}
        for key, value in kpi_data.items():
            if key in skip:
                continue
            label = key.replace("_", " ").title()
            report += f"| {label} | {value} |\n"
        return report
