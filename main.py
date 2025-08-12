import json
from scraper import scrape_programs
from filters import filter_by_keyword
from rich import print
from rich.table import Table
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

def scrape_or_load_data():
    try:
        with open("data/programs.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[yellow]No cache found. Scraping...[/yellow]")
        data = scrape_programs(pages=3)

    return data
    # keyword = input("Enter keyword to search (e.g. AI, engineering, bio): ")
    # results = filter_by_keyword(data, keyword)
    # display_programs(results)

if __name__ == "__main__":
    data = scrape_or_load_data()
    # utils.check_program_schema(data)
    # data = utils.sort_programs(data)
    # for prog in data:
    #     prog["category"] = utils.classify_program(prog)
    # data = utils.mark_stale_programs(data)
    md_table = utils.create_md_table([p for p in data])
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(md_table)
