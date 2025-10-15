import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

# --- Step 1. Send request with a browser-like User-Agent ---
headers = {
    "User-Agent": ( # Identifyer of browser
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}
response = requests.get(url, headers=headers)
response.raise_for_status()

# --- Step 2. Parse the HTML ---
soup = BeautifulSoup(response.text, "html.parser")

# --- Step 3. Find the table ---
table = soup.find("table", {"class": "wikitable"})

# --- Step 4. Extract headers ---
headers = [th.get_text(strip=True) for th in table.find_all("th")]

# --- Step 5. Extract rows ---
rows = []
for tr in table.find_all("tr")[1:]:
    cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
    if cells:
        rows.append(cells)

# --- Step 6. Convert to DataFrame ---
df = pd.DataFrame(rows, columns=headers)

# --- Step 7. Save output safely ---
os.makedirs("output", exist_ok=True)
output_path = "output/wikipedia_gdp_nominal_bs4.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"✅ Scraped {len(df)} rows from Wikipedia.")
print(f"💾 Saved to: {output_path}")
