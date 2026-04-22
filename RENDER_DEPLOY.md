# 🚀 Render Deployment - Step by Step

## Your Repository
**URL:** https://github.com/firozkhan9892/angel-trading-agent

---

## Deploy on Render (5 minutes)

### Step 1: Go to Render
1. Open https://render.com
2. Click **Sign up** (or Sign in if you have account)
3. Choose **Sign up with GitHub**
4. Authorize Render to access your GitHub

### Step 2: Create Web Service
1. Click **New +** button (top right)
2. Select **Web Service**
3. Connect your GitHub account if not already connected
4. Find and select: `angel-trading-agent`
5. Click **Connect**

### Step 3: Configure Service
Fill in these settings:

- **Name:** `angel-trading-agent`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python agent.py`
- **Plan:** Free (or Paid for guaranteed uptime)

### Step 4: Add Environment Variables
Click **Advanced** and add these variables:

```
API_KEY=cvOyKdcC
CLIENT_ID=F24431
PASSWORD=9892
TOTP_SECRET=MZHYJE5XO6C2T55OC2RHOERRMA
SYMBOL=RELIANCE
EXCHANGE=NSE
INTERVAL=FIVE_MINUTE
TELEGRAM_BOT_TOKEN=8703305303:AAHEgrFr2...
TELEGRAM_CHAT_ID=1067001644
TELEGRAM_ENABLED=true
```

### Step 5: Deploy
Click **Create Web Service**

Render will:
- Build your app (2-3 minutes)
- Start the agent
- Give you a live URL

### Step 6: Monitor
- Check logs in Render dashboard
- You should get Telegram message: "Agent Started"
- Trading signals will come every 5 minutes

---

## Keep Alive (Free Plan)

To prevent spin-down:

1. Go to https://uptimerobot.com
2. Sign up (free)
3. Add Monitor:
   - Type: HTTP(s)
   - URL: Your Render URL (from dashboard)
   - Interval: 5 minutes
4. Save!

---

## ✅ Done!

Your agent is now live 24/7 with:
- Trading signals every 5 minutes
- Company news every 30 minutes
- Telegram alerts in real-time

**Check your Telegram for startup message!** 📱
