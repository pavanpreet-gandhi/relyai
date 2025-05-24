from yahoo_scraper import YahooNewsScraper
from ai_summarizer import AISummarizer
import logging
import os

TICKER = 'AAPL'

# Create logs directory if it doesn't exist
logs_dir = './logs'
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
    print(f"Created logs directory at {os.path.abspath(logs_dir)}")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'./logs/{TICKER}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
scraper = YahooNewsScraper(TICKER, logger)
scraper.scrape()

summarizer = AISummarizer(TICKER, logger)
summarizer.summarize_articles()