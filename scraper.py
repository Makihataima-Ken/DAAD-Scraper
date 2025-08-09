
import requests
from bs4 import BeautifulSoup
import time
import json
from utils import delay_random

BASE_URL = "https://www2.daad.de/deutschland/studienangebote/"

def scrape_programs(pages=3,field ="international-programs/en/"):
    all_programs = []

    for page in range(1, pages + 1):
        
        url = f"{BASE_URL + field}?page={page}"
        
        # Debuging 
        print(f"Scraping page {page}...")
        
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.select(".result-list__body > article")

        for card in cards:
            title = card.select_one("h2").text.strip()
            link = card.select_one("a")["href"]
            location = card.select_one(".result-list__university").text.strip()
            degree = card.select_one(".result-list__degree").text.strip() if card.select_one(".result-list__degree") else ""
            
            all_programs.append({
                "title": title,
                "url": f"https://www2.daad.de{link}",
                "location": location,
                "degree": degree,
            })

        delay_random(2, 4)

    with open("data/programs.json", "w", encoding="utf-8") as f:
        json.dump(all_programs, f, indent=2, ensure_ascii=False)
    
    return all_programs
