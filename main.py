from scraper import scrape_programs
from rich import print
from rich.table import Table
from filters import filter_for_cs
import utils

def display_programs(programs):
    table = Table(title="DAAD Programs")

    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("Location", style="magenta")
    table.add_column("Degree")
    table.add_column("Link", style="green")

    for p in programs:
        table.add_row(p["title"], p["location"], p["degree"], p["url"])

    print(table)

if __name__ == "__main__":
    print("[yellow]Scraping...[/yellow]")
    data = scrape_programs()
    cs_programs = filter_for_cs(data)
    # display_programs(cs_programs)
    md_table = utils.create_md_table(cs_programs)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(md_table)
