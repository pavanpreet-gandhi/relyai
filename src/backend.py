from yahoo_scraper import YahooNewsScraper
from ai_summarizer import AISummarizer
import logging

TICKER = 'AAPL'

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