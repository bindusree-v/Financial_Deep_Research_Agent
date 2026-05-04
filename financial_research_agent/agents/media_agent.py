from core.research_loop import ResearchLoop
from core.report_generator import ReportGenerator

class MediaAgent:
    def __init__(self):
        self.research_loop = ResearchLoop()
        self.report_generator = ReportGenerator()
        print("Media Sector Agent initialized")

    def run(self, query: str) -> str:
        print("Media Agent starting deep research...")
        findings = self.research_loop.run(query, "Media")
        report = self.report_generator.generate(findings, "Media", query)
        return report
