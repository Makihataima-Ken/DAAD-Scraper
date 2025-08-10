
import requests
from bs4 import BeautifulSoup
import time
import json
from utils import delay_random

BASE_URL = "https://www.daad.de/en/studying-in-germany/universities/all-degree-programmes/"

def scrape_programs(pages=3):
    all_programs = []

    counter = 0
    
    for page in range(1, pages + 1):
        
        url = f"{BASE_URL}?hec-p={page}"
        
        # Debuging 
        print(f"Scraping page {page}...")
        
        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            res.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.select("article.result")

        for card in cards:
            
            uni = card.select_one("h4 span:nth-of-type(1)").text.strip() if card.select_one("h4 span:nth-of-type(1)") else "Location not found"
            title = card.select_one("h4 span:nth-of-type(2)").text.strip() if card.select_one("h4 span:nth-of-type(2)") else "Title not found"
            degree = "Not found"
            location = "Not found"
            
            grid_items = card.select(".items-grid__item")
            for item in grid_items:
                # <dt> is the label, <dd> is the value
                label = item.select_one("dt")
                value = item.select_one("dd")
                if label and "Location" in label.text and value:
                    location = value.text.strip()
                if label and "Degree" in label.text and value:
                    degree = value.text.strip()
                    
            
            all_programs.append({
                "id":counter,
                "university": uni,
                "title": title,
                # "url": f"https://www2.daad.de{link}",
                "degree": degree,
                "location": location,
            })
            
            counter = counter + 1

        delay_random(2, 4)

    with open("data/programs.json", "w", encoding="utf-8") as f:
        json.dump(all_programs, f, indent=2, ensure_ascii=False)
    
    return all_programs
