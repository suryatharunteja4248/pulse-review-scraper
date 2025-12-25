# Pulse Assignment – Product Review Scraper

This project is a Python-based review scraping script that extracts product reviews
for a given company and time period, and exports them into a structured JSON file.

The script supports:
- Input parameters through CLI
- Date-range filtering
- Pagination handling
- JSON output format
- Error handling & graceful failures

## Tech Stack
Python, Requests, BeautifulSoup, Dateutil

## Review Source

Due to 403 blocking restrictions on Capterra / GetApp in my region, the solution
uses **Trustpilot** as a SaaS review source while preserving the same assignment logic:

- Reviews are extracted for a product
- Data is parsed and structured
- Date-range filtering is applied
- Output is saved as JSON

This fulfills the requirement of scraping reviews for a SaaS product from an online
review platform.

## How to Run

Install dependencies:

pip install requests beautifulsoup4 python-dateutil

yaml
Copy code

Run the script:

python reviews_scraper.py --source capterra --url <trustpilot-review-url> --start YYYY-MM-DD --end YYYY-MM-DD

makefile
Copy code

Example:

python reviews_scraper.py --source capterra --url https://www.trustpilot.com/review/www.zoho.com --start 2020-01-01 --end 2025-12-31

perl
Copy code

## Output

The script generates `reviews.json` in the format:

[
{
"title": "Great product",
"review": "Zoho has improved our workflow...",
"date": "2024-08-17"
}
]

pgsql
Copy code

## Error Handling
- Invalid URLs handled gracefully
- Missing fields default to safe values
- Script stops safely when no more pages are available

## Assumptions / Notes
- Some SaaS review websites block automated access
- Trustpilot used as a working alternative data source
- G2 is included as a placeholder function

## Possible Extensions (Bonus Scope)
- Add G2 / GetApp fallback when not blocked
- Add CSV export
- Add proxy / session-based crawling