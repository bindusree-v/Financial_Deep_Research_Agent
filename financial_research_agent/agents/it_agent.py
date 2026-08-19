"""
IT Agent Module
This module contains the ITAgent class responsible for coordinating
research and report generation specifically for the IT sector.
"""

# 1. Imports
from core.research_loop import ResearchLoop
from core.report_generator import ReportGenerator

class ITAgent:
    """
    Agent that specializes in IT sector research.
    It utilizes the ResearchLoop to gather findings and ReportGenerator
    to compile those findings into a structured markdown report.
    """
    
    def __init__(self):
        """
        Initializes the ITAgent with necessary components.
        """
        # Create an instance of the ResearchLoop to perform deep web searches
        self.research_loop = ResearchLoop()
        
        # Create an instance of the ReportGenerator to build the final report
        self.report_generator = ReportGenerator()
        
        # Print initialization message
        print("IT Sector Agent initialized")

    def run(self, query: str) -> str:
        """
        Executes the research process for a given IT sector query.
        
        Args:
            query (str): The specific research query provided by the user.
            
        Returns:
            str: The generated markdown report text.
        """
        # Print starting message for the research process
        print("IT Agent starting deep research...")
        
        # Define IT specific topics list as requested
        it_topics = [
            "TCS Infosys Wipro HCL revenue",
            "Indian IT sector AI adoption",
            "IT sector deal wins contracts 2025",
            "IT companies attrition hiring trends",
            "IT sector US client spending"
        ]
        
        # Run the deep research loop for the IT sector using the provided query
        # The loop returns a list of dictionaries containing step, query, and findings
        findings = self.research_loop.run(query, "IT")
        
        # Generate the final structured markdown report based on the gathered findings
        report_text = self.report_generator.generate(findings, "IT", query)
        
        # Return the final report text
        return report_text
