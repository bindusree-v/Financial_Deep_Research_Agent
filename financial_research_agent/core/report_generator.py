import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

class ReportGenerator:
    def __init__(self):
        # Load API key from environment
        groq_api_key = os.getenv("GROQ_API_KEY")
        
        # Initialize LLM via ChatGroq
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=groq_api_key,
            max_tokens=1000
        )

    def generate(self, findings: list, sector: str, query: str) -> str:
        
        # Separate financial data from research findings
        financial_data = ""
        research_findings = ""
        regulatory_data = ""
        
        for f in findings:
            if f["step"] == 0:
                financial_data = f["findings"]
            elif f["step"] == -1:
                regulatory_data = f["findings"]
            else:
                research_findings += f"Step {f['step']}:\nQuery: {f['query']}\nFindings: {f['findings'][:500]}\n\n"
        
        # Build comprehensive prompt
        prompt = f"""You are a senior financial research analyst. Write a professional markdown report.

Original Query: {query}
Sector: {sector}

REAL FINANCIAL DATA (use these exact numbers in report):
{financial_data}

REGULATORY ENVIRONMENT DATA:
{regulatory_data}

RESEARCH FINDINGS FROM WEB:
{research_findings[:2000]}

Write a comprehensive markdown report with EXACTLY these sections:

# Financial Research Report: {query}

## Executive Summary
(3-4 sentences summarizing key findings)

## Company Financial Metrics
(Use the real financial data provided above - include actual numbers for price, revenue, P/E ratio etc)

## Key Research Findings
(Bullet points from web research - minimum 5 points)

## Sector Trends & Insights
(3-4 trends identified from research)

## Regulatory Environment
(Use regulatory data provided - list key regulations and their impact)

## Risk Factors
(3-4 key risks)

## Investment Outlook
(Brief outlook based on data)

## Sources
(List all search queries used as sources)

Make the report detailed, professional, and data-driven.
Use actual numbers from financial data section."""

        # Call LLM
        from langchain_core.messages import HumanMessage
        response = self.llm.invoke([HumanMessage(content=prompt)])
        report_text = response.content.strip()
        
        # Fallback if empty
        if not report_text:
            report_text = f"# Financial Research Report\n\n## Query\n{query}\n\n## Financial Data\n{financial_data}\n\n## Findings\n{research_findings}"
        
        # Save report
        os.makedirs("reports", exist_ok=True)
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"reports/{date_str}_{sector.lower()}_report.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_text)
        
        print(f"Report saved at: {filename}")
        return report_text
