"""
Metals Agent module for the Financial Research Agent.
This agent is responsible for handling queries specific to the Metals sector.
"""

# Import the ResearchLoop to gather data and findings
from core.research_loop import ResearchLoop

# Import the ReportGenerator to compile the findings into a report
from core.report_generator import ReportGenerator

class MetalsAgent:
    """
    Agent responsible for managing and executing research tasks 
    specifically for the Metals sector.
    """
    
    def __init__(self):
        """
        Initializes the MetalsAgent by setting up its dependencies.
        It instantiates the ResearchLoop and ReportGenerator.
        """
        # Initialize the research loop to fetch data
        self.research_loop = ResearchLoop()
        
        # Initialize the report generator to format the final output
        self.report_generator = ReportGenerator()
        
        # Notify that the agent has been successfully initialized
        print("Metals Sector Agent initialized")

    def run(self, query: str) -> str:
        """
        Executes the deep research and generates a report for the given query.
        
        Args:
            query (str): The user's query about the Metals sector.
            
        Returns:
            str: The generated markdown report containing the research findings.
        """
        # Notify that the deep research process is beginning
        print("Metals Agent starting deep research...")
        
        # Run the research loop for the query and specify the "Metals" sector
        findings = self.research_loop.run(query, "Metals")
        
        # Generate a final markdown report using the gathered findings
        report = self.report_generator.generate(findings, "Metals", query)
        
        # Return the generated report text
        return report
