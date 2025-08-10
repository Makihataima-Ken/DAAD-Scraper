import json
from scraper import scrape_programs
from filters import filter_by_keyword
from rich import print
from rich.table import Table

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
    try:
        with open("data/programs.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[yellow]No cache found. Scraping...[/yellow]")
        data = scrape_programs(pages=3,field ="international-programs/en/")

    keyword = input("Enter keyword to search (e.g. AI, engineering, bio): ")
    results = filter_by_keyword(data, keyword)
    display_programs(results)
