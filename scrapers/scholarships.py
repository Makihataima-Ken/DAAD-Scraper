import requests
import json
import re

SCHOLARSHIPS_JS_URL = (
    "https://www2.daad.de/bundles/"
    "daadstipendiendatenbanklsh/data/a/js/scholarships.js"
)

def scrape_scholarships():
    print("Downloading DAAD scholarships dataset...")

    response = requests.get(SCHOLARSHIPS_JS_URL)
    response.raise_for_status()

    js_text = response.text

    # Extract the JSON array inside TAFFY(...)
    match = re.search(r"TAFFY\(\s*(\[.*\])\s*\)", js_text, re.DOTALL)

    if not match:
        print("Could not extract scholarship array.")
        return []

    json_array_text = match.group(1)

    # Parse JSON safely
    scholarships_data = json.loads(json_array_text)

    results = []

    for item in scholarships_data:
        results.append({
            "id": item.get("id"),
            "title": item.get("nameEn") or item.get("programmnameEn"),
            "is_daAD": item.get("isDaad"),
            "subject_groups": item.get("subjectGrps"),
            "status": item.get("status"),
            "origin": item.get("origin"),
            "intentions": item.get("intentions"),
        })

    print(f"Loaded {len(results)} scholarships.")
    return results