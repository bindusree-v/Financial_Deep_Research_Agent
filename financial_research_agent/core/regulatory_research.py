import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

class RegulatoryResearch:
    """
    A class dedicated to researching and formatting regulatory 
    information for the 20 target financial sectors.
    """

    def __init__(self):
        """
        Initializes the RegulatoryResearch instance by loading API keys,
        setting up Tavily and Groq clients, and defining the regulation data.
        """
        # Load API keys from the environment
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        groq_api_key = os.getenv("GROQ_API_KEY")
        
        # Initialize TavilyClient for search
        self.tavily_client = TavilyClient(api_key=tavily_api_key)
        
        # Initialize LLM via ChatGroq
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=groq_api_key,
            max_tokens=500
        )
        
        # Dictionary storing bodies, key regulations, and search queries for all 20 sectors
        self.sector_regulations = {
            "IT": {
                "bodies": ["NASSCOM", "MeitY", "TRAI"],
                "key_regulations": [
                    "India Data Protection Bill 2023",
                    "IT Act 2000 amendments",
                    "Cybersecurity regulations",
                    "Digital India initiatives"
                ],
                "search_queries": [
                    "India IT sector data privacy regulations 2025",
                    "NASSCOM IT industry compliance requirements",
                    "India cybersecurity laws IT companies impact"
                ]
            },
            "Pharma": {
                "bodies": ["CDSCO", "NPPA", "FDA", "EMA"],
                "key_regulations": [
                    "Drug Price Control Order (DPCO)",
                    "FDA approval process",
                    "Good Manufacturing Practices (GMP)",
                    "Biosimilar regulations"
                ],
                "search_queries": [
                    "India pharma drug pricing regulations 2025",
                    "CDSCO drug approval process changes",
                    "India pharmaceutical export regulations"
                ]
            },
            "Banking": {
                "bodies": ["RBI", "SEBI", "IRDAI", "NHB"],
                "key_regulations": [
                    "Basel III norms",
                    "RBI repo rate decisions",
                    "NPA provisioning norms",
                    "KYC AML guidelines"
                ],
                "search_queries": [
                    "RBI banking regulations 2025 India",
                    "Basel III compliance Indian banks impact",
                    "RBI NPA guidelines banking sector"
                ]
            },
            "Energy": {
                "bodies": ["PNGRB", "CERC", "Ministry of Power", "MNRE"],
                "key_regulations": [
                    "Renewable energy targets",
                    "Carbon emission norms",
                    "Gas pricing regulations",
                    "Solar energy policies"
                ],
                "search_queries": [
                    "India energy sector regulations 2025",
                    "CERC electricity tariff regulations",
                    "India renewable energy policy changes"
                ]
            },
            "FMCG": {
                "bodies": ["FSSAI", "BIS", "Ministry of Consumer Affairs"],
                "key_regulations": [
                    "Food Safety Standards",
                    "Labeling regulations",
                    "GST on FMCG products",
                    "Plastic packaging norms"
                ],
                "search_queries": [
                    "FSSAI food safety regulations India 2025",
                    "GST impact FMCG sector India",
                    "India packaging regulations FMCG companies"
                ]
            },
            "Auto": {
                "bodies": ["MoRTH", "SIAM", "Bureau of Indian Standards"],
                "key_regulations": [
                    "BS6 emission norms",
                    "EV policy and incentives",
                    "Safety regulations",
                    "Import duty on auto parts"
                ],
                "search_queries": [
                    "India auto sector emission norms 2025",
                    "EV policy India automobile industry",
                    "SIAM automotive regulations compliance"
                ]
            },
            "Telecom": {
                "bodies": ["TRAI", "DoT", "Ministry of Communications"],
                "key_regulations": [
                    "Spectrum allocation policies",
                    "Net neutrality rules",
                    "5G rollout regulations",
                    "Interconnect usage charges"
                ],
                "search_queries": [
                    "TRAI telecom regulations India 2025",
                    "India 5G spectrum policy impact",
                    "DoT telecom compliance requirements"
                ]
            },
            "RealEstate": {
                "bodies": ["RERA", "Ministry of Housing", "NHB"],
                "key_regulations": [
                    "RERA compliance",
                    "Stamp duty regulations",
                    "Affordable housing policies",
                    "FDI in real estate"
                ],
                "search_queries": [
                    "RERA real estate regulations India 2025",
                    "India housing policy changes impact",
                    "FDI real estate sector India regulations"
                ]
            },
            "Metals": {
                "bodies": ["Ministry of Steel", "IBM", "MOEF"],
                "key_regulations": [
                    "Steel import duties",
                    "Mining regulations",
                    "Environmental clearances",
                    "Carbon emission norms"
                ],
                "search_queries": [
                    "India steel sector regulations 2025",
                    "Mining regulations India metals companies",
                    "Environmental norms India metals sector"
                ]
            },
            "Insurance": {
                "bodies": ["IRDAI", "Ministry of Finance"],
                "key_regulations": [
                    "Solvency margin requirements",
                    "FDI in insurance",
                    "Crop insurance schemes",
                    "Health insurance regulations"
                ],
                "search_queries": [
                    "IRDAI insurance regulations India 2025",
                    "FDI insurance sector India impact",
                    "India health insurance policy changes"
                ]
            },
            "Cement": {
                "bodies": ["Ministry of Commerce", "CCI", "Bureau of Indian Standards"],
                "key_regulations": [
                    "Competition Commission guidelines",
                    "Environmental emission norms",
                    "Quality standards BIS",
                    "Import export duties"
                ],
                "search_queries": [
                    "India cement sector regulations 2025",
                    "CCI cement industry competition rules",
                    "Environmental norms cement companies India"
                ]
            },
            "Chemicals": {
                "bodies": ["Ministry of Chemicals", "CPCB", "DCGI"],
                "key_regulations": [
                    "Chemical safety regulations",
                    "Environmental pollution norms",
                    "Export import regulations",
                    "Hazardous chemical handling"
                ],
                "search_queries": [
                    "India chemicals sector regulations 2025",
                    "CPCB environmental norms chemicals industry",
                    "India chemical export regulations impact"
                ]
            },
            "Consumer": {
                "bodies": ["Ministry of Consumer Affairs", "BIS", "CCPA"],
                "key_regulations": [
                    "Consumer Protection Act 2019",
                    "E-commerce regulations",
                    "Product quality standards",
                    "Advertising standards"
                ],
                "search_queries": [
                    "India consumer protection regulations 2025",
                    "CCPA consumer goods compliance",
                    "India e-commerce regulations consumer sector"
                ]
            },
            "Infrastructure": {
                "bodies": ["NHAI", "Ministry of Road Transport", "PPP Authority"],
                "key_regulations": [
                    "PPP policy framework",
                    "Toll regulation",
                    "Land acquisition laws",
                    "Environmental clearances"
                ],
                "search_queries": [
                    "India infrastructure regulations 2025",
                    "NHAI highway project regulations",
                    "PPP infrastructure policy India changes"
                ]
            },
            "Media": {
                "bodies": ["MIB", "TRAI", "Press Council of India"],
                "key_regulations": [
                    "Content regulation guidelines",
                    "OTT platform regulations",
                    "FDI in media",
                    "Broadcasting standards"
                ],
                "search_queries": [
                    "India media sector regulations 2025",
                    "OTT platform rules India impact",
                    "FDI media broadcasting India regulations"
                ]
            },
            "Aviation": {
                "bodies": ["DGCA", "AAI", "Ministry of Civil Aviation"],
                "key_regulations": [
                    "UDAN regional connectivity scheme",
                    "Aircraft maintenance regulations",
                    "Slot allocation policies",
                    "Open sky agreements"
                ],
                "search_queries": [
                    "DGCA aviation regulations India 2025",
                    "India open sky policy aviation impact",
                    "UDAN scheme aviation sector regulations"
                ]
            },
            "Retail": {
                "bodies": ["Ministry of Commerce", "DPIIT", "CCI"],
                "key_regulations": [
                    "FDI in retail",
                    "E-commerce regulations",
                    "GST on retail",
                    "Consumer protection rules"
                ],
                "search_queries": [
                    "India retail sector regulations 2025",
                    "FDI retail policy India impact",
                    "E-commerce regulations India retail companies"
                ]
            },
            "Hospitality": {
                "bodies": ["Ministry of Tourism", "FSSAI", "State Tourism Boards"],
                "key_regulations": [
                    "Hotel classification norms",
                    "Food safety standards",
                    "GST on hospitality",
                    "Foreign tourist visa policies"
                ],
                "search_queries": [
                    "India hospitality sector regulations 2025",
                    "GST hospitality hotels India impact",
                    "Tourism policy India hotel industry"
                ]
            },
            "Agriculture": {
                "bodies": ["Ministry of Agriculture", "APEDA", "FCI"],
                "key_regulations": [
                    "MSP policies",
                    "Farm laws",
                    "Export restrictions",
                    "Pesticide regulations"
                ],
                "search_queries": [
                    "India agriculture sector regulations 2025",
                    "MSP policy changes India farming",
                    "India crop export regulations impact"
                ]
            },
            "Defense": {
                "bodies": ["Ministry of Defence", "DRDO", "DDP"],
                "key_regulations": [
                    "Defence Acquisition Procedure (DAP)",
                    "Atmanirbhar Bharat defence policy",
                    "FDI in defence",
                    "Offset policy"
                ],
                "search_queries": [
                    "India defence sector regulations 2025",
                    "Atmanirbhar Bharat defence policy impact",
                    "FDI defence sector India changes"
                ]
            }
        }

    def research(self, sector: str, query: str) -> str:
        """
        Executes search queries for the given sector and summarizes the findings 
        using the LLM into a concise regulatory overview.
        
        Args:
            sector (str): The sector to research.
            query (str): The specific user query context.
            
        Returns:
            str: Summarized regulatory findings from the LLM.
        """
        try:
            # Check if sector exists in our data
            sector_data = self.sector_regulations.get(sector)
            if not sector_data:
                return "No regulatory data available for this sector"
                
            # Get search queries and limit to max 2 searches to save API calls
            queries_to_run = sector_data.get("search_queries", [])[:2]
            
            combined_search_results = ""
            
            # Execute searches
            for search_query in queries_to_run:
                print(f"Searching regulatory info: {search_query}")
                results = self.tavily_client.search(search_query, max_results=2)
                
                if results and "results" in results:
                    for r in results["results"]:
                        combined_search_results += r.get("content", "") + "\n"
                        
            if not combined_search_results.strip():
                combined_search_results = "No fresh regulatory data found online."
                
            # Formulate the prompt for the LLM
            prompt = f"""You are a financial regulatory expert. Summarize these regulatory findings for the {sector} sector:

Search Results:
{combined_search_results[:1500]}

Please provide a concise summary covering these exact sections:
1. Key regulatory bodies
2. Current regulations affecting sector
3. Recent regulatory changes
4. Impact on companies

Return only the summary. Do not add any introductory or concluding remarks."""

            # Generate the summary
            response = self.llm.invoke([HumanMessage(content=prompt)])
            summary = str(response.content).strip()
            
            print(f"Regulatory research complete for {sector} sector")
            return summary
            
        except Exception as e:
            print(f"Error during regulatory research for {sector}: {e}")
            return "Error retrieving regulatory data."

    def format_for_report(self, regulatory_summary: str, sector: str) -> str:
        """
        Formats the regulatory summary into a Markdown section.
        
        Args:
            regulatory_summary (str): The summary generated by the LLM.
            sector (str): The sector in question.
            
        Returns:
            str: Formatted Markdown string.
        """
        try:
            sector_data = self.sector_regulations.get(sector, {})
            bodies = sector_data.get("bodies", ["Various Bodies"])
            bodies_str = ", ".join(bodies)
            
            report_section = f"\n## Regulatory Environment\n\n"
            report_section += f"**Key Regulatory Bodies:** {bodies_str}\n\n"
            
            if regulatory_summary and regulatory_summary != "No regulatory data available for this sector":
                report_section += f"{regulatory_summary}\n"
            else:
                report_section += "No regulatory data gathered.\n"
                
            return report_section
            
        except Exception as e:
            print(f"Error formatting regulatory report: {e}")
            return "\n## Regulatory Environment\n\nError formatting regulatory data.\n"
