from datetime import datetime
import time
import random

from rich import print
from rich.table import Table

def delay_random(min_seconds=2, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def check_program_schema(programs):
    required_fields = ["id", "university", "title", "degree", "location", "url"]
    for prog in programs:
        for field in required_fields:
            if field not in prog or not prog[field]:
                raise ValueError(f"Program {prog.get('id')} missing required field '{field}'")

def sort_programs(programs):
    return sorted(programs, key=lambda p: (p["university"].lower(), p["title"].lower()))

PROGRAM_CATEGORIES = {
    "Engineering": ["engineering", "mechanical", "electrical", "civil"],
    "Computer Science": ["computer", "informatics", "software", "AI", "machine learning"],
    "Natural Sciences": ["biology", "chemistry", "physics", "earth science"],
}

def classify_program(prog):
    title_lower = prog["title"].lower()
    for category, keywords in PROGRAM_CATEGORIES.items():
        if any(kw.lower() in title_lower for kw in keywords):
            return category
    return "Other"
 
def mark_stale_programs(programs, months_threshold=12):
    now = datetime.now()
    for prog in programs:
        if "date_added" in prog:
            age_in_months = (now - datetime.fromisoformat(prog["date_added"])).days / 30
            prog["active"] = age_in_months < months_threshold
        else:
            prog["active"] = True
    return programs

def display_programs(programs):
    table = Table(title="DAAD Programs")

    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("Location", style="magenta")
    table.add_column("Degree")
    table.add_column("Link", style="green")

    for p in programs:
        table.add_row(p["title"], p["location"], p["degree"], p["url"])

    print(table)

# format Readme files
from collections import defaultdict

def create_programs_md(programs: list):
    sections = defaultdict(list)

    # Group by degree
    for prog in programs:
        sections[prog["degree"]].append(prog)

    md = "# DAAD Programs\n\n"
    md += "## Filter by Degree\n"
    for degree in sections:
        anchor = degree.lower().replace(" ", "-")
        md += f"- [{degree}](#{anchor})\n"

    md += "\n---\n"

    # Create section per degree
    for degree, progs in sections.items():
        md += f"\n## {degree}\n\n"
        md += "| University | Program | Location | Apply |\n"
        md += "|------------|---------|----------|-------|\n"

        for prog in progs:
            button = f'<a href="{prog["url"]}" target="_blank">Apply</a>'
            md += f"| {prog['university']} | {prog['title']} | {prog['location']} | {button} |\n"

    return md

def create_scholarships_md(scholarships: list):
    from datetime import datetime

    md = "# 💰 DAAD Scholarships\n\n"
    md += f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    md += f"Total Scholarships: {len(scholarships)}\n\n"
    md += "---\n\n"

    if not scholarships:
        md += "No scholarships found.\n"
        return md

    md += "| Title | DAAD Funded | Subjects | Apply |\n"
    md += "|-------|-------------|----------|-------|\n"

    for s in scholarships:
        title = s.get("title", "N/A").replace("|", "-")

        is_daad = "✅" if s.get("is_daAD") else "❌"

        subjects = ", ".join(s.get("subject_groups", []))
        subjects = subjects if subjects else "-"

        url = s.get("url", "#")
        button = f'<a href="{url}" target="_blank">View</a>'

        md += f"| {title} | {is_daad} | {subjects} | {button} |\n"

    return md

def update_readme(program_count, scholarship_count):
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"""# 🎓 DAAD Scraper
                 
                    ## 📊 Available Data

                    - [🎓 Study Programs](PROGRAMS.md)
                    - [💰 Scholarships](SCHOLARSHIPS.md)

                    ---

                    Last Updated: {datetime.utcnow().strftime('%Y-%m-%d')}  
                    Total Programs: {program_count}  
                    Total Scholarships: {scholarship_count}
                    """)