from core.research_loop import ResearchLoop
from core.report_generator import ReportGenerator

class RetailAgent:
    def __init__(self):
        self.research_loop = ResearchLoop()
        self.report_generator = ReportGenerator()
        print("Retail Sector Agent initialized")

    def run(self, query: str) -> str:
        print("Retail Agent starting deep research...")
        findings = self.research_loop.run(query, "Retail")
        report = self.report_generator.generate(findings, "Retail", query)
        return report
