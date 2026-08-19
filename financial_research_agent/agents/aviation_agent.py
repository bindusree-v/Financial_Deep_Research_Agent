from core.research_loop import ResearchLoop
from core.report_generator import ReportGenerator

class AviationAgent:
    def __init__(self):
        self.research_loop = ResearchLoop()
        self.report_generator = ReportGenerator()
        print("Aviation Sector Agent initialized")

    def run(self, query: str) -> str:
        print("Aviation Agent starting deep research...")
        findings = self.research_loop.run(query, "Aviation")
        report = self.report_generator.generate(findings, "Aviation", query)
        return report
