from core.research_loop import ResearchLoop
from core.report_generator import ReportGenerator

class ChemicalsAgent:
    def __init__(self):
        self.research_loop = ResearchLoop()
        self.report_generator = ReportGenerator()
        print("Chemicals Sector Agent initialized")

    def run(self, query: str) -> str:
        print("Chemicals Agent starting deep research...")
        findings = self.research_loop.run(query, "Chemicals")
        report = self.report_generator.generate(findings, "Chemicals", query)
        return report
