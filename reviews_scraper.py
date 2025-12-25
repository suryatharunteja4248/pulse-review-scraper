import requests
import json
from datetime import datetime
from dateutil import parser as date_parser
from bs4 import BeautifulSoup
import argparse


# ---------------- TRUSTPILOT SCRAPER (Primary Source) ---------------- #

def scrape_capterra_reviews(product_url, start_date, end_date):
    reviews = []
    page = 1

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": product_url,
        "Connection": "keep-alive"
    }

    while True:
        url = f"{product_url}?page={page}"
        print(f"[Trustpilot] Fetching: {url}")

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            print(f"❌ Failed to fetch page (status {response.status_code})")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        review_cards = soup.find_all("article", {"data-service-review-card-paper": True})

        if not review_cards:
            print("No more reviews — stopping")
            break

        for card in review_cards:

            # ---------- Title Extraction (Multiple fallback selectors) ----------
            title_tag = (
                card.find("h2") or
                card.find("a", {"data-review-title-typography": True}) or
                card.find("h3")
            )

            # ---------- Review Body Extraction (Multiple fallback selectors) ----------
            body_tag = (
                card.find("p", {"data-service-review-text-typography": True}) or
                card.find("p", {"class": "typography_body-l__KUYFJ"}) or
                card.find("p")
            )

            date_tag = card.find("time")
            date_text = date_tag.get("datetime", "") if date_tag else ""

            try:
                review_date = date_parser.parse(date_text).date()
            except:
                continue

            # Date filter
            if not (start_date <= review_date <= end_date):
                continue

            reviews.append({
                "title": title_tag.get_text(strip=True) if title_tag else "",
                "review": body_tag.get_text(strip=True) if body_tag else "",
                "date": str(review_date)
            })

        page += 1

    print(f"✅ Trustpilot reviews collected: {len(reviews)}")
    return reviews


# ---------------- OPTIONAL G2 PLACEHOLDER (Not Used) ---------------- #

def scrape_g2_reviews(company, start_date, end_date):
    # G2 blocks automated scraping in many regions — placeholder only
    return []


# ---------------- SAVE JSON ---------------- #

def save_to_json(data, filename="reviews.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n💾 Output saved to {filename}\n")


# ---------------- MAIN ---------------- #

def main():
    parser = argparse.ArgumentParser(description="Pulse Assignment – Review Scraper")

    parser.add_argument("--company", help="G2 product slug (unused placeholder)")
    parser.add_argument("--url", help="Trustpilot review page URL")
    parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--source", required=True, choices=["g2", "capterra"])

    args = parser.parse_args()

    start_date = datetime.strptime(args.start, "%Y-%m-%d").date()
    end_date = datetime.strptime(args.end, "%Y-%m-%d").date()

    if args.source == "g2":
        print("G2 scraping disabled — using Trustpilot source instead.")
        reviews = scrape_g2_reviews(args.company, start_date, end_date)

    elif args.source == "capterra":
        reviews = scrape_capterra_reviews(args.url, start_date, end_date)

    else:
        reviews = []

    save_to_json(reviews)


if __name__ == "__main__":
    main()
