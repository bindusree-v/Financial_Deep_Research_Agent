import sys

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.text import Text
from rich import print as rprint
from rich.rule import Rule
from rich.prompt import Prompt, Confirm

from agents.it_agent import ITAgent
from agents.pharma_agent import PharmaAgent
from agents.banking_agent import BankingAgent
from agents.energy_agent import EnergyAgent
from agents.fmcg_agent import FMCGAgent
from agents.auto_agent import AutoAgent
from agents.telecom_agent import TelecomAgent
from agents.realestate_agent import RealEstateAgent
from agents.metals_agent import MetalsAgent
from agents.insurance_agent import InsuranceAgent
from agents.cement_agent import CementAgent
from agents.chemicals_agent import ChemicalsAgent
from agents.consumer_agent import ConsumerAgent
from agents.infrastructure_agent import InfrastructureAgent
from agents.media_agent import MediaAgent
from agents.aviation_agent import AviationAgent
from agents.retail_agent import RetailAgent
from agents.hospitality_agent import HospitalityAgent
from agents.agriculture_agent import AgricultureAgent
from agents.defense_agent import DefenseAgent

console = Console()

def main():
    console.print(Panel.fit(
        "[bold cyan]Financial Deep Research Agent[/bold cyan]\n"
        "[dim]Powered by AI | 20 Sectors | Real-time Data[/dim]",
        border_style="cyan"
    ))

    query = Prompt.ask("\n[bold yellow]Enter your financial research query[/bold yellow]")

    try:
        from core.query_analyzer import QueryAnalyzer
        analyzer = QueryAnalyzer()
        
        with console.status("[bold green]Analyzing query...[/bold green]", spinner="dots"):
            analysis_result = analyzer.analyze(query)
            
        sector = analysis_result.get("sector", "Unknown")
        research_plan = analysis_result.get("research_plan", [])
        
        sector_colors = {
            "IT": "blue", "Pharma": "green", "Banking": "yellow",
            "Energy": "orange3", "FMCG": "magenta", "Auto": "cyan",
            "Telecom": "bright_blue", "RealEstate": "bright_green",
            "Metals": "bright_red", "Insurance": "bright_magenta",
            "Cement": "grey70", "Chemicals": "bright_yellow",
            "Consumer": "bright_cyan", "Infrastructure": "bright_white",
            "Media": "purple", "Aviation": "sky_blue1",
            "Retail": "pink1", "Hospitality": "gold1",
            "Agriculture": "dark_green", "Defense": "dark_red"
        }
        
        if sector == "Unknown":
            console.print(Panel(
                "[bold red]Query Outside Scope[/bold red]\n"
                "[dim]This system handles IT, Pharma, Banking, Energy, FMCG,\n"
                "Auto, Telecom, RealEstate, Metals, Insurance, Cement,\n"
                "Chemicals, Consumer, Infrastructure, Media, Aviation,\n"
                "Retail, Hospitality, Agriculture, Defense[/dim]",
                border_style="red"
            ))
            sys.exit(0)
            
        color = sector_colors.get(sector, "white")
        console.print(f"\n[bold {color}]Sector Identified: {sector}[/bold {color}]\n")
        
        if research_plan:
            table = Table(title="Research Plan", border_style="cyan", show_lines=True)
            table.add_column("Step", style="bold cyan", width=6)
            table.add_column("Research Point", style="white")
            for i, point in enumerate(research_plan, 1):
                table.add_row(str(i), point)
            console.print(table)
        else:
            console.print("[dim]No research plan generated.[/dim]")
            
    except Exception as e:
        console.print(f"\n[bold red]Error analyzing query: {str(e)}[/bold red]")
        sys.exit(1)

    proceed = Confirm.ask("\n[bold]Proceed with this research plan?[/bold]")
    if not proceed:
        console.print("[red]Research cancelled.[/red]")
        sys.exit(0)
        
    console.print(Rule(f"[bold cyan]Starting {sector} Sector Research[/bold cyan]"))
    
    try:
        from core.router import route_query

        agent_map = {
            "IT": ITAgent,
            "Pharma": PharmaAgent,
            "Banking": BankingAgent,
            "Energy": EnergyAgent,
            "FMCG": FMCGAgent,
            "Auto": AutoAgent,
            "Telecom": TelecomAgent,
            "RealEstate": RealEstateAgent,
            "Metals": MetalsAgent,
            "Insurance": InsuranceAgent,
            "Cement": CementAgent,
            "Chemicals": ChemicalsAgent,
            "Consumer": ConsumerAgent,
            "Infrastructure": InfrastructureAgent,
            "Media": MediaAgent,
            "Aviation": AviationAgent,
            "Retail": RetailAgent,
            "Hospitality": HospitalityAgent,
            "Agriculture": AgricultureAgent,
            "Defense": DefenseAgent
        }

        routed_sector = route_query(analysis_result)

        if routed_sector is None:
            console.print("[bold red]Cannot process this query.[/bold red]")
        else:
            AgentClass = agent_map.get(routed_sector)
            if AgentClass:
                agent = AgentClass()
                agent.run(query)
                console.print("\n")
                console.print(Panel(
                    f"[bold green]Research Complete![/bold green]\n"
                    f"[dim]Report saved in reports/ folder[/dim]",
                    border_style="green"
                ))
            else:
                console.print(f"[bold red]No agent found for sector: {routed_sector}[/bold red]")
        
    except Exception as e:
        console.print(f"\n[bold red]Error during agent execution: {str(e)}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()