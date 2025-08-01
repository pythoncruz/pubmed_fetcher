import asyncio
import csv
import sys
from typing import List, Optional

import typer
from rich.console import Console

from . import processor
from .models import Paper

app = typer.Typer(add_completion=False)
console = Console()

def write_to_csv(papers: List[Paper], filename: Optional[str]):
    """Writes the list of papers to a CSV file or prints to the console."""
    if not papers:
        console.print("[yellow]No matching papers found.[/yellow]")
        return

    headers = list(Paper.model_fields.keys())
    data_rows = [p.model_dump(by_alias=True) for p in papers]

    if filename:
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data_rows)
            console.print(f"[green]Successfully wrote {len(papers)} results to {filename}[/green]")
        except IOError as e:
            console.print(f"[bold red]Error writing to file {filename}: {e}[/bold red]")
            sys.exit(1)
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data_rows)

@app.command()
def main(
    query: str = typer.Argument(..., help="The search query for PubMed."),
    file: Optional[str] = typer.Option(None, "-f", "--file", help="Filename to save the results."),
    debug: bool = typer.Option(False, "-d", "--debug", help="Print debug information."),
):
    """
    Fetches PubMed research papers with authors from pharma/biotech companies.
    """
    with console.status("[bold blue]Fetching and analyzing papers...[/]", spinner="dots"):
        papers = asyncio.run(processor.process_query(query, debug))
    
    write_to_csv(papers, file)

if __name__ == "__main__":
    app()