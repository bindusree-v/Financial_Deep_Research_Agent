from core.research_loop import ResearchLoop
from core.report_generator import ReportGenerator

class CementAgent:
    def __init__(self):
        self.research_loop = ResearchLoop()
        self.report_generator = ReportGenerator()
        print("Cement Sector Agent initialized")

    def run(self, query: str) -> str:
        print("Cement Agent starting deep research...")
        findings = self.research_loop.run(query, "Cement")
        report = self.report_generator.generate(findings, "Cement", query)
        return report
