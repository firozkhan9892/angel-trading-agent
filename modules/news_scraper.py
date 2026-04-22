"""
News Scraper Module
Fetches real company news, orders, and announcements from NewsAPI
"""

import requests
from logzero import logger
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class NewsScraperNewsAPI:
    """Fetch real news from NewsAPI."""

    API_KEY = os.getenv("NEWS_API_KEY", "demo")
    BASE_URL = "https://newsapi.org/v2/everything"

    @staticmethod
    def get_company_news(symbol: str, limit: int = 5) -> list:
        """
        Fetch real news using NewsAPI.

        Args:
            symbol: Stock symbol (e.g., 'RELIANCE', 'INFY')
            limit: Number of news items

        Returns:
            List of news with title, date, link, source
        """
        try:
            # Search for company orders, contracts, wins
            query = f"{symbol} order OR contract OR wins OR bags OR secures"

            params = {
                "q": query,
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": limit,
                "apiKey": NewsScraperNewsAPI.API_KEY,
            }

            response = requests.get(NewsScraperNewsAPI.BASE_URL, params=params, timeout=10)

            if response.status_code != 200:
                logger.warning(f"NewsAPI fetch failed: {response.status_code}")
                return []

            data = response.json()
            news_list = []

            if data.get('articles'):
                for article in data['articles'][:limit]:
                    news_list.append({
                        "title": article.get('title', 'N/A'),
                        "link": article.get('url', ''),
                        "date": article.get('publishedAt', datetime.now().strftime("%Y-%m-%d")),
                        "source": article.get('source', {}).get('name', 'NewsAPI'),
                        "description": article.get('description', '')
                    })

            logger.info(f"Fetched {len(news_list)} real news from NewsAPI for {symbol}")
            return news_list

        except Exception as e:
            logger.error(f"NewsAPI error: {e}")
            return []


class NewsAggregator:
    """Aggregate news from multiple sources."""

    @staticmethod
    def get_all_news(symbol: str, limit: int = 5) -> list:
        """
        Fetch real news from NewsAPI.

        Args:
            symbol: Stock symbol
            limit: News items to fetch

        Returns:
            List of real news
        """
        all_news = []

        # Fetch from NewsAPI
        api_news = NewsScraperNewsAPI.get_company_news(symbol, limit)
        all_news.extend(api_news)

        # Remove duplicates
        unique_news = {news['title']: news for news in all_news}

        return list(unique_news.values())[:limit]

    @staticmethod
    def filter_order_news(news_list: list) -> list:
        """
        Filter news for order announcements.

        Keywords: 'order', 'contract', 'wins', 'bags', 'secures'
        """
        order_keywords = ['order', 'contract', 'wins', 'bags', 'secures', 'awarded', 'gets']

        filtered = []
        for news in news_list:
            title_lower = news['title'].lower()
            if any(keyword in title_lower for keyword in order_keywords):
                filtered.append(news)

        return filtered

