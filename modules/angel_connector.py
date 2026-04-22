"""
Angel One SmartAPI Connector Module
Handles authentication, session management, and data fetching
"""

import pyotp
import pandas as pd
from datetime import datetime, timedelta
from SmartApi import SmartConnect
from logzero import logger
import os
from dotenv import load_dotenv

load_dotenv()


class AngelConnector:
    """
    Angel One SmartAPI connection manager.
    Handles login, token refresh, and market data fetching.
    """

    def __init__(self):
        self.api_key     = os.getenv("API_KEY")
        self.client_id   = os.getenv("CLIENT_ID")
        self.password    = os.getenv("PASSWORD")
        self.totp_secret = os.getenv("TOTP_SECRET")
        self.smart_api   = None
        self.auth_token  = None
        self.feed_token  = None

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    def login(self) -> bool:
        """Login to Angel One SmartAPI and establish session."""
        try:
            totp = pyotp.TOTP(self.totp_secret).now()
            self.smart_api = SmartConnect(api_key=self.api_key)

            data = self.smart_api.generateSession(
                self.client_id,
                self.password,
                totp
            )

            if data["status"]:
                self.auth_token = data["data"]["jwtToken"]
                self.feed_token = self.smart_api.getfeedToken()
                logger.info(f"✅ Login successful — Client: {self.client_id}")
                return True
            else:
                logger.error(f"❌ Login failed: {data['message']}")
                return False

        except Exception as e:
            logger.error(f"❌ Login exception: {e}")
            return False

    def logout(self):
        """Terminate the SmartAPI session."""
        try:
            self.smart_api.terminateSession(self.client_id)
            logger.info("🔒 Session terminated.")
        except Exception as e:
            logger.warning(f"Logout warning: {e}")

    # ------------------------------------------------------------------
    # Market Data
    # ------------------------------------------------------------------
    def get_historical_data(
        self,
        symbol_token: str,
        exchange: str = "NSE",
        interval: str = "FIVE_MINUTE",
        days: int = 5
    ) -> list:
        """
        Fetch OHLCV historical candle data.

        Args:
            symbol_token : Angel One instrument token (e.g. '3045' for SBIN)
            exchange     : 'NSE' | 'BSE' | 'NFO'
            interval     : ONE_MINUTE | FIVE_MINUTE | FIFTEEN_MINUTE | ONE_HOUR | ONE_DAY
            days         : How many past days of data to fetch

        Returns:
            List of dicts with [timestamp, open, high, low, close, volume]
        """
        try:
            from datetime import datetime, timedelta

            to_date   = datetime.now()
            from_date = to_date - timedelta(days=days)

            params = {
                "exchange":    exchange,
                "symboltoken": symbol_token,
                "interval":    interval,
                "fromdate":    from_date.strftime("%Y-%m-%d %H:%M"),
                "todate":      to_date.strftime("%Y-%m-%d %H:%M"),
            }

            response = self.smart_api.getCandleData(params)

            if response["status"]:
                data = []
                for candle in response["data"]:
                    data.append({
                        "timestamp": candle[0],
                        "open": float(candle[1]),
                        "high": float(candle[2]),
                        "low": float(candle[3]),
                        "close": float(candle[4]),
                        "volume": int(candle[5])
                    })

                logger.info(f"Fetched {len(data)} candles for token {symbol_token}")
                return data
            else:
                logger.error(f"Data fetch failed: {response['message']}")
                return []

        except Exception as e:
            logger.error(f"Historical data exception: {e}")
            return []

    def get_ltp(self, exchange: str, symbol: str, symbol_token: str) -> float:
        """Get Last Traded Price (LTP) for a symbol."""
        try:
            data = self.smart_api.ltpData(exchange, symbol, symbol_token)
            if data["status"]:
                ltp = data["data"]["ltp"]
                logger.info(f"💰 LTP for {symbol}: ₹{ltp}")
                return ltp
            else:
                logger.error(f"LTP fetch failed: {data['message']}")
                return 0.0
        except Exception as e:
            logger.error(f"LTP exception: {e}")
            return 0.0

    def search_symbol_token(self, symbol: str, exchange: str = "NSE") -> str:
        """
        Search instrument token for a given symbol name.
        Returns token string or empty string on failure.
        """
        try:
            data = self.smart_api.searchScrip(exchange, symbol)
            if data["status"] and data["data"]:
                token = data["data"][0]["symboltoken"]
                logger.info(f"🔍 Token for {symbol}: {token}")
                return token
            return ""
        except Exception as e:
            logger.error(f"Symbol search exception: {e}")
            return ""
