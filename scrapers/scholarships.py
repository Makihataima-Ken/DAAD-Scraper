import requests
from bs4 import BeautifulSoup
import json
from utils import delay_random

BASE_URL = "https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_scholarships():
    all_scholarships = []
    page = 1
    counter = 0

    while True:
        url = f"{BASE_URL}?status=&origin=&subjectGrps=&daad=&intention=&q=&page={page}&back=1"
        print(f"Scraping scholarship page {page}...")

        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            res.raise_for_status()
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(res.text)
        except requests.RequestException as e:
            print(f"Stopping on page {page}: {e}")
            break

        soup = BeautifulSoup(res.text, "html.parser")

        # THIS IS THE IMPORTANT PART
        result_list = soup.select_one("ul.resultlist")
        
        # cards = result_list.select("li.entry.clearfix")
        cards = soup.select("li.entry")
        
        print(f"Found {len(cards)} scholarship entries on page {page}.")

        if not cards:
            print("No more scholarship entries found. Stopping pagination.")
            break

        for card in cards:
            # Title + link usually inside <a>
            link_tag = card.select_one("a")
            title = link_tag.get_text(strip=True) if link_tag else "No title"

            link = ""
            if link_tag and link_tag.has_attr("href"):
                link = link_tag["href"]
                if not link.startswith("http"):
                    link = f"https://www2.daad.de{link}"

            # Optional: extract short description if available
            description_tag = card.select_one("p")
            summary = description_tag.get_text(strip=True) if description_tag else ""

            scholarship = {
                "id": counter,
                "title": title,
                "summary": summary,
                "url": link
            }

            all_scholarships.append(scholarship)
            counter += 1

        page += 1
        # delay_random(1, 3)

    # Save JSON
    # with open("data/scholarships.json", "w", encoding="utf-8") as f:
    #     json.dump(all_scholarships, f, indent=2, ensure_ascii=False)

    return all_scholarships