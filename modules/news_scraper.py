"""
News Scraper Module
Fetches company news, orders, and announcements
"""

import requests
from bs4 import BeautifulSoup
from logzero import logger
from datetime import datetime
import re


class NewsScraperMock:
    """Mock news source for testing (replace with real API)."""

    MOCK_NEWS = {
        "RELIANCE": [
            {"title": "Reliance wins Rs 5000 crore order from NTPC", "source": "Economic Times"},
            {"title": "Reliance bags new contract for renewable energy", "source": "MoneyControl"},
            {"title": "Reliance secures major order from government", "source": "Business Today"},
        ],
        "INFY": [
            {"title": "Infosys wins $500M contract from Fortune 500 company", "source": "ET"},
            {"title": "Infosys bags new order in cloud services", "source": "MC"},
        ],
        "TCS": [
            {"title": "TCS wins major IT contract", "source": "ET"},
            {"title": "TCS secures digital transformation order", "source": "MC"},
        ],
    }

    @staticmethod
    def get_company_news(symbol: str, limit: int = 5) -> list:
        """Get mock news for testing."""
        symbol_upper = symbol.upper()
        mock_news = NewsScraperMock.MOCK_NEWS.get(symbol_upper, [])

        news_list = []
        for item in mock_news[:limit]:
            news_list.append({
                "title": item["title"],
                "link": "https://example.com",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "source": item["source"]
            })

        logger.info(f"Fetched {len(news_list)} mock news for {symbol}")
        return news_list


class NewsAggregator:
    """Aggregate news from multiple sources."""

    @staticmethod
    def get_all_news(symbol: str, limit: int = 5) -> list:
        """
        Fetch news from all sources and combine.

        Args:
            symbol: Stock symbol
            limit: News items per source

        Returns:
            Combined news list
        """
        all_news = []

        # Use mock news for now (replace with real API)
        mock_news = NewsScraperMock.get_company_news(symbol, limit)
        all_news.extend(mock_news)

        # Remove duplicates and sort by date
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
