
from src.services.scraper import TrustpilotScraper
import pandas as pd

def test_domains(domains):
    for domain in domains:
        print(f"\n--- Scraping {domain} ---")
        scraper = TrustpilotScraper(domain)
        df = scraper.scrape_reviews(max_reviews=5)
        if not df.empty:
            print(f"Total reviews: {len(df)}")
            print(df[['domain', 'user', 'rating', 'text']].head(5))
        else:
            print("No reviews found.")

if __name__ == "__main__":
    test_domains(['amazon.es', 'pccomponentes.com'])
