from core.research_loop import ResearchLoop
from core.report_generator import ReportGenerator

class DefenseAgent:
    def __init__(self):
        self.research_loop = ResearchLoop()
        self.report_generator = ReportGenerator()
        print("Defense Sector Agent initialized")

    def run(self, query: str) -> str:
        print("Defense Agent starting deep research...")
        findings = self.research_loop.run(query, "Defense")
        report = self.report_generator.generate(findings, "Defense", query)
        return report
