"""
Telegram Commands Handler
Responds to user commands on Telegram
"""

from datetime import datetime, time
from logzero import logger
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class TelegramCommandHandler:
    """Handle Telegram bot commands."""

    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    @staticmethod
    def get_market_status() -> dict:
        """Get current market status."""
        now = datetime.now()
        current_time = now.time()

        market_open = time(9, 15)
        market_close = time(15, 30)

        is_weekday = now.weekday() < 5  # Mon-Fri
        is_open = is_weekday and market_open <= current_time <= market_close

        if is_open:
            status = "OPEN"
            time_remaining = datetime.combine(now.date(), market_close) - now
            message = f"Market is OPEN\n\nClosing in: {time_remaining.seconds // 3600}h {(time_remaining.seconds % 3600) // 60}m"
        else:
            status = "CLOSED"
            if now.weekday() >= 5:
                message = "Market is CLOSED (Weekend)"
            else:
                next_open = datetime.combine(now.date(), market_open)
                if current_time > market_close:
                    next_open = datetime.combine(now.date() + __import__('datetime').timedelta(days=1), market_open)

                time_until = next_open - now
                hours = time_until.seconds // 3600
                minutes = (time_until.seconds % 3600) // 60
                message = f"Market is CLOSED\n\nOpens in: {hours}h {minutes}m"

        return {
            "status": status,
            "message": message,
            "is_open": is_open,
            "time": now.strftime("%Y-%m-%d %H:%M:%S IST")
        }

    def send_status(self) -> bool:
        """Send market status to Telegram."""
        try:
            market_info = self.get_market_status()

            message = f"""Market Status

Status: {market_info['status']}

{market_info['message']}

Time: {market_info['time']}

Use /help for more commands
"""

            payload = {
                "chat_id": self.chat_id,
                "text": message,
            }

            response = requests.post(self.api_url, json=payload, timeout=5)

            if response.status_code == 200:
                logger.info("Status message sent to Telegram")
                return True
            else:
                logger.error(f"Status send failed: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Status command error: {e}")
            return False

    def send_help(self) -> bool:
        """Send help message to Telegram."""
        try:
            message = """Angel One Trading Agent - Commands

/status - Get current market status
/help - Show this help message
/signals - Get today's signals count
/latest - Get latest signal

Agent Features:
- Real-time trading signals (RSI, MACD, EMA, VWAP, BB)
- Company order news from Finnhub
- Automatic alerts every 5 minutes

Market Hours: 9:15 AM - 3:30 PM IST (Mon-Fri)
"""

            payload = {
                "chat_id": self.chat_id,
                "text": message,
            }

            response = requests.post(self.api_url, json=payload, timeout=5)
            return response.status_code == 200

        except Exception as e:
            logger.error(f"Help command error: {e}")
            return False
