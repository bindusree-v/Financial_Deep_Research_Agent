"""
Pharma Agent Module
This module contains the PharmaAgent class responsible for coordinating
research and report generation specifically for the Pharma sector.
"""

# 1. Imports
from core.research_loop import ResearchLoop
from core.report_generator import ReportGenerator

class PharmaAgent:
    """
    Agent that specializes in Pharma sector research.
    It utilizes the ResearchLoop to gather findings and ReportGenerator
    to compile those findings into a structured markdown report.
    """
    
    def __init__(self):
        """
        Initializes the PharmaAgent with necessary components.
        """
        # Create an instance of the ResearchLoop to perform deep web searches
        self.research_loop = ResearchLoop()
        
        # Create an instance of the ReportGenerator to build the final report
        self.report_generator = ReportGenerator()
        
        # Print initialization message
        print("Pharma Sector Agent initialized")

    def run(self, query: str) -> str:
        """
        Executes the research process for a given Pharma sector query.
        
        Args:
            query (str): The specific research query provided by the user.
            
        Returns:
            str: The generated markdown report text.
        """
        # Print starting message for the research process
        print("Pharma Agent starting deep research...")
        
        # Run the deep research loop for the Pharma sector using the provided query
        # The loop returns a list of dictionaries containing step, query, and findings
        findings = self.research_loop.run(query, "Pharma")
        
        # Generate the final structured markdown report based on the gathered findings
        report_text = self.report_generator.generate(findings, "Pharma", query)
        
        # Return the final report text
        return report_text
