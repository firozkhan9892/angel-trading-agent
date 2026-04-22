"""
Technical Indicators Engine
Computes RSI, MACD, SMA, EMA, Bollinger Bands, VWAP on OHLCV DataFrame
"""

import pandas as pd
import numpy as np


class IndicatorEngine:
    """
    Stateless helper — pass a DataFrame, get one back with indicator columns added.
    All methods are @staticmethod so no instantiation is needed.
    """

    # ------------------------------------------------------------------
    # Moving Averages
    # ------------------------------------------------------------------
    @staticmethod
    def add_sma(df: pd.DataFrame, periods: list[int] = [9, 21, 50]) -> pd.DataFrame:
        """Simple Moving Averages for given periods."""
        for p in periods:
            df[f"SMA_{p}"] = df["close"].rolling(window=p).mean().round(2)
        return df

    @staticmethod
    def add_ema(df: pd.DataFrame, periods: list[int] = [9, 21]) -> pd.DataFrame:
        """Exponential Moving Averages for given periods."""
        for p in periods:
            df[f"EMA_{p}"] = df["close"].ewm(span=p, adjust=False).mean().round(2)
        return df

    # ------------------------------------------------------------------
    # RSI
    # ------------------------------------------------------------------
    @staticmethod
    def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        Relative Strength Index.
        Overbought > 70 | Oversold < 30
        """
        delta = df["close"].diff()
        gain  = delta.clip(lower=0)
        loss  = (-delta).clip(lower=0)

        avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
        avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

        rs          = avg_gain / avg_loss.replace(0, np.nan)
        df["RSI"]   = (100 - (100 / (1 + rs))).round(2)
        return df

    # ------------------------------------------------------------------
    # MACD
    # ------------------------------------------------------------------
    @staticmethod
    def add_macd(
        df: pd.DataFrame,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> pd.DataFrame:
        """
        MACD Line, Signal Line, Histogram.
        Bullish crossover: MACD crosses above Signal
        Bearish crossover: MACD crosses below Signal
        """
        ema_fast          = df["close"].ewm(span=fast, adjust=False).mean()
        ema_slow          = df["close"].ewm(span=slow, adjust=False).mean()
        df["MACD"]        = (ema_fast - ema_slow).round(4)
        df["MACD_Signal"] = df["MACD"].ewm(span=signal, adjust=False).mean().round(4)
        df["MACD_Hist"]   = (df["MACD"] - df["MACD_Signal"]).round(4)
        return df

    # ------------------------------------------------------------------
    # Bollinger Bands
    # ------------------------------------------------------------------
    @staticmethod
    def add_bollinger(df: pd.DataFrame, period: int = 20, std_dev: float = 2.0) -> pd.DataFrame:
        """
        Bollinger Bands — Upper / Middle / Lower.
        Price near upper band → overbought, near lower → oversold.
        """
        sma               = df["close"].rolling(window=period).mean()
        std               = df["close"].rolling(window=period).std()
        df["BB_Upper"]    = (sma + std_dev * std).round(2)
        df["BB_Middle"]   = sma.round(2)
        df["BB_Lower"]    = (sma - std_dev * std).round(2)
        df["BB_Width"]    = ((df["BB_Upper"] - df["BB_Lower"]) / df["BB_Middle"] * 100).round(2)
        return df

    # ------------------------------------------------------------------
    # VWAP
    # ------------------------------------------------------------------
    @staticmethod
    def add_vwap(df: pd.DataFrame) -> pd.DataFrame:
        """
        Volume Weighted Average Price — intraday benchmark.
        Price > VWAP → bullish bias | Price < VWAP → bearish bias
        """
        typical_price = (df["high"] + df["low"] + df["close"]) / 3
        df["VWAP"]    = (
            (typical_price * df["volume"]).cumsum() /
            df["volume"].cumsum()
        ).round(2)
        return df

    # ------------------------------------------------------------------
    # All-in-one
    # ------------------------------------------------------------------
    @staticmethod
    def compute_all(df: pd.DataFrame) -> pd.DataFrame:
        """Apply all indicators in one call."""
        df = IndicatorEngine.add_sma(df)
        df = IndicatorEngine.add_ema(df)
        df = IndicatorEngine.add_rsi(df)
        df = IndicatorEngine.add_macd(df)
        df = IndicatorEngine.add_bollinger(df)
        df = IndicatorEngine.add_vwap(df)
        return df
