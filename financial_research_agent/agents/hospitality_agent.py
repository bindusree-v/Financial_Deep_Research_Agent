from core.research_loop import ResearchLoop
from core.report_generator import ReportGenerator

class HospitalityAgent:
    def __init__(self):
        self.research_loop = ResearchLoop()
        self.report_generator = ReportGenerator()
        print("Hospitality Sector Agent initialized")

    def run(self, query: str) -> str:
        print("Hospitality Agent starting deep research...")
        findings = self.research_loop.run(query, "Hospitality")
        report = self.report_generator.generate(findings, "Hospitality", query)
        return report
