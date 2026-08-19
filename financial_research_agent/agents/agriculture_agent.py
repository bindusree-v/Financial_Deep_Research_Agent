from core.research_loop import ResearchLoop
from core.report_generator import ReportGenerator

class AgricultureAgent:
    def __init__(self):
        self.research_loop = ResearchLoop()
        self.report_generator = ReportGenerator()
        print("Agriculture Sector Agent initialized")

    def run(self, query: str) -> str:
        print("Agriculture Agent starting deep research...")
        findings = self.research_loop.run(query, "Agriculture")
        report = self.report_generator.generate(findings, "Agriculture", query)
        return report
