"""
Angel One Intraday Buy/Sell Signal Agent
========================================
Main runner — fetches live data, computes indicators,
generates signals, and logs them on a configurable interval.

Usage:
    python agent.py                    # uses .env defaults
    python agent.py --symbol INFY --interval FIVE_MINUTE
"""

import argparse
import time
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from logzero import logger, logfile

# ── Local modules ────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from modules.angel_connector  import AngelConnector
from modules.indicators        import IndicatorEngine
from modules.signal_generator  import SignalGenerator
from modules.telegram_notifier import TelegramNotifier
from modules.news_scraper      import NewsAggregator

load_dotenv()

# ── Logging setup ─────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logfile(
    f"logs/agent_{datetime.now().strftime('%Y%m%d')}.log",
    maxBytes=5_000_000,
    backupCount=3,
)

# ── Interval map (minutes between each scan) ──────────────────────────
INTERVAL_SLEEP = {
    "ONE_MINUTE":     60,
    "FIVE_MINUTE":   300,
    "FIFTEEN_MINUTE": 900,
}

# ── Market hours (IST) ────────────────────────────────────────────────
MARKET_OPEN  = (9, 15)   # 9:15 AM
MARKET_CLOSE = (15, 30)  # 3:30 PM


def is_market_open() -> bool:
    now = datetime.now()
    if now.weekday() >= 5:      # Saturday / Sunday
        return False
    t = (now.hour, now.minute)
    return MARKET_OPEN <= t <= MARKET_CLOSE


def print_banner():
    try:
        print("""
╔══════════════════════════════════════════════════════════╗
║       Angel One Intraday Signal Agent  v1.0             ║
║       Indicators : RSI · MACD · EMA · VWAP · BB         ║
║       Press  Ctrl+C  to stop                             ║
╚══════════════════════════════════════════════════════════╝
""")
    except:
        print("Angel One Intraday Signal Agent v1.0")


def print_signal_box(symbol: str, sig, interval: str):
    """Pretty-print the signal to console."""
    color = {"BUY": "\033[92m", "SELL": "\033[91m", "HOLD": "\033[93m"}.get(sig.action, "")
    reset = "\033[0m"

    print(f"\n{'━'*58}")
    print(f"  📅 {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}   |   {interval}")
    print(f"  📌 Symbol   : {symbol}")
    print(f"  💰 LTP      : ₹{sig.ltp}")
    print(f"  {color}🚦 Signal   : {sig.action}  (Score: {sig.score:+d} | {sig.confidence}){reset}")

    if sig.action != "HOLD":
        print(f"  🎯 Target   : ₹{sig.target}")
        print(f"  🛑 Stop Loss: ₹{sig.sl}")

    print(f"\n  📊 Reasons:")
    for r in sig.reasons:
        print(f"     {r}")
    print(f"{'━'*58}")


