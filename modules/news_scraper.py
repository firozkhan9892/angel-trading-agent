"""
News Scraper Module
Fetches real company news, orders, and announcements from Finnhub
"""

import requests
from logzero import logger
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class NewsScraperFinnhub:
    """Fetch real news from Finnhub API."""

    API_KEY = os.getenv("FINNHUB_API_KEY", "")
    BASE_URL = "https://finnhub.io/api/v1/company-news"

    @staticmethod
    def get_company_news(symbol: str, limit: int = 5) -> list:
        """
        Fetch real news using Finnhub API.

        Args:
            symbol: Stock symbol (e.g., 'RELIANCE', 'INFY')
            limit: Number of news items

        Returns:
            List of news with title, date, link, source
        """
        try:
            if not NewsScraperFinnhub.API_KEY:
                logger.warning("Finnhub API key not set")
                return []

            params = {
                "symbol": symbol.upper(),
                "token": NewsScraperFinnhub.API_KEY,
                "limit": limit,
            }

            response = requests.get(NewsScraperFinnhub.BASE_URL, params=params, timeout=10)

            if response.status_code != 200:
                logger.warning(f"Finnhub fetch failed: {response.status_code}")
                return []

            data = response.json()
            news_list = []

            if isinstance(data, list):
                for article in data[:limit]:
                    # Filter for order/contract news
                    title = article.get('headline', '')
                    keywords = ['order', 'contract', 'wins', 'bags', 'secures', 'awarded']

                    if any(kw.lower() in title.lower() for kw in keywords):
                        news_list.append({
                            "title": title,
                            "link": article.get('url', ''),
                            "date": datetime.fromtimestamp(article.get('datetime', 0)).strftime("%Y-%m-%d"),
                            "source": article.get('source', 'Finnhub'),
                            "description": article.get('summary', '')
                        })

            logger.info(f"Fetched {len(news_list)} real news from Finnhub for {symbol}")
            return news_list

        except Exception as e:
            logger.error(f"Finnhub error: {e}")
            return []


class NewsAggregator:
    """Aggregate news from multiple sources."""

    @staticmethod
    def get_all_news(symbol: str, limit: int = 5) -> list:
        """
        Fetch real news from Finnhub.

        Args:
            symbol: Stock symbol
            limit: News items to fetch

        Returns:
            List of real news
        """
        all_news = []

        # Fetch from Finnhub
        finnhub_news = NewsScraperFinnhub.get_company_news(symbol, limit * 2)
        all_news.extend(finnhub_news)

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


