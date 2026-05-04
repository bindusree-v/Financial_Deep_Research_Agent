import os
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from the .env file
load_dotenv()

class ReportGenerator:
    """
    A class designed to synthesize raw research findings into a well-structured, 
    professional markdown report using an LLM.
    """
    
    def __init__(self):
        """
        Initializes the ReportGenerator.
        Loads the OPENROUTER_API_KEY from the environment and sets up the ChatOpenAI client.
        """
        print("Initializing ReportGenerator...")
        
        # 1. Load OPENROUTER_API_KEY from the .env file
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            print("Warning: OPENROUTER_API_KEY is not set in the environment.")
            
        # Set up the LangChain ChatOpenAI client pointing to OpenRouter
        try:
            self.llm = ChatOpenAI(
                model="claude-sonnet-4-20250514",
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1",
                temperature=0.3 # Low temperature for structured, factual reporting
            )
            print("ChatOpenAI via OpenRouter initialized for report generation.")
        except Exception as e:
            print(f"Failed to initialize ChatOpenAI: {e}")
            self.llm = None

    def generate_report(self, findings: List[Dict[str, Any]], sector: str, original_query: str) -> str:
        """
        Generates a comprehensive markdown report from the given research findings.
        
        Args:
            findings (List[Dict[str, Any]]): List of finding dicts (keys: step, query, findings).
            sector (str): The researched sector (e.g., 'IT', 'Pharma').
            original_query (str): The initial user query that started the research.
            
        Returns:
            str: The raw text of the generated markdown report.
        """
        # 2. Accept findings, sector, and original_query
        print(f"\nGenerating '{sector}' report for query: '{original_query}'")
        
        # Format the structured findings into a string for the LLM prompt
        findings_text = ""
        for item in findings:
            step = item.get("step", "Unknown")
            query = item.get("query", "Unknown query")
            content = item.get("findings", "No findings recorded.")
            
            # Combine them in a readable format
            findings_text += f"--- Step {step} ---\n"
            findings_text += f"Query: {query}\n"
            findings_text += f"Findings: {content}\n\n"

        # 3. Use Claude via OpenRouter to synthesize all findings into a structured markdown report
        # 4. Report must have specific sections exactly as requested
        prompt = f"""
You are an expert financial analyst. Please write a comprehensive Markdown report on the "{sector}" sector.
The original goal for this research was: "{original_query}"

Below are the iterative research findings:
{findings_text}

Please synthesize these findings into a highly professional Markdown report.
Your report MUST contain exactly the following sections with these exact headings:

# Executive Summary
(Write exactly 3-4 sentences summarizing the most critical takeaways.)

# Key Findings
(Use bullet points to detail the main factual discoveries from the research.)

# Sector Insights
(Analyze the broader trends, opportunities, or risks noticed within the {sector} sector based on the findings.)

# Limitations
(State what was NOT covered or what gaps remain based on the findings provided.)

# Sources
(List all the queries that were used to gather this information, as a bulleted list.)

Start your response immediately with the "# Executive Summary" heading. Do not include conversational filler.
"""
        
        print("Sending findings to LLM for report synthesis...")
        try:
            # Generate the report text
            response = self.llm.invoke(prompt)
            report_content = response.content.strip()
            
            # Clean up markdown code block tags if the LLM includes them
            if report_content.startswith("```markdown"):
                report_content = report_content[11:]
            elif report_content.startswith("```"):
                report_content = report_content[3:]
                
            if report_content.endswith("```"):
                report_content = report_content[:-3]
                
            report_content = report_content.strip()
            print("Report successfully synthesized.")
            
        except Exception as e:
            print(f"Error during LLM report generation: {e}")
            report_content = f"# Error Generating Report\nAn error occurred: {e}"
            
        # 5. Create a folder called "reports" if it does not exist
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            try:
                os.makedirs(reports_dir)
                print(f"Created directory: '{reports_dir}'")
            except Exception as e:
                print(f"Error creating directory '{reports_dir}': {e}")
                
        # 6. Save the report as "reports/YYYY-MM-DD_sector_report.md"
        today_date = datetime.now().strftime("%Y-%m-%d")
        
        # Clean up sector string to be filesystem-safe
        clean_sector = sector.lower().replace(" ", "_").replace("/", "_")
        filename = f"{today_date}_{clean_sector}_report.md"
        file_path = os.path.join(reports_dir, filename)
        
        # Write the generated content to the markdown file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(report_content)
            # 7. Print the saved file path
            print(f"Success! Report saved to: {os.path.abspath(file_path)}")
        except Exception as e:
            print(f"Error saving report to '{file_path}': {e}")
            
        # 8. Return the report text as string
        return report_content

# Optional block to test if executed directly
if __name__ == "__main__":
    print("ReportGenerator test block. (Requires valid OPENROUTER_API_KEY)")
    # generator = ReportGenerator()
    # test_findings = [
    #     {"step": 1, "query": "Test search 1", "findings": "The sector is growing by 5%."},
    #     {"step": 2, "query": "Test search 2", "findings": "New regulations are expected soon."}
    # ]
    # generator.generate_report(test_findings, "IT", "What is the future of the IT sector?")
