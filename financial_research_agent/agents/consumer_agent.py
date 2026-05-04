from core.research_loop import ResearchLoop
from core.report_generator import ReportGenerator

class ConsumerAgent:
    def __init__(self):
        self.research_loop = ResearchLoop()
        self.report_generator = ReportGenerator()
        print("Consumer Sector Agent initialized")

    def run(self, query: str) -> str:
        print("Consumer Agent starting deep research...")
        findings = self.research_loop.run(query, "Consumer")
        report = self.report_generator.generate(findings, "Consumer", query)
        return report
