import os
import json
import logging
from dotenv import load_dotenv
from openai import OpenAI
from textwrap import dedent

class AISummarizer:
    
    
    def __init__(self, ticker: str, logger: logging.Logger = logging.getLogger(__name__)):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.ticker = ticker
        self.articles_file = f'data/{ticker}_articles.json'
        self.save_file = f'data/{ticker}_summaries.json'
        self.logger = logger
    
    
    def summarize_article(self, article: dict):
        model = 'gpt-4o'
        system_message = """
        You are a financial news summarizer.
        Your job is to summarise financial news articles in a few sentences and give actionable yet balanced insights.
        Output the summaries in a clear and concise manner.
        The summaries should almost sound like tweets to be engaging and informative.
        Each summary should be around 280 characters long.
        Add emojis but no hashtags.
        """
        user_message = f"""
        Summarize the following article:
        ```
        Title: {article['title']}
        Content: {article['content']}
        ```
        Note that the article may contain irrelevant information, only summarise the information related to '{self.ticker}'.
        """
        system_message = dedent(system_message).strip()
        user_message = dedent(user_message).strip()
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': user_message}
            ]
        )
        summary = completion.choices[0].message.content
        self.logger.info(f"Generated summary for article: {article['link']}")
        self.logger.info(f'Summary: {summary}')
        return summary
    
    
    def summarize_articles(self):
        try:
            with open(self.articles_file, 'r') as f:
                article_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError('No data found, please run the scraper first')
        
        try:
            with open(self.save_file, 'r') as f:
                summaries = json.load(f)
        except FileNotFoundError:
            summaries = []
        
        existing_summaries = [summary['link'] for summary in summaries]
        for article in article_data:
            if article['link'] not in existing_summaries:
                summary = self.summarize_article(article)
                summaries.append({'link': article['link'], 'summary': summary})
            else:
                self.logger.info(f"Already summarized article: {article['link']}")
        
        with open(self.save_file, 'w') as f:
            json.dump(summaries, f, indent=4)
        
        return summaries


# Run the summarizer on the AMZN ticker
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('./logs/ai_summarizer_test.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    ticker = 'AMZN'
    summarizer = AISummarizer(ticker, logger)
    summarizer.summarize_articles()