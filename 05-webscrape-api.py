"""
Simple: pull quotes from the site's JSON (no HTML parsing) and save to CSV.
Site: https://quotes.toscrape.com/api/quotes?page=1
"""

import time
import requests
import pandas as pd

BASE_URL = "https://quotes.toscrape.com/api/quotes"
HEADERS = {"User-Agent": "DataEngineeringWorkshop/1.0 (+https://example.org/training)"}

def get_page(page):
    """Return JSON for a single page number (1, 2, 3, ...)."""
    r = requests.get(BASE_URL, params={"page": page}, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()

# -------- run ----------
rows = []
page = 1

while True:
    data = get_page(page)
    for q in data["quotes"]:  # each q has: text, author {name}, tags
        rows.append({
            "text": q["text"].strip(),
            "author": q["author"]["name"].strip(),
            "tags": ",".join(q.get("tags", [])),
            "page": page,
        })

    if not data["has_next"]:
        break

    page += 1
    time.sleep(0.4)  # be polite

# Save to CSV
df = pd.DataFrame(rows)
df.to_csv("output/quotes_hidden_api.csv", index=False, encoding="utf-8")
print(f"✅ Scraped {len(df)} quotes across {page} pages.")
print("💾 Saved to: quotes_hidden_api.csv")
