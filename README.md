# Angel One Intraday Trading Agent
Automated Buy/Sell signal generator for Indian stock market using Angel One SmartAPI.

## Features
- Real-time OHLCV data from Angel One
- 5 technical indicators: RSI, MACD, EMA, VWAP, Bollinger Bands
- Multi-indicator confluence scoring system
- BUY/SELL/HOLD signals with confidence levels
- Auto stop-loss & target calculation (2:1 R:R)
- Live logging + CSV signal history
- Market hours aware (9:15 AM - 3:30 PM IST)

## Setup

### Local Development
```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in your Angel One credentials in .env
python agent.py
```

### Render Deployment

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/angel-agent.git
   git push -u origin main
   ```

2. **Create Render Service:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Set environment variables in Render dashboard:
     ```
     API_KEY=your_api_key
     CLIENT_ID=your_client_id
     PASSWORD=your_mpin
     TOTP_SECRET=your_totp_secret
     SYMBOL=RELIANCE
     EXCHANGE=NSE
     INTERVAL=FIVE_MINUTE
     ```
   - Build command: `pip install -r requirements.txt`
   - Start command: `python agent.py`
   - Choose "Free" or "Paid" plan

3. **Monitor Logs:**
   - Render dashboard shows live logs
   - Signals saved to `output/signals_log.csv`

## Usage

```bash
# Default (RELIANCE, 5-min)
python agent.py

# Custom symbol & interval
python agent.py --symbol INFY --interval ONE_MINUTE
python agent.py --symbol TCS --interval FIFTEEN_MINUTE
```

## Signal Scoring

| Indicator | BUY | SELL |
|-----------|-----|------|
| RSI < 35  | +20 | -20 (RSI > 65) |
| MACD Cross| +25 | -25 |
| EMA 9>21  | +20 | -20 |
| Price > VWAP | +15 | -15 |
| BB Lower  | +20 | -20 (BB Upper) |
| **Total** | **+100** | **-100** |

**Thresholds:**
- BUY: Score ≥ +40
- SELL: Score ≤ -40
- HOLD: -40 < Score < +40

## Files

- `agent.py` - Main runner
- `modules/angel_connector.py` - API connection
- `modules/indicators.py` - Technical indicators
- `modules/signal_generator.py` - Signal logic
- `requirements.txt` - Dependencies
- `.env` - Credentials (keep secret!)
- `Procfile` - Render deployment config

## Notes

- Agent respects market hours (9:15 AM - 3:30 PM IST)
- Logs saved to `logs/` directory
- Signals exported to `output/signals_log.csv`
- Stop-loss: 0.5% | Target: 1.0% (2:1 R:R)
