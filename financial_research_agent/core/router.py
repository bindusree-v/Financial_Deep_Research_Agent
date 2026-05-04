def route_query(analysis_result: dict) -> str | None:
    sector = analysis_result.get("sector", "Unknown")
    
    valid_sectors = [
        "IT", "Pharma", "Banking", "Energy", "FMCG",
        "Auto", "Telecom", "RealEstate", "Metals", "Insurance",
        "Cement", "Chemicals", "Consumer", "Infrastructure", "Media",
        "Aviation", "Retail", "Hospitality", "Agriculture", "Defense"
    ]
    
    if sector in valid_sectors:
        print(f"Routing to {sector} Sector Agent")
        return sector
    else:
        print("Sorry, this system only handles financial research for:")
        print("IT, Pharma, Banking, Energy, FMCG, Auto, Telecom,")
        print("RealEstate, Metals, Insurance, Cement, Chemicals,")
        print("Consumer, Infrastructure, Media, Aviation, Retail,")
        print("Hospitality, Agriculture, Defense")
        return None
