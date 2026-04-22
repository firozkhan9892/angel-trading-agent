"""
Telegram Notification Module
Sends trading signals to Telegram in real-time
"""

import requests
from logzero import logger
import os
from dotenv import load_dotenv

load_dotenv()


class TelegramNotifier:
    """Send signals to Telegram chat."""

    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.enabled = os.getenv("TELEGRAM_ENABLED", "true").lower() == "true"
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_signal(self, signal) -> bool:
        """Send BUY/SELL alert to Telegram."""
        if not self.enabled or not self.bot_token or not self.chat_id:
            return False

        try:
            if signal.action == "HOLD":
                return True  # Don't send HOLD signals

            message = f"""{signal.action} SIGNAL

LTP: Rs {signal.ltp}
Score: {signal.score:+d}
Confidence: {signal.confidence}

Target: Rs {signal.target}
Stop Loss: Rs {signal.sl}

Time: {self._get_timestamp()}
"""

            payload = {
                "chat_id": self.chat_id,
                "text": message,
            }

            response = requests.post(self.api_url, json=payload, timeout=5)

            if response.status_code == 200:
                logger.info(f"Telegram alert sent: {signal.action}")
                return True
            else:
                logger.error(f"Telegram error: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Telegram exception: {e}")
            return False

    def send_error(self, error_msg: str) -> bool:
        """Send error notification."""
        if not self.enabled or not self.bot_token or not self.chat_id:
            return False

        try:
            message = f"⚠️ *Agent Error*\n\n{error_msg}\n\n⏰ {self._get_timestamp()}"

            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }

            response = requests.post(self.api_url, json=payload, timeout=5)
            return response.status_code == 200

        except Exception as e:
            logger.error(f"Error notification failed: {e}")
            return False

    def send_startup(self, symbol: str, interval: str) -> bool:
        """Send startup notification."""
        if not self.enabled or not self.bot_token or not self.chat_id:
            logger.warning(f"Telegram disabled or missing credentials: enabled={self.enabled}, token={bool(self.bot_token)}, chat_id={bool(self.chat_id)}")
            return False

        try:
            message = f"Agent Started\n\nSymbol: {symbol}\nInterval: {interval}\nTime: {self._get_timestamp()}\n\nWatching for signals..."

            payload = {
                "chat_id": self.chat_id,
                "text": message,
            }

            response = requests.post(self.api_url, json=payload, timeout=5)
            if response.status_code == 200:
                logger.info("Startup message sent successfully")
                return True
            else:
                logger.error(f"Startup failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Startup notification exception: {e}")
            return False

    @staticmethod
    def _get_timestamp() -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
