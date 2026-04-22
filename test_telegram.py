"""
Telegram Test Script
Quick way to verify bot token and chat ID are working
"""

import os
import sys
from dotenv import load_dotenv

# Fix Windows encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))
from modules.telegram_notifier import TelegramNotifier


def test_telegram():
    """Test Telegram connection."""
    print("\n" + "="*50)
    print("Testing Telegram Connection")
    print("="*50 + "\n")

    notifier = TelegramNotifier()

    # Check credentials
    if not notifier.bot_token:
        print("ERROR: TELEGRAM_BOT_TOKEN not set in .env")
        return False

    if not notifier.chat_id:
        print("ERROR: TELEGRAM_CHAT_ID not set in .env")
        return False

    if not notifier.enabled:
        print("ERROR: TELEGRAM_ENABLED is false")
        return False

    print(f"OK - Bot Token: {notifier.bot_token[:20]}...")
    print(f"OK - Chat ID: {notifier.chat_id}")
    print(f"OK - Enabled: {notifier.enabled}\n")

    # Send test message
    print("Sending test message...\n")

    test_message = """Bot is Running!

Telegram integration is working!

This is a test message from Angel One Trading Agent.

If you see this, your bot is properly configured.
"""

    import requests
    try:
        payload = {
            "chat_id": notifier.chat_id,
            "text": test_message,
            "parse_mode": "Markdown",
        }

        response = requests.post(notifier.api_url, json=payload, timeout=5)

        if response.status_code == 200:
            print("SUCCESS! Message sent to Telegram!")
            print("\nCheck your Telegram chat for the message.\n")
            return True
        else:
            print(f"FAILED! Status: {response.status_code}")
            print(f"Response: {response.text}\n")
            return False

    except Exception as e:
        print(f"ERROR: {e}\n")
        return False


if __name__ == "__main__":
    success = test_telegram()
    sys.exit(0 if success else 1)
