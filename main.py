from scrapers.programs import scrape_programs
from scrapers.scholarships import scrape_scholarships
from utils import create_programs_md, create_scholarships_md, update_readme
from datetime import datetime


def main():
    programs = scrape_programs()
    scholarships = scrape_scholarships()

    with open("PROGRAMS.md", "w", encoding="utf-8") as f:
        f.write(create_programs_md(programs))

    with open("SCHOLARSHIPS.md", "w", encoding="utf-8") as f:
        f.write(create_scholarships_md(scholarships))

    # Update README counters
    update_readme(program_count=len(programs), scholarship_count=len(scholarships))


if __name__ == "__main__":
    main()