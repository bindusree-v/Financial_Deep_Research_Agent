import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_openai import ChatOpenAI

# Load environment variables from the .env file
load_dotenv()

class ResearchLoop:
    """
    A class that runs a 5-step recursive financial research loop.
    It uses Tavily for web search and Claude (via OpenRouter) to evaluate findings 
    and generate subsequent search queries.
    """
    
    def __init__(self):
        """
        Initializes the ResearchLoop by loading required API keys and setting up the API clients.
        """
        print("Initializing ResearchLoop...")
        
        # 1. Load OPENROUTER_API_KEY and TAVILY_API_KEY from .env file
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        
        # Add warnings if keys are missing
        if not self.tavily_api_key:
            print("Warning: TAVILY_API_KEY is not set in the environment.")
        if not self.openrouter_api_key:
            print("Warning: OPENROUTER_API_KEY is not set in the environment.")
            
        # Initialize the TavilyClient for web searching
        try:
            self.tavily_client = TavilyClient(api_key=self.tavily_api_key)
            print("TavilyClient initialized.")
        except Exception as e:
            print(f"Failed to initialize TavilyClient: {e}")
            self.tavily_client = None
            
        # Initialize the LangChain ChatOpenAI client pointing to OpenRouter
        try:
            self.llm = ChatOpenAI(
                model="claude-sonnet-4-20250514",
                api_key=self.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1",
                temperature=0.2
            )
            print("ChatOpenAI via OpenRouter initialized.")
        except Exception as e:
            print(f"Failed to initialize ChatOpenAI: {e}")
            self.llm = None

    def run_loop(self, initial_query: str, sector: str) -> List[Dict[str, Any]]:
        """
        Runs a loop of exactly 5 search steps using the provided query and sector.
        
        Args:
            initial_query (str): The starting research query.
            sector (str): The sector to focus on (e.g., "IT", "Pharma").
            
        Returns:
            List[Dict[str, Any]]: A list containing exactly 5 dictionaries with the keys:
                                  "step", "query", and "findings".
        """
        # 2. Accept initial_query and sector as arguments
        findings_log = []
        current_query = initial_query
        
        print(f"\nStarting 5-step research loop for sector: {sector}")
        print(f"Initial query: '{initial_query}'")
        
        # 3. Run a loop of exactly 5 search steps
        for step in range(1, 6):
            print(f"\n--- Step {step}/5 ---")
            
            # 4a. Search the web using Tavily with the current query
            try:
                print("Executing Tavily search...")
                # Perform a basic web search
                search_result = self.tavily_client.search(query=current_query, search_depth="basic")
                
                # Extract and format the results into a string representation
                results_list = search_result.get("results", [])
                if results_list:
                    context_pieces = [f"- {res.get('title', 'No Title')}: {res.get('content', 'No Content')}" for res in results_list]
                    findings = "\n".join(context_pieces)
                else:
                    findings = "No results found for this query."
            except Exception as e:
                print(f"Error during Tavily search on step {step}: {e}")
                findings = f"Search failed with error: {e}"
                
            # 4b. Print completion message exactly as requested
            print(f"Step {step}/5 complete — searched: {current_query}")
            
            # 4d. Store findings as a dictionary with keys: step (int), query (string), findings (string)
            findings_log.append({
                "step": step,
                "query": current_query,
                "findings": findings
            })
            
            # If we just finished the 5th step, we don't need to generate a 6th query.
            if step == 5:
                break
                
            # 4c. Use Claude via OpenRouter to read the result and generate the next search query
            try:
                print("Generating next search query with LLM...")
                prompt = f"""
You are an expert financial researcher focusing on the {sector} sector.
We are conducting an iterative 5-step search.
The original overall goal was: "{initial_query}"

We just ran step {step} with the following search query:
"{current_query}"

Here are the summarized web search findings from that step:
{findings}

Based on these findings and the original goal, what should our NEXT search query be to dig deeper, verify claims, or explore a new relevant angle?
Return ONLY the exact text for the next search query, with no quotes, no extra formatting, and no explanation.
"""
                response = self.llm.invoke(prompt)
                
                # Clean up the output to get just the query text
                next_query = response.content.strip()
                if next_query.startswith('"') and next_query.endswith('"'):
                    next_query = next_query[1:-1]
                    
                current_query = next_query
                print(f"Next query generated: '{current_query}'")
                
            except Exception as e:
                print(f"Error generating next query with LLM on step {step}: {e}")
                # Provide a safe fallback query so the loop doesn't completely crash on API failures
                current_query = f"{initial_query} deep dive part {step + 1}"
                print(f"Using fallback query: '{current_query}'")
                
        # 5. After 5 steps, return a list of all finding dicts
        print("\nResearch loop successfully completed.")
        return findings_log

# Optional block to test if executed directly
if __name__ == "__main__":
    print("To test the ResearchLoop, ensure your .env file has valid API keys.")
    # loop = ResearchLoop()
    # results = loop.run_loop("Latest trends in AI hardware", "IT")
    # print(f"Collected {len(results)} steps of findings.")
