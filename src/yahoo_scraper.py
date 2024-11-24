import json
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


class YahooNewsScraper:
    
    def __init__(self, ticker: str, logger: logging.Logger = logging.getLogger(__name__)):
        self.ticker = ticker
        self.save_file = f'data/{ticker}_articles.json'
        self.url = f'https://uk.finance.yahoo.com/quote/{ticker}/latest-news/'
        self.driver = None
        self.logger = logger
    
    def setup_driver(self):
        options = Options()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    def quit_driver(self):
        self.logger.info('Quitting WebDriver')
        self.driver.quit()
    
    def navigate_to_url(self):
        self.logger.info(f'Navigating to URL: {self.url}')
        self.driver.get(self.url)
    
    def handle_cookie_consent(self):
        if self.driver.title == 'Yahoo is part of the Yahoo family of brands':
            self.logger.info('Handling cookie consent page')
            self.driver.find_element(By.CLASS_NAME, 'reject-all').click()
    
    def find_news_stream(self):
        self.logger.info('Locating news stream element')
        return self.driver.find_element(By.CLASS_NAME, 'stream-items')
    
    def find_article_links(self, news_stream):
        self.logger.info('Finding article links')
        articles = news_stream.find_elements(By.CLASS_NAME, 'story-item')
        return [article.find_element(By.TAG_NAME, 'a').get_attribute('href') for article in articles]
    
    def load_existing_data(self):
        try:
            with open(self.save_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def process_article(self, link):
        self.logger.info(f'Processing article: {link}')
        self.driver.get(link)
        title = self.driver.title
        
        try:
            paragraphs = self.driver.find_elements(By.TAG_NAME, "p")
            text_content = '\n'.join([p.text for p in paragraphs if p.text.strip()])
        except StaleElementReferenceException:
            self.logger.warning('StaleElementReferenceException encountered, retrying')
            paragraphs = self.driver.find_elements(By.TAG_NAME, "p")
            text_content = '\n'.join([p.text for p in paragraphs if p.text.strip()])
        
        return {'title': title, 'link': link, 'content': text_content}
    
    def scrape(self):
        self.setup_driver()
        self.navigate_to_url()
        self.handle_cookie_consent()
        
        news_stream = self.find_news_stream()
        article_links = self.find_article_links(news_stream)
        
        article_data = self.load_existing_data()
        existing_articles = [article['link'] for article in article_data]
        for link in article_links:
            if link not in existing_articles:
                article_data.append(self.process_article(link))
            else:
                self.logger.info(f'Already processed article: {link}')
        
        self.quit_driver()
        
        with open(self.save_file, 'w') as f:
            json.dump(article_data, f, indent=4)
        
        return article_data


# Run the scraper on the AMZN ticker
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('./logs/yahoo_scraper_test.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    ticker = 'AMZN'
    scraper = YahooNewsScraper(ticker, logger)
    data = scraper.scrape()