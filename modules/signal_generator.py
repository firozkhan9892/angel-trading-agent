"""
Buy / Sell Signal Generator
Multi-indicator confluence scoring system for intraday signals
"""

import pandas as pd
from dataclasses import dataclass
from logzero import logger


@dataclass
class Signal:
    action:      str   # BUY | SELL | HOLD
    score:       int   # Confluence score (-100 to +100)
    confidence:  str   # HIGH | MEDIUM | LOW
    reasons:     list  # Human-readable list of reasons
    ltp:         float # Last traded price at signal time
    sl:          float # Suggested Stop Loss
    target:      float # Suggested Target


class SignalGenerator:
    """
    Scoring-based multi-indicator signal engine.

    Scoring rubric (each indicator contributes points):
      RSI          : +20 (oversold→BUY) / -20 (overbought→SELL)
      MACD         : +25 (bullish cross) / -25 (bearish cross)
      EMA crossover: +20 (EMA9 > EMA21) / -20
      VWAP         : +15 (price > VWAP)  / -15
      Bollinger    : +20 (near lower band→BUY) / -20 (near upper band→SELL)
    Max possible   : +100 / -100
    """

    # Thresholds
    BUY_THRESHOLD  =  40   # score >= +40  → BUY
    SELL_THRESHOLD = -40   # score <= -40  → SELL

    SL_PCT     = 0.005   # 0.5% stop loss
    TARGET_PCT = 0.010   # 1.0% target  (2:1 R:R)

    # ------------------------------------------------------------------
    def generate(self, data: list) -> Signal:
        """
        Analyse the latest candle and return a Signal.

        Args:
            data: List of dicts with OHLCV + indicator columns

        Returns:
            Signal dataclass
        """
        if not data or len(data) < 30:
            logger.warning("Not enough data for signal generation")
            return self._hold_signal(0.0, "Insufficient data")

        latest = data[-1]
        prev   = data[-2]
        score  = 0
        reasons = []

        # RSI
        rsi = latest.get("RSI", 50)
        if rsi and rsi < 35:
            score += 20
            reasons.append(f"RSI oversold ({rsi:.1f} < 35) - Bullish")
        elif rsi and rsi > 65:
            score -= 20
            reasons.append(f"RSI overbought ({rsi:.1f} > 65) - Bearish")
        else:
            reasons.append(f"RSI neutral ({rsi:.1f})")

        # MACD crossover
        macd = latest.get("MACD", 0)
        macd_sig = latest.get("MACD_Signal", 0)
        p_macd = prev.get("MACD", 0)
        p_sig = prev.get("MACD_Signal", 0)

        if p_macd and p_sig and macd and macd_sig:
            if p_macd <= p_sig and macd > macd_sig:
                score += 25
                reasons.append("MACD bullish crossover - BUY signal")
            elif p_macd >= p_sig and macd < macd_sig:
                score -= 25
                reasons.append("MACD bearish crossover - SELL signal")
            elif macd > macd_sig:
                score += 10
                reasons.append("MACD above signal - Bullish momentum")
            else:
                score -= 10
                reasons.append("MACD below signal - Bearish momentum")

        # EMA Crossover
        ema9 = latest.get("EMA_9", latest["close"])
        ema21 = latest.get("EMA_21", latest["close"])
        p_ema9 = prev.get("EMA_9", prev["close"])
        p_ema21 = prev.get("EMA_21", prev["close"])

        if p_ema9 and p_ema21 and ema9 and ema21:
            if p_ema9 <= p_ema21 and ema9 > ema21:
                score += 20
                reasons.append("EMA 9 crossed above EMA 21 - Golden cross")
            elif p_ema9 >= p_ema21 and ema9 < ema21:
                score -= 20
                reasons.append("EMA 9 crossed below EMA 21 - Death cross")
            elif ema9 > ema21:
                score += 8
                reasons.append("EMA 9 > EMA 21 - Bullish trend")
            else:
                score -= 8
                reasons.append("EMA 9 < EMA 21 - Bearish trend")

        # VWAP
        close = latest["close"]
        vwap = latest.get("VWAP", close)

        if vwap:
            if close > vwap:
                score += 15
                reasons.append(f"Price > VWAP - Bullish bias")
            else:
                score -= 15
                reasons.append(f"Price < VWAP - Bearish bias")

        # Bollinger Bands
        bb_upper = latest.get("BB_Upper", close * 1.02)
        bb_lower = latest.get("BB_Lower", close * 0.98)

        if bb_upper and bb_lower:
            bb_pct = (close - bb_lower) / (bb_upper - bb_lower + 1e-9)

            if bb_pct < 0.20:
                score += 20
                reasons.append(f"Price near BB Lower - Reversal likely (BUY)")
            elif bb_pct > 0.80:
                score -= 20
                reasons.append(f"Price near BB Upper - Reversal likely (SELL)")
            else:
                reasons.append(f"Price mid-Bollinger Band")

        return self._build_signal(score, reasons, close)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _build_signal(self, score: int, reasons: list, ltp: float) -> Signal:
        if score >= self.BUY_THRESHOLD:
            action = "BUY"
            sl     = round(ltp * (1 - self.SL_PCT), 2)
            target = round(ltp * (1 + self.TARGET_PCT), 2)
        elif score <= self.SELL_THRESHOLD:
            action = "SELL"
            sl     = round(ltp * (1 + self.SL_PCT), 2)
            target = round(ltp * (1 - self.TARGET_PCT), 2)
        else:
            action = "HOLD"
            sl     = 0.0
            target = 0.0

        abs_score   = abs(score)
        confidence  = "HIGH" if abs_score >= 70 else "MEDIUM" if abs_score >= 40 else "LOW"

        signal = Signal(
            action=action,
            score=score,
            confidence=confidence,
            reasons=reasons,
            ltp=ltp,
            sl=sl,
            target=target,
        )
        self._log_signal(signal)
        return signal

    def _hold_signal(self, ltp: float, reason: str) -> Signal:
        return Signal("HOLD", 0, "LOW", [reason], ltp, 0.0, 0.0)

    @staticmethod
    def _log_signal(sig: Signal):
        emoji = {"BUY": "🟢", "SELL": "🔴", "HOLD": "🟡"}.get(sig.action, "⚪")
        logger.info(
            f"{emoji} SIGNAL: {sig.action} | Score: {sig.score:+d} | "
            f"Confidence: {sig.confidence} | LTP: ₹{sig.ltp}"
        )
        if sig.action != "HOLD":
            logger.info(f"   🎯 Target: ₹{sig.target}  |  🛑 SL: ₹{sig.sl}")