def run_agent(symbol: str, token: str, exchange: str, interval: str):
    """Core agent loop."""
    connector = AngelConnector()
    engine    = IndicatorEngine()
    generator = SignalGenerator()
    telegram  = TelegramNotifier()
    news_agg  = NewsAggregator()

    if not connector.login():
        logger.error("Cannot start agent — login failed.")
        telegram.send_error("❌ Angel One login failed. Check credentials.")
        return

    sleep_secs = INTERVAL_SLEEP.get(interval, 300)
    scan_count = 0
    idle_count = 0

    logger.info(f"🎯 Watching : {symbol} ({exchange}) | Interval: {interval}")
    logger.info(f"⏱️  Scanning every {sleep_secs // 60} minute(s)")
    logger.info("💡 Free Render plan: Keep-alive pings every 10 min to prevent spin-down")

    try:
        # Send startup notification (before market check)
        startup_sent = telegram.send_startup(symbol, interval)
        if startup_sent:
            logger.info("✅ Telegram startup message sent!")
        else:
            logger.warning("⚠️  Telegram startup message failed - check credentials")

        while True:
            if not is_market_open():
                idle_count += 1
                if idle_count % 2 == 0:  # Ping every 10 min during market closed
                    logger.info(f"🕐 Market closed. Keep-alive ping #{idle_count // 2}...")
                time.sleep(300)
                continue

            idle_count = 0

            scan_count += 1
            logger.info(f"\n{'='*50}\n🔍 Scan #{scan_count} | {datetime.now().strftime('%H:%M:%S')}")

            # 1. Fetch data
            df = connector.get_historical_data(
                symbol_token=token,
                exchange=exchange,
                interval=interval,
                days=5,
            )

            if df.empty:
                logger.warning("⚠️  Empty data received — skipping this scan.")
                time.sleep(60)
                continue

            # 2. Compute indicators
            df = IndicatorEngine.compute_all(df)

            # 3. Generate signal
            signal = generator.generate(df)

            # 4. Display
            print_signal_box(symbol, signal, interval)

            # 5. Send Telegram alert
            telegram.send_signal(signal)

            # 6. Fetch and send news (every 30 minutes)
            if scan_count % 6 == 0:  # Every 6 scans (30 min for 5-min interval)
                news_list = news_agg.get_all_news(symbol, limit=3)
                if news_list:
                    for news in news_list:
                        msg = f"NEWS: {news['title']}\n\nSource: {news['source']}\nDate: {news['date']}"
                        try:
                            import requests
                            payload = {
                                "chat_id": telegram.chat_id,
                                "text": msg,
                            }
                            requests.post(telegram.api_url, json=payload, timeout=5)
                        except:
                            pass

            # 7. Save to CSV log
            row = {
                "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "symbol":     symbol,
                "ltp":        signal.ltp,
                "signal":     signal.action,
                "score":      signal.score,
                "confidence": signal.confidence,
                "target":     signal.target,
                "sl":         signal.sl,
            }
            import pandas as pd
            pd.DataFrame([row]).to_csv(
                "output/signals_log.csv",
                mode="a",
                header=not os.path.exists("output/signals_log.csv"),
                index=False,
            )

            # 6. Wait for next candle
            logger.info(f"⏳ Next scan in {sleep_secs // 60} min(s)…")
            time.sleep(sleep_secs)

    except KeyboardInterrupt:
        logger.info("\n🛑 Agent stopped by user.")
    finally:
        connector.logout()
        logger.info(f"📁 Signal log saved → output/signals_log.csv")


# ── Entry point ───────────────────────────────────────────────────────
def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Angel One Intraday Signal Agent")
    parser.add_argument("--symbol",   default=os.getenv("SYMBOL",   "RELIANCE"))
    parser.add_argument("--exchange", default=os.getenv("EXCHANGE",  "NSE"))
    parser.add_argument("--interval", default=os.getenv("INTERVAL",  "FIVE_MINUTE"))
    args = parser.parse_args()

    # ── Resolve symbol token ──────────────────────────────────────────
    # You can hardcode common tokens here or let the agent search dynamically
    COMMON_TOKENS = {
        "RELIANCE": "2885",
        "INFY":     "1594",
        "TCS":      "11536",
        "SBIN":     "3045",
        "HDFCBANK": "1333",
        "NIFTY":    "99926000",
        "BANKNIFTY":"26009",
    }

    token = COMMON_TOKENS.get(args.symbol.upper())

    if not token:
        # Try dynamic lookup
        logger.info(f"🔍 Searching token for {args.symbol}…")
        connector = AngelConnector()
        if connector.login():
            token = connector.search_symbol_token(args.symbol, args.exchange)
            connector.logout()

    if not token:
        logger.error(f"❌ Could not find token for symbol '{args.symbol}'. Add it to COMMON_TOKENS.")
        sys.exit(1)

    run_agent(
        symbol=args.symbol.upper(),
        token=token,
        exchange=args.exchange,
        interval=args.interval,
    )


if __name__ == "__main__":
    main()
