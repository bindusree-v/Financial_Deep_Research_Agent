import os
import json
from dotenv import load_dotenv  # ← dotenv correct
from langchain_openai import ChatOpenAI

# Load environment variables from the .env file
load_dotenv()

class QueryAnalyzer:
    """
    A class to analyze financial research queries, identify the associated sector,
    and generate a 5-point research plan using an LLM.
    """
    
    def __init__(self):
        """
        Initializes the QueryAnalyzer.
        Loads the OPENROUTER_API_KEY from the environment and sets up the ChatOpenAI client.
        """
        print("Initializing QueryAnalyzer...")
        
        # 1. Load OPENROUTER_API_KEY from environment
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            print("Warning: OPENROUTER_API_KEY is not set. Please check your .env file.")
            
        # 3. Use ChatOpenAI class with OpenRouter base URL and the specified Claude model
        self.llm = ChatOpenAI(
            model="nvidia/nemotron-ultra-253b-v1:free", 
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.0  # Keep temperature low for structured outputs
        )
        print("QueryAnalyzer initialized with ChatOpenAI via OpenRouter.")

    def analyze(self, query: str) -> dict:
        """
        Accepts a user financial research query string as input,
        identifies the sector, and generates a structured research plan.
        
        Args:
            query (str): The user's financial research query.
            
        Returns:
            dict: A dictionary containing "sector" and "research_plan".
        """
        print(f"Analyzing query: '{query}'")
        
        # Construct the prompt requesting specific JSON structure
        prompt = f"""
You are an expert financial research assistant. Please analyze the following user query:
"{query}"

Tasks:
1. Identify which sector the query belongs to. Your answer MUST be exactly one of: "IT", "Pharma", or "Unknown".
2. Generate a research plan containing exactly 5 bullet points detailing what will be researched.

Respond ONLY with a valid JSON object in the following format, without any markdown formatting or extra text:
{{
    "sector": "Sector Name",
    "research_plan": [
        "Point 1",
        "Point 2",
        "Point 3",
        "Point 4",
        "Point 5"
    ]
}}
"""
        print("Sending prompt to LLM...")
        
        try:
            # Invoke the LLM
            response = self.llm.invoke(prompt)
            print("Received response from LLM.")
            
            # Extract content from response
            content = response.content.strip()
            
            # Clean up markdown code blocks if the LLM still returns them
            if content.startswith("```json"):
                content = content[7:]
            elif content.startswith("```"):
                content = content[3:]
            
            if content.endswith("```"):
                content = content[:-3]
                
            content = content.strip()
            
            # Parse the JSON string
            print("Parsing LLM response to dictionary...")
            result = json.loads(content)
            
            # Validate output keys
            sector = result.get("sector", "Unknown")
            research_plan = result.get("research_plan", [])
            
            # Ensure it is exactly 5 bullet points
            if len(research_plan) != 5:
                print(f"Warning: Expected exactly 5 bullet points, but got {len(research_plan)}.")
                
            print("Analysis complete.")
            
            # 4. Return dictionary with keys "sector" and "research_plan"
            return {
                "sector": sector,
                "research_plan": research_plan
            }
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from LLM response: {e}")
            print(f"Raw response was: {response.content}")
            return {
                "sector": "Unknown",
                "research_plan": []
            }
        except Exception as e:
            print(f"An error occurred during analysis: {e}")
            return {
                "sector": "Unknown",
                "research_plan": []
            }

# Simple test block to show it working if run directly
if __name__ == "__main__":
    analyzer = QueryAnalyzer()
    test_query = "What are the key drivers for Microsoft's cloud revenue growth this quarter?"
    print("\n--- Running Test ---")
    result = analyzer.analyze(test_query)
    print("\nFinal Output:")
    print(json.dumps(result, indent=2))
