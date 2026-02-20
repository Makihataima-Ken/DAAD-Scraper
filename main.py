from filters import filter_for_cs
    
from scrapers.programs import scrape_programs
from scrapers.scholarships import scrape_scholarships
from utils import create_programs_md, create_scholarships_md

def create_programs_table():
    programs = scrape_programs()
    cs_programs = filter_for_cs(programs)
    return create_programs_md(cs_programs)

def create_scholarships_table():
    scholarships = scrape_scholarships()
    return create_scholarships_md(scholarships)

def main():

    # programs_table = create_programs_table()
    scholarships_table = create_scholarships_table()
    
    # with open("PROGRAMS.md", "w", encoding="utf-8") as f:
    #     f.write(programs_table)

    with open("SCHOLARSHIPS.md", "w", encoding="utf-8") as f:
        f.write(scholarships_table)

if __name__ == "__main__":
    main()
