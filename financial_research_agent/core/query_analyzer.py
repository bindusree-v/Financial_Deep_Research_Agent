import os
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# 2. Load GROQ_API_KEY from .env using python-dotenv
load_dotenv()

class QueryAnalyzer:
    """
    A class to analyze financial research queries and determine the sector
    along with a 5-point research plan.
    """
    
    def __init__(self):
        """
        Initializes the QueryAnalyzer. Loads the API key and sets up ChatOpenAI.
        """
        # Load the Groq API key from the environment
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("Warning: GROQ_API_KEY not found in .env file.")
            
        try:
            # 3. Use ChatGroq from langchain_groq with specified configurations
            self.llm = ChatGroq(
                model="llama-3.1-8b-instant",
                api_key=self.api_key,
                max_tokens=1000
            )
        except Exception as e:
            print(f"Failed to initialize ChatGroq: {e}")
            self.llm = None

    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Sends the query to Claude to identify the sector and create a research plan.
        """
        print("Analyzing query...")
        
        result = {
            "sector": "Unknown",
            "research_plan": []
        }
        
        if not self.llm:
            print("Error: LLM client is not initialized.")
            return result
            
        system_prompt = """You are a financial sector classifier. Respond in exactly this format:

SECTOR: IT
PLAN:
1. Short specific research point (max 15 words)
2. Short specific research point (max 15 words)
3. Short specific research point (max 15 words)
4. Short specific research point (max 15 words)
5. Short specific research point (max 15 words)

Sector classification rules:
- IT: TCS, Infosys, Wipro, HCL, Tech Mahindra = SECTOR: IT
- Pharma: Sun Pharma, Dr Reddy, Cipla, Biocon = SECTOR: Pharma
- Banking: HDFC, ICICI, SBI, Axis, Kotak = SECTOR: Banking
- Energy: Reliance, ONGC, NTPC, Power Grid, Adani = SECTOR: Energy
- FMCG: HUL, ITC, Nestle, Dabur, Britannia = SECTOR: FMCG
- Auto: Tata Motors, Maruti, Bajaj, Hero, Mahindra = SECTOR: Auto
- Telecom: Airtel, Jio, Vodafone, Vi = SECTOR: Telecom
- RealEstate: DLF, Godrej Properties, Oberoi = SECTOR: RealEstate
- Metals: Tata Steel, JSW, Hindalco, Vedanta = SECTOR: Metals
- Insurance: LIC, HDFC Life, SBI Life = SECTOR: Insurance
- Cement: UltraTech, Shree Cement, ACC, Ambuja = SECTOR: Cement
- Chemicals: Asian Paints, Pidilite, SRF, Aarti = SECTOR: Chemicals
- Consumer: Titan, Voltas, Havells, Crompton = SECTOR: Consumer
- Infrastructure: L&T, IRB, Adani Ports, GMR = SECTOR: Infrastructure
- Media: Zee, Sun TV, PVR, Inox = SECTOR: Media
- Aviation: IndiGo, Air India, SpiceJet = SECTOR: Aviation
- Retail: DMart, Trent, V-Mart, Shoppers Stop = SECTOR: Retail
- Hospitality: Indian Hotels, EIH, Lemon Tree = SECTOR: Hospitality
- Agriculture: UPL, Coromandel, PI Industries = SECTOR: Agriculture
- Defense: HAL, BEL, BEML, Mazagon Dock = SECTOR: Defense
- Non-financial queries = SECTOR: Unknown

Rules:
- Each point max 15 words, direct and specific
- No intro words like First, Next, Finally
- Start directly with the research action"""

        full_prompt = f"{system_prompt}\n\nUser Query: {query}"
        
        try:
            response = self.llm.invoke(full_prompt)
            
            content = str(response.content).strip()
            
            for line in content.split("\n"):
                line = line.strip()
                line_upper = line.upper()
                
                if line_upper.startswith("SECTOR:"):
                    extracted = line.split(":", 1)[1].strip()
                    valid_sectors = [
                        "IT", "Pharma", "Banking", "Energy", "FMCG",
                        "Auto", "Telecom", "RealEstate", "Metals", "Insurance",
                        "Cement", "Chemicals", "Consumer", "Infrastructure", "Media",
                        "Aviation", "Retail", "Hospitality", "Agriculture", "Defense"
                    ]
                    if extracted in valid_sectors:
                        result["sector"] = extracted
                    else:
                        result["sector"] = "Unknown"
                        
                elif line and line[0].isdigit() and "." in line[:3]:
                    clean = line.split(".", 1)[1].strip()
                    if clean:
                        result["research_plan"].append(clean)
                        
        except Exception as e:
            # Print error if API fails
            print(f"API Error: Failed to analyze query. Details: {e}")
            
        # Return dict with exactly the requested keys
        return result

# Optional block to test if executed directly
if __name__ == "__main__":
    analyzer = QueryAnalyzer()
    test_result = analyzer.analyze("Analyze the current state of TCS and Infosys")
    print(test_result)
