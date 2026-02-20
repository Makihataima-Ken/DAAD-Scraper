
import requests
from bs4 import BeautifulSoup
import time
import json
from utils import delay_random

BASE_URL = "https://www.daad.de/en/studying-in-germany/universities/all-degree-programmes/"

def scrape_programs():
    all_programs = []
    page = 1
    counter = 0

    while True:
        url = f"{BASE_URL}?hec-p={page}"
        print(f"Scraping page {page}...")

        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            res.raise_for_status()
        except requests.RequestException as e:
            print(f"Stopping. Request failed on page {page}: {e}")
            break

        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.select("article.result")

        # STOP CONDITION
        if not cards:
            print("No more results found. Stopping pagination.")
            break

        for card in cards:
            uni = card.select_one("h3 span:nth-of-type(1)")
            title = card.select_one("h3 span:nth-of-type(2)")
            link_tag = card.select_one("p a")

            uni = uni.text.strip() if uni else "Unknown"
            title = title.text.strip() if title else "Unknown"
            link = f"https://www.daad.de{link_tag['href']}" if link_tag else "Not found"

            degree = "Not found"
            location = "Not found"

            grid_items = card.select(".items-grid__item")
            for item in grid_items:
                label = item.select_one("dt")
                value = item.select_one("dd")

                if label and value:
                    if "Location" in label.text:
                        location = value.text.strip()
                    if "Degree" in label.text:
                        degree = value.text.strip()

            if degree == "Master":
                all_programs.append({
                    "id": counter,
                    "university": uni,
                    "title": title,
                    "url": link,
                    "degree": degree,
                    "location": location,
                })

            counter += 1

        page += 1
        # delay_random(2, 4)

    with open("data/programs.json", "w", encoding="utf-8") as f:
        json.dump(all_programs, f, indent=2, ensure_ascii=False)

    return all_programs
