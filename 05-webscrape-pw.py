"""
Lazada 'Just For You' minimal scraper (Playwright only, no args needed).

BEGINNER NOTES:
- This script opens Lazada, waits for product cards, scrolls, collects data,
  and saves it to output/lazada_jfy.csv.
- You do NOT need to pass a URL. It uses the Lazada homepage by default.
- Keep it headless=True for speed. If you want to watch the browser, set it to False.

Run:
  python lazada_jfy_min.py
"""

import re
import time
import random
from pathlib import Path

import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError

# 1) You can change this to any Lazada listing page later if you want.
START_URL = "https://www.lazada.com.ph/"
OUT_CSV = "output/lazada_jfy.csv"
HEADLESS = True                 # Set to False to see the browser
NAV_TIMEOUT_MS = 30_000         # How long to wait for the page to load
SELECTOR_TIMEOUT_MS = 15_000    # How long to wait for product cards to appear


def pct_to_star_score(style_value: str | None) -> float | None:
    """
    Convert CSS style like 'width: 96%;' into star rating out of 5.
    Lazada uses a filled-stars layer width (0%..100%). 100% = 5 stars.
    So stars = (percent / 100) * 5 = percent / 20
    """
    if not style_value:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", style_value)
    if not m:
        return None
    percent = float(m.group(1))
    return round(percent / 20.0, 2)  # e.g., 96% → 4.8


def clean(text: str | None) -> str | None:
    """Trim whitespace; return None if empty."""
    if not text:
        return None
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned or None


def scrape_visible_cards(page) -> list[dict]:
    """
    Grab data from each '.card-jfy-item-desc' tile currently in the DOM.
    We extract: title, currency, price, discount, rating, reviews.
    """
    rows = []

    # Find all the product tiles
    cards = page.query_selector_all(".card-jfy-item-desc")

    for card in cards:
        title_el = card.query_selector(".card-jfy-title")
        currency_el = card.query_selector(".hp-mod-price-first-line .currency")
        price_el = card.query_selector(".hp-mod-price-first-line .price")
        discount_el = card.query_selector(".hp-mod-price-first-line .hp-mod-discount")
        rating_layer = card.query_selector(".card-jfy-rating-layer.top-layer.checked")
        reviews_el = card.query_selector(".card-jfy-ratings-comment")

        # Read text safely (elements may not exist on every tile)
        title = clean(title_el.inner_text()) if title_el else None
        currency = clean(currency_el.inner_text()) if currency_el else None
        price = clean(price_el.inner_text()) if price_el else None
        discount = clean(discount_el.inner_text()) if discount_el else None

        # Rating is derived from a CSS width percentage on the "checked" layer
        rating_style = rating_layer.get_attribute("style") if rating_layer else None
        rating = pct_to_star_score(rating_style)

        # Reviews look like "(1234)"; turn into an integer 1234
        reviews = None
        if reviews_el:
            m = re.search(r"\(([\d,]+)\)", reviews_el.inner_text())
            if m:
                reviews = int(m.group(1).replace(",", ""))

        # Only add rows that have at least a title or a price
        if title or price:
            rows.append(
                {
                    "title": title,
                    "currency": currency,
                    "price": price,
                    "discount": discount,
                    "rating": rating,
                    "reviews": reviews,
                }
            )

    return rows


def run_scrape() -> list[dict]:
    """
    Open a browser, go to Lazada, wait for cards, scroll a bit to load more,
    scrape them, then close the browser. Returns a list of dicts.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900}
        )
        page = context.new_page()

        # 1) Go to Lazada homepage
        page.goto(START_URL, timeout=NAV_TIMEOUT_MS, wait_until="domcontentloaded")

        # 2) Wait for at least one card to appear (site is dynamic)
        try:
            page.wait_for_selector(".card-jfy-item-desc", timeout=SELECTOR_TIMEOUT_MS)
        except TimeoutError:
            print("No 'Just For You' cards were found. Try HEADLESS=False or wait longer.")
            context.close()
            browser.close()
            return []

        # 3) Gentle scrolling: helps load more rows below the fold
        for _ in range(4):
            page.mouse.wheel(0, 2500)                 # scroll down a bit
            time.sleep(0.8 + random.random() * 0.5)   # short pause so content can load

        # 4) Collect the data from visible cards
        data = scrape_visible_cards(page)

        # 5) Close everything
        context.close()
        browser.close()

        return data


def save_to_csv(rows: list[dict], path: str) -> None:
    """Save the rows to a CSV file (creates the output folder if needed)."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows, columns=["title", "currency", "price", "discount", "rating", "reviews"])
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


def main():
    """Entry point: run the scrape and save to CSV."""
    rows = run_scrape()
    if not rows:
        print("Nothing scraped. You can try again, or set HEADLESS=False to observe the page.")
        return
    save_to_csv(rows, OUT_CSV)


if __name__ == "__main__":
    main()
