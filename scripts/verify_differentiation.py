
import pandas as pd
from src.services.scraper import TrustpilotScraper
from src.services.preprocessor import SpanishTextPreprocessor
from src.services.analyzer import SentimentAnalyzerES

def run_test(domain):
    print(f"\n--- Testing Domain: {domain} ---")
    scraper = TrustpilotScraper(domain)
    preprocessor = SpanishTextPreprocessor()
    analyzer = SentimentAnalyzerES()
    
    df_raw = scraper.scrape_reviews(max_reviews=20)
    if df_raw.empty:
        print(f"No data for {domain}")
        return
        
    processed = [preprocessor.process_pipeline(t) for t in df_raw['text']]
    df_proc = pd.DataFrame(processed)
    df_merged = pd.concat([df_raw, df_proc.drop(columns=['original'])], axis=1)
    
    df_final = analyzer.analyze_batch(df_merged)
    
    avg_rating = df_final['rating'].mean()
    avg_sentiment = df_final['sentimiento_score'].mean()
    dist = df_final['sentimiento'].value_counts().to_dict()
    
    print(f"Average Rating (Trustpilot): {avg_rating:.2f}")
    print(f"Average Hybrid Sentiment: {avg_sentiment:.2f}")
    print(f"Distribution: {dist}")

if __name__ == "__main__":
    domains = ['amazon.es', 'pccomponentes.com']
    for d in domains:
        run_test(d)
