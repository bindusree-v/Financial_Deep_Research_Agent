import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from data_sources.financial_api import FinancialDataFetcher
from data_sources.rag_system import RAGSystem
from core.regulatory_research import RegulatoryResearch

load_dotenv()

class ResearchLoop:
    def __init__(self):
        # Load API keys from environment
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        groq_api_key = os.getenv("GROQ_API_KEY")
        
        # Initialize TavilyClient
        self.tavily_client = TavilyClient(api_key=tavily_api_key)
        
        # Initialize LLM via ChatGroq
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=groq_api_key,
            max_tokens=1000
        )
        
        self.financial_api = FinancialDataFetcher()
        self.rag = RAGSystem()
        self.rag.load_documents("documents")
        self.regulatory = RegulatoryResearch()

    def extract_tickers(self, query: str, sector: str) -> list:
        
        ticker_map = {
            "IT": {
                "tcs": "TCS.NS", "infosys": "INFY.NS", "infy": "INFY.NS",
                "wipro": "WIPRO.NS", "hcl": "HCLTECH.NS",
                "tech mahindra": "TECHM.NS", "techm": "TECHM.NS"
            },
            "Pharma": {
                "sun pharma": "SUNPHARMA.NS", "sunpharma": "SUNPHARMA.NS",
                "dr reddy": "DRREDDY.NS", "drreddy": "DRREDDY.NS",
                "cipla": "CIPLA.NS", "biocon": "BIOCON.NS", "lupin": "LUPIN.NS"
            },
            "Banking": {
                "hdfc": "HDFCBANK.NS", "icici": "ICICIBANK.NS",
                "sbi": "SBIN.NS", "axis": "AXISBANK.NS",
                "kotak": "KOTAKBANK.NS"
            },
            "Energy": {
                "reliance": "RELIANCE.NS", "ongc": "ONGC.NS",
                "ntpc": "NTPC.NS", "power grid": "POWERGRID.NS",
                "adani": "ADANIGREEN.NS"
            },
            "FMCG": {
                "hul": "HINDUNILVR.NS", "itc": "ITC.NS",
                "nestle": "NESTLEIND.NS", "dabur": "DABUR.NS",
                "britannia": "BRITANNIA.NS"
            },
            "Auto": {
                "tata motors": "TATAMOTORS.NS", "maruti": "MARUTI.NS",
                "bajaj": "BAJAJ-AUTO.NS", "hero": "HEROMOTOCO.NS",
                "mahindra": "M&M.NS"
            },
            "Telecom": {
                "airtel": "BHARTIARTL.NS", "jio": "RELIANCE.NS",
                "vi": "IDEA.NS", "vodafone": "IDEA.NS"
            },
            "RealEstate": {
                "dlf": "DLF.NS", "godrej": "GODREJPROP.NS",
                "oberoi": "OBEROIRLTY.NS", "prestige": "PRESTIGE.NS"
            },
            "Metals": {
                "tata steel": "TATASTEEL.NS", "jsw": "JSWSTEEL.NS",
                "hindalco": "HINDALCO.NS", "vedanta": "VEDL.NS"
            },
            "Insurance": {
                "lic": "LICI.NS", "hdfc life": "HDFCLIFE.NS",
                "sbi life": "SBILIFE.NS", "icici prudential": "ICICIPRULI.NS"
            },
            "Cement": {
                "ultratech": "ULTRACEMCO.NS",
                "shree cement": "SHREECEM.NS",
                "acc": "ACC.NS",
                "ambuja": "AMBUJACEM.NS"
            },
            "Chemicals": {
                "asian paints": "ASIANPAINT.NS",
                "pidilite": "PIDILITIND.NS",
                "srf": "SRF.NS",
                "aarti": "AARTIIND.NS"
            },
            "Consumer": {
                "titan": "TITAN.NS",
                "voltas": "VOLTAS.NS",
                "havells": "HAVELLS.NS",
                "crompton": "CROMPTON.NS"
            },
            "Infrastructure": {
                "larsen": "LT.NS",
                "l&t": "LT.NS",
                "irb": "IRB.NS",
                "adani ports": "ADANIPORTS.NS",
                "gmr": "GMRINFRA.NS"
            },
            "Media": {
                "zee": "ZEEL.NS",
                "sun tv": "SUNTV.NS",
                "pvr": "PVRINOX.NS",
                "inox": "PVRINOX.NS"
            },
            "Aviation": {
                "indigo": "INDIGO.NS",
                "interglobe": "INDIGO.NS",
                "spicejet": "SPICEJET.NS"
            },
            "Retail": {
                "dmart": "DMART.NS",
                "avenue supermarts": "DMART.NS",
                "trent": "TRENT.NS",
                "shoppers stop": "SHOPERSTOP.NS"
            },
            "Hospitality": {
                "indian hotels": "INDHOTEL.NS",
                "taj": "INDHOTEL.NS",
                "eih": "EIHOTEL.NS",
                "lemon tree": "LEMONTREE.NS"
            },
            "Agriculture": {
                "upl": "UPL.NS",
                "coromandel": "COROMANDEL.NS",
                "pi industries": "PIIND.NS"
            },
            "Defense": {
                "hal": "HAL.NS",
                "bel": "BEL.NS",
                "beml": "BEML.NS",
                "mazagon": "MAZDOCK.NS"
            }
        }
        
        default_tickers = {
            "IT": ["TCS.NS", "INFY.NS", "WIPRO.NS"],
            "Pharma": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS"],
            "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS"],
            "Energy": ["RELIANCE.NS", "ONGC.NS", "NTPC.NS"],
            "FMCG": ["HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS"],
            "Auto": ["TATAMOTORS.NS", "MARUTI.NS", "BAJAJ-AUTO.NS"],
            "Telecom": ["BHARTIARTL.NS", "RELIANCE.NS", "IDEA.NS"],
            "RealEstate": ["DLF.NS", "GODREJPROP.NS", "OBEROIRLTY.NS"],
            "Metals": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS"],
            "Insurance": ["LICI.NS", "HDFCLIFE.NS", "SBILIFE.NS"],
            "Cement": ["ULTRACEMCO.NS", "SHREECEM.NS", "ACC.NS"],
            "Chemicals": ["ASIANPAINT.NS", "PIDILITIND.NS", "SRF.NS"],
            "Consumer": ["TITAN.NS", "VOLTAS.NS", "HAVELLS.NS"],
            "Infrastructure": ["LT.NS", "ADANIPORTS.NS", "IRB.NS"],
            "Media": ["ZEEL.NS", "SUNTV.NS", "PVRINOX.NS"],
            "Aviation": ["INDIGO.NS", "SPICEJET.NS"],
            "Retail": ["DMART.NS", "TRENT.NS", "SHOPERSTOP.NS"],
            "Hospitality": ["INDHOTEL.NS", "EIHOTEL.NS", "LEMONTREE.NS"],
            "Agriculture": ["UPL.NS", "COROMANDEL.NS", "PIIND.NS"],
            "Defense": ["HAL.NS", "BEL.NS", "BEML.NS"]
        }
        
        query_lower = query.lower()
        found_tickers = []
        
        sector_tickers = ticker_map.get(sector, {})
        defaults = default_tickers.get(sector, ["TCS.NS", "INFY.NS"])
        
        for company, ticker in sector_tickers.items():
            if company in query_lower:
                if ticker not in found_tickers:
                    found_tickers.append(ticker)
        
        if not found_tickers:
            return defaults
        
        if len(found_tickers) == 1:
            for t in defaults:
                if t not in found_tickers:
                    found_tickers.append(t)
                    break
        
        print(f"Tickers identified: {found_tickers}")
        return found_tickers[:3]

    def run(self, query: str, sector: str) -> list:
        findings_list = []
        current_query = query
        seen_queries = set()
        
        print(f"\nStarting deep research for: {query}")
        print("="*50)
        
        # Financial Data Fetching
        tickers = self.extract_tickers(query, sector)
        stock_data = self.financial_api.get_multiple_stocks(tickers)
        formatted_financial_data = self.financial_api.format_for_report(stock_data)
        
        print(f"Financial data fetched for: {tickers}")
        
        findings_list.append({
            "step": 0,
            "query": "Financial API Data",
            "findings": formatted_financial_data
        })
        
        try:
            print("\nFetching regulatory research...")
            regulatory_summary = self.regulatory.research(sector, query)
            findings_list.append({
                "step": -1,
                "query": "Regulatory Research",
                "findings": regulatory_summary
            })
            print("Regulatory research added.")
        except Exception as e:
            print(f"Regulatory research failed: {e}")
        
        for step in range(1, 11):
            try:
                # Avoid duplicate queries
                if current_query in seen_queries:
                    current_query = f"{sector} sector latest news {step}"
                seen_queries.add(current_query)
                
                print(f"\nStep {step}/10 - Searching: {current_query}")
                
                # Search using tavily
                results = self.tavily_client.search(current_query, max_results=3)
                
                # Extract text safely
                findings_text = ""
                if results and "results" in results:
                    for r in results["results"]:
                        findings_text += r.get("content", "") + "\n"
                
                if not findings_text:
                    findings_text = "No results found for this query"
                
                # Query RAG for internal knowledge
                rag_result = self.rag.query(current_query)
                if rag_result and "No " not in rag_result:
                    findings_text += f"\nFrom Annual Reports:\n{rag_result}"
                
                # Store finding
                findings_list.append({
                    "step": step,
                    "query": current_query,
                    "findings": findings_text[:800]
                })
                
                print(f"Step {step}/10 complete")
                
                # Generate next query based on findings
                if step < 10:
                    prompt = f"""You are a financial research assistant analyzing the {sector} sector.

Based on these findings:
{findings_text[:400]}

Current research topic: {current_query}
Already searched: {list(seen_queries)}

Generate ONE specific follow-up search query to dig deeper into a NEW aspect not yet covered.
Focus on: financial metrics, company performance, market trends, regulations, or competitor analysis.
Return ONLY the search query, nothing else, no quotes, no explanation."""

                    response = self.llm.invoke([HumanMessage(content=prompt)])
                    next_query = response.content.strip().strip('"').strip("'")
                    
                    if len(next_query) > 10 and next_query not in seen_queries:
                        current_query = next_query
                    else:
                        fallbacks = [
                            f"{sector} sector revenue growth 2025",
                            f"{sector} companies market share India",
                            f"{sector} sector regulatory changes 2025",
                            f"{sector} sector AI adoption trends",
                            f"{sector} sector employee attrition",
                            f"{sector} sector deal wins contracts",
                            f"{sector} sector global expansion",
                            f"{sector} sector profit margins analysis"
                        ]
                        current_query = fallbacks[step % len(fallbacks)]
                        
            except Exception as e:
                print(f"Error in step {step}: {e}")
                continue
        
        print("\n" + "="*50)
        research_steps = len([f for f in findings_list if f["step"] > 0])
        print(f"Research complete! {research_steps} steps completed.")
        return findings_list
