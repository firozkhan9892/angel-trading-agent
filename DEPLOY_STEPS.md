# 🚀 Complete Deployment Guide

## Step 1: Setup Git Locally

```bash
cd "c:/Users/Admin/Desktop/vibecoding basic to advance/angel_agent"
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"
git init
git add .
git commit -m "Angel One Trading Agent - Initial commit"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `angel-trading-agent`
3. Description: `24/7 Angel One Trading Agent with Telegram alerts and news`
4. Choose: **Public** (easier for Render)
5. Click **Create repository**

## Step 3: Push to GitHub

After creating repo, GitHub will show you commands. Run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/angel-trading-agent.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username!

## Step 4: Deploy on Render

1. Go to https://render.com
2. Sign up with GitHub (easier!)
3. Click **New +** → **Web Service**
4. Select your `angel-trading-agent` repository
5. Fill in settings:
   - **Name:** `angel-trading-agent`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python agent.py`
   - **Plan:** Free (or Paid for guaranteed uptime)

6. Click **Advanced** and add these Environment Variables:
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

7. Click **Create Web Service**

## Step 5: Monitor Deployment

- Render will show deployment logs
- Wait for "Build successful"
- You'll get a URL like: `https://angel-trading-agent.onrender.com`

## Step 6: Keep Alive (Free Plan Only)

To prevent spin-down on free plan:

1. Go to https://uptimerobot.com
2. Sign up (free)
3. Click **Add Monitor**
4. Select **HTTP(s)**
5. URL: `https://angel-trading-agent.onrender.com`
6. Interval: **5 minutes**
7. Save!

---

## ✅ You're Live!

Your agent is now running 24/7 with:
- Trading signals every 5 minutes
- Company news every 30 minutes
- Telegram alerts in real-time

Check your Telegram for startup message!

---

## 📝 Your Details Needed:

Please provide:
1. **GitHub Username:** (e.g., `john-doe`)
2. **GitHub Email:** (e.g., `john@gmail.com`)
3. **Confirm all credentials in `.env` are correct**

Then I'll automate the deployment for you!
