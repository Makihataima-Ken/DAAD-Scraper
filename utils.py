from datetime import datetime, timedelta
import time
import random

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

# 
def mark_stale_programs(programs, months_threshold=12):
    now = datetime.now()
    for prog in programs:
        if "date_added" in prog:
            age_in_months = (now - datetime.fromisoformat(prog["date_added"])).days / 30
            prog["active"] = age_in_months < months_threshold
        else:
            prog["active"] = True
    return programs

# format Readme files
def create_md_table(programs):
    table = "| University | Program | Degree | Location | Link |\n"
    table += "|------------|---------|--------|----------|------|\n"
    for prog in programs:
        table += f"| {prog['university']} | {prog['title']} | {prog['degree']} | {prog['location']} | [Link]({prog['url']}) |\n"
    return table

