# 📰 News Integration Guide

## Features

Your agent now fetches **company news and order announcements** automatically!

### What It Does:
- Fetches latest news every 30 minutes
- Searches for order/contract announcements
- Sends news alerts to Telegram
- Aggregates from multiple sources (MoneyControl, Economic Times, BSE)

---

## News Sources

| Source | Type | Updates |
|--------|------|---------|
| **MoneyControl** | General news | Real-time |
| **Economic Times** | Financial news | Real-time |
| **BSE** | Official announcements | Daily |

---

## Keywords Tracked

The agent filters news for these keywords:
- `order` - New orders received
- `contract` - Contract wins
- `wins` - Project wins
- `bags` - Bags new order
- `secures` - Secures contract
- `awarded` - Gets awarded
- `gets` - Gets new deal

---

## Example News Alert on Telegram

```
NEWS: Reliance wins Rs 5000 crore order from NTPC

Source: MoneyControl
Date: 2026-04-22
```

---

## How It Works

1. **Every 30 minutes** (during market hours):
   - Agent fetches latest news for your symbol
   - Filters for order/contract keywords
   - Sends top 3 news items to Telegram

2. **Automatic Updates**:
   - No manual intervention needed
   - Runs alongside trading signals
   - Separate from signal alerts

3. **Multiple Sources**:
   - Aggregates from 3+ sources
   - Removes duplicates
   - Prioritizes recent news

---

## Configuration

News fetching is **automatic** - no setup needed!

To disable news (optional):
```python
# In agent.py, comment out the news section:
# if scan_count % 6 == 0:
#     news_list = news_agg.get_all_news(symbol, limit=3)
```

---

## Troubleshooting

### Not receiving news?
- Check internet connection
- Verify symbol is in supported list
- Check Telegram is enabled

### Slow news fetching?
- Web scraping can be slow (5-10 sec)
- Runs every 30 min to avoid delays
- Doesn't affect trading signals

### Add more sources?
Edit `modules/news_scraper.py` and add new scraper classes:
```python
class NewsScraperYourSource:
    @staticmethod
    def get_company_news(symbol, limit=5):
        # Your scraping logic
        pass
```

---

## Supported Symbols

```
RELIANCE, INFY, TCS, SBIN, HDFCBANK, WIPRO, MARUTI, BAJAJFINSV
```

Add more in `symbol_map` in `news_scraper.py`

---

**Your agent now tracks both trading signals AND company news!** 📈📰
