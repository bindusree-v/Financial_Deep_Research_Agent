"""
Banking Agent module for the Financial Research Agent.
This agent is responsible for handling queries specific to the Banking sector.
"""

# Import the ResearchLoop to gather data and findings
from core.research_loop import ResearchLoop

# Import the ReportGenerator to compile the findings into a report
from core.report_generator import ReportGenerator

class BankingAgent:
    """
    Agent responsible for managing and executing research tasks 
    specifically for the Banking sector.
    """
    
    def __init__(self):
        """
        Initializes the BankingAgent by setting up its dependencies.
        It instantiates the ResearchLoop and ReportGenerator.
        """
        # Initialize the research loop to fetch data
        self.research_loop = ResearchLoop()
        
        # Initialize the report generator to format the final output
        self.report_generator = ReportGenerator()
        
        # Notify that the agent has been successfully initialized
        print("Banking Sector Agent initialized")

    def run(self, query: str) -> str:
        """
        Executes the deep research and generates a report for the given query.
        
        Args:
            query (str): The user's query about the banking sector.
            
        Returns:
            str: The generated markdown report containing the research findings.
        """
        # Notify that the deep research process is beginning
        print("Banking Agent starting deep research...")
        
        # Run the research loop for the query and specify the "Banking" sector
        findings = self.research_loop.run(query, "Banking")
        
        # Generate a final markdown report using the gathered findings
        report = self.report_generator.generate(findings, "Banking", query)
        
        # Return the generated report text
        return report
