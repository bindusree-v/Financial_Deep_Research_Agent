from core.research_loop import ResearchLoop
from core.report_generator import ReportGenerator

class InfrastructureAgent:
    def __init__(self):
        self.research_loop = ResearchLoop()
        self.report_generator = ReportGenerator()
        print("Infrastructure Sector Agent initialized")

    def run(self, query: str) -> str:
        print("Infrastructure Agent starting deep research...")
        findings = self.research_loop.run(query, "Infrastructure")
        report = self.report_generator.generate(findings, "Infrastructure", query)
        return report
