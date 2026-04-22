# 🚀 Render Deployment Guide

## Step 1: Initialize Git Repository

```bash
cd angel_agent
git init
git add .
git commit -m "Initial commit: Angel One trading agent"
```

## Step 2: Push to GitHub

```bash
# Create new repo on GitHub (https://github.com/new)
git remote add origin https://github.com/YOUR_USERNAME/angel-agent.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Render

### Option A: Web Service (Recommended for 24/7)

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select `angel-agent` repository
5. Fill in deployment settings:
   - **Name:** `angel-trading-agent`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python agent.py`
   - **Plan:** Free (or Paid for guaranteed uptime)

6. Click **"Advanced"** and add environment variables:
   ```
   API_KEY=cvOyKdcC
   CLIENT_ID=F24431
   PASSWORD=9892
   TOTP_SECRET=MZHYJE5XO6C2T55OC2RHOERRMA
   SYMBOL=RELIANCE
   EXCHANGE=NSE
   INTERVAL=FIVE_MINUTE
   ```

7. Click **"Create Web Service"**

### Option B: Docker (More Control)

1. Same steps 1-3 above
2. On Render, click **"New +"** → **"Web Service"**
3. Select repository
4. Set **Runtime** to `Docker`
5. Add same environment variables
6. Deploy!

## Step 4: Monitor Live

- **Render Dashboard:** View logs in real-time
- **Signal Output:** Logs saved to `output/signals_log.csv`
- **Agent Logs:** Check `logs/agent_YYYYMMDD.log`

## Step 5: Keep Running 24/7

### Free Plan Limitations:
- Spins down after 15 min of inactivity
- Not ideal for 24/7 trading

### Paid Plan (Recommended):
- Upgrade to **Starter** or **Standard** plan
- Guaranteed uptime
- Better for production trading

## Troubleshooting

### Agent not starting?
```bash
# Check logs in Render dashboard
# Common issues:
# 1. Missing environment variables
# 2. Invalid Angel One credentials
# 3. Network connectivity
```

### Signals not generating?
- Verify market hours (9:15 AM - 3:30 PM IST)
- Check if Angel One API is accessible
- Review logs for errors

### Update code?
```bash
git add .
git commit -m "Update: new features"
git push origin main
# Render auto-deploys on push!
```

## Alternative Hosting Options

| Platform | Cost | Uptime | Best For |
|----------|------|--------|----------|
| **Render** | Free/Paid | 99.9% (Paid) | Easy deployment |
| **Railway** | Pay-as-you-go | 99.9% | Flexible pricing |
| **Heroku** | Paid only | 99.9% | Reliable |
| **AWS EC2** | Paid | 99.99% | Full control |
| **DigitalOcean** | $5+/mo | 99.99% | VPS control |

## Local Testing Before Deploy

```bash
# Test locally first
python agent.py --symbol INFY --interval FIVE_MINUTE

# Check logs
tail -f logs/agent_*.log

# Verify signals
cat output/signals_log.csv
```

---

**Your agent is ready for 24/7 deployment!** 🎉
