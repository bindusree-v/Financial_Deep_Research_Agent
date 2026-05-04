from typing import Optional, Dict, Any

def route_query(analysis_result: Dict[str, Any]) -> Optional[str]:
    """
    Routes the query to the appropriate sector agent based on the analysis result.
    
    Args:
        analysis_result (Dict[str, Any]): A dictionary containing 'sector' 
            and 'research_plan' keys.
            
    Returns:
        Optional[str]: The name of the routed sector ('IT' or 'Pharma'), 
            or None if the sector is 'Unknown'.
    """
    # Extract the sector from the input dictionary
    sector = analysis_result.get("sector")
    
    if sector == "IT":
        print("Routing to IT Sector Agent")
        return "IT"
    elif sector == "Pharma":
        print("Routing to Pharma Sector Agent")
        return "Pharma"
    elif sector == "Unknown":
        print("We're sorry, but this system currently only handles financial research for the IT and Pharma sectors.")
        return None
    else:
        # Fallback for any unexpected sector values
        print(f"We're sorry, but this system currently only handles financial research for the IT and Pharma sectors. (Unrecognized sector: {sector})")
        return None

# Simple test block to show it working if run directly
if __name__ == "__main__":
    print("\n--- Testing Router ---")
    
    print("Testing IT:")
    result_it = route_query({"sector": "IT", "research_plan": ["test"]})
    print(f"Returned: {result_it}\n")
    
    print("Testing Pharma:")
    result_pharma = route_query({"sector": "Pharma", "research_plan": ["test"]})
    print(f"Returned: {result_pharma}\n")
    
    print("Testing Unknown:")
    result_unknown = route_query({"sector": "Unknown", "research_plan": ["test"]})
    print(f"Returned: {result_unknown}")
