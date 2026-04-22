"""
Token Regeneration Guide
Steps to get a new Telegram bot token
"""

print("""
╔════════════════════════════════════════════════════════════╗
║         🔄 Telegram Bot Token Regeneration Guide          ║
╚════════════════════════════════════════════════════════════╝

STEP 1: Open Telegram & Find @BotFather
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Open Telegram app
2. Search for: @BotFather
3. Click on it

STEP 2: Get Your Current Bot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Send: /mybots
2. Select your bot (angel_trading_bot or similar)
3. Click "API Token"

STEP 3: Regenerate Token
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Click "Edit Token"
2. Confirm regeneration
3. Copy the NEW token (looks like: 123456:ABC-DEF...)

STEP 4: Update .env File
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Replace the old token with new one:

OLD:
TELEGRAM_BOT_TOKEN=8775992837:AAEQcbgPpz_YlamE-EXgmqOg4gLjCetOOjQ

NEW:
TELEGRAM_BOT_TOKEN=YOUR_NEW_TOKEN_HERE

STEP 5: Test New Token
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run: python test_telegram.py

Should show: SUCCESS! Message sent to Telegram!

STEP 6: Deploy to Render
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Update .env locally
2. Push to GitHub: git push origin main
3. Render auto-deploys with new token

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  IMPORTANT:
- Keep your token SECRET (don't share it)
- Don't commit .env to GitHub (it's in .gitignore)
- Use environment variables in Render dashboard

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
