# 📱 Telegram Setup Guide

## Step 1: Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/start`
3. Send `/newbot`
4. Follow prompts:
   - Bot name: `Angel Trading Agent`
   - Bot username: `angel_trading_bot` (must be unique)
5. Copy the **API Token** (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

## Step 2: Get Your Chat ID

1. Search for **@userinfobot** in Telegram
2. Send `/start`
3. It will show your **User ID** (e.g., `123456789`)
4. This is your `TELEGRAM_CHAT_ID`

## Step 3: Update `.env`

```bash
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=123456789
TELEGRAM_ENABLED=true
```

## Step 4: Test Locally

```bash
python agent.py
# You should get a startup message on Telegram
```

## Step 5: Deploy to Render

Add these env vars in Render dashboard:
```
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
TELEGRAM_ENABLED=true
```

---

## What You'll Receive

### 🟢 BUY Signal
```
🟢 BUY SIGNAL

💰 LTP: ₹2500.50
📊 Score: +65
🎯 Confidence: HIGH

🎯 Target: ₹2526.00
🛑 Stop Loss: ₹2488.00

⏰ 2026-04-22 14:35:28 IST
```

### 🔴 SELL Signal
```
🔴 SELL SIGNAL

💰 LTP: ₹2480.25
📊 Score: -72
🎯 Confidence: HIGH

🎯 Target: ₹2455.00
🛑 Stop Loss: ₹2498.00

⏰ 2026-04-22 14:40:15 IST
```

### 🚀 Startup Alert
```
🚀 Agent Started

📌 Symbol: RELIANCE
⏱️  Interval: FIVE_MINUTE
🕐 Time: 2026-04-22 09:15:00 IST

Watching for signals...
```

---

## Troubleshooting

### Not receiving messages?
- ✅ Check bot token is correct
- ✅ Check chat ID is correct
- ✅ Make sure `TELEGRAM_ENABLED=true`
- ✅ Verify bot has permission to send messages

### Bot not responding?
- Go to @BotFather
- Send `/mybots`
- Select your bot
- Check "Bot Settings" → "Privacy Mode" is OFF

### Test message manually:
```bash
curl -X POST https://api.telegram.org/bot{TOKEN}/sendMessage \
  -d chat_id={CHAT_ID} \
  -d text="Test message"
```

---

## Privacy & Security

⚠️ **Keep your bot token & chat ID secret!**
- Don't commit `.env` to GitHub (use `.gitignore`)
- Use environment variables in Render
- Never share your bot token publicly

---

**Your agent will now send real-time trading alerts to Telegram!** 📲
