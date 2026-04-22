# 🚀 Quick Start Guide

## ✅ Your Setup is Complete!

Your Angel One Trading Agent is ready with:
- ✅ Angel One SmartAPI integration
- ✅ 5 technical indicators
- ✅ Telegram alerts (VERIFIED WORKING)
- ✅ Free Render deployment ready

---

## 🎯 Test Locally First

### 1. Install Dependencies
```bash
cd angel_agent
pip install -r requirements.txt
```

### 2. Verify Telegram
```bash
python test_telegram.py
# Should show: SUCCESS! Message sent to Telegram!
```

### 3. Run Agent (Market Hours Only)
```bash
python agent.py
# Runs 9:15 AM - 3:30 PM IST only
# You'll get startup message on Telegram
```

---

## 📱 What You'll Receive on Telegram

### When Agent Starts
```
Bot is Running!
Symbol: RELIANCE
Interval: FIVE_MINUTE
```

### When BUY Signal Generated
```
BUY SIGNAL

LTP: ₹2500.50
Score: +65
Confidence: HIGH

Target: ₹2526.00
Stop Loss: ₹2488.00
```

### When SELL Signal Generated
```
SELL SIGNAL

LTP: ₹2480.25
Score: -72
Confidence: HIGH

Target: ₹2455.00
Stop Loss: ₹2498.00
```

---

## 🌐 Deploy to Render (24/7)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Angel One agent with Telegram"
git remote add origin https://github.com/YOUR_USERNAME/angel-agent.git
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Settings:
   - Build: `pip install -r requirements.txt`
   - Start: `python agent.py`
5. Add Environment Variables:
   ```
   API_KEY=cvOyKdcC
   CLIENT_ID=F24431
   PASSWORD=9892
   TOTP_SECRET=MZHYJE5XO6C2T55OC2RHOERRMA
   SYMBOL=RELIANCE
   EXCHANGE=NSE
   INTERVAL=FIVE_MINUTE
   TELEGRAM_BOT_TOKEN=8775992837:AAEQcbgPpz_YlamE-EXgmqOg4gLjCetOOjQ
   TELEGRAM_CHAT_ID=1067001644
   TELEGRAM_ENABLED=true
   ```
6. Click "Create Web Service"

### Step 3: Keep Alive (Free Plan)
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Sign up (free)
3. Add Monitor:
   - URL: `https://your-app.onrender.com`
   - Interval: 5 minutes
4. Done! Your app stays awake 24/7

---

## 📊 Monitor Your Agent

**Render Dashboard:**
- View live logs
- Check signal history
- Download CSV reports

**Telegram:**
- Get instant alerts
- See all signals in real-time

**Local Logs:**
- `logs/agent_YYYYMMDD.log` - Detailed logs
- `output/signals_log.csv` - All signals

---

## 🔧 Troubleshooting

### Agent not starting?
```bash
python agent.py
# Check for errors in console
```

### No Telegram messages?
```bash
python test_telegram.py
# Verify bot token and chat ID
```

### Market hours check:
- Agent only runs: **9:15 AM - 3:30 PM IST**
- Weekdays only (Mon-Fri)
- Outside hours: Agent sleeps

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `agent.py` | Main runner |
| `.env` | Your credentials (KEEP SECRET!) |
| `test_telegram.py` | Test Telegram connection |
| `requirements.txt` | Dependencies |
| `Procfile` | Render config |
| `TELEGRAM.md` | Telegram setup details |
| `FREE_PLAN.md` | Free tier optimization |

---

## 🎉 You're All Set!

Your 24/7 automated trading agent is ready to deploy!

**Next Steps:**
1. ✅ Test locally with `python agent.py`
2. ✅ Push to GitHub
3. ✅ Deploy on Render
4. ✅ Setup UptimeRobot (free plan)
5. ✅ Get real-time Telegram alerts!

**Happy Trading!** 📈💰
