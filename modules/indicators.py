"""
Technical Indicators Engine
Computes RSI, MACD, SMA, EMA, Bollinger Bands, VWAP without pandas
"""


class IndicatorEngine:
    """Calculate indicators from OHLCV data."""

    @staticmethod
    def add_sma(data: list, periods: list = [9, 21, 50]) -> list:
        """Simple Moving Average."""
        for p in periods:
            for i in range(len(data)):
                if i < p - 1:
                    data[i][f"SMA_{p}"] = None
                else:
                    avg = sum(d["close"] for d in data[i-p+1:i+1]) / p
                    data[i][f"SMA_{p}"] = round(avg, 2)
        return data

    @staticmethod
    def add_ema(data: list, periods: list = [9, 21]) -> list:
        """Exponential Moving Average."""
        for p in periods:
            multiplier = 2 / (p + 1)
            for i in range(len(data)):
                if i < p - 1:
                    data[i][f"EMA_{p}"] = None
                elif i == p - 1:
                    avg = sum(d["close"] for d in data[:p]) / p
                    data[i][f"EMA_{p}"] = round(avg, 2)
                else:
                    prev_ema = data[i-1][f"EMA_{p}"]
                    ema = data[i]["close"] * multiplier + prev_ema * (1 - multiplier)
                    data[i][f"EMA_{p}"] = round(ema, 2)
        return data

    @staticmethod
    def add_rsi(data: list, period: int = 14) -> list:
        """Relative Strength Index."""
        for i in range(len(data)):
            if i < period:
                data[i]["RSI"] = None
            else:
                gains = []
                losses = []
                for j in range(i - period + 1, i + 1):
                    change = data[j]["close"] - data[j-1]["close"]
                    if change > 0:
                        gains.append(change)
                        losses.append(0)
                    else:
                        gains.append(0)
                        losses.append(abs(change))

                avg_gain = sum(gains) / period
                avg_loss = sum(losses) / period

                if avg_loss == 0:
                    rsi = 100
                else:
                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))

                data[i]["RSI"] = round(rsi, 2)
        return data

    @staticmethod
    def add_macd(data: list, fast: int = 12, slow: int = 26, signal: int = 9) -> list:
        """MACD Line, Signal Line, Histogram."""
        # Calculate EMAs
        ema_fast = [None] * len(data)
        ema_slow = [None] * len(data)

        mult_fast = 2 / (fast + 1)
        mult_slow = 2 / (slow + 1)

        for i in range(len(data)):
            if i == fast - 1:
                ema_fast[i] = sum(d["close"] for d in data[:fast]) / fast
            elif i > fast - 1:
                ema_fast[i] = data[i]["close"] * mult_fast + ema_fast[i-1] * (1 - mult_fast)

            if i == slow - 1:
                ema_slow[i] = sum(d["close"] for d in data[:slow]) / slow
            elif i > slow - 1:
                ema_slow[i] = data[i]["close"] * mult_slow + ema_slow[i-1] * (1 - mult_slow)

        # Calculate MACD
        macd_line = []
        for i in range(len(data)):
            if ema_fast[i] and ema_slow[i]:
                macd_line.append(ema_fast[i] - ema_slow[i])
            else:
                macd_line.append(None)

        # Calculate Signal line
        signal_line = [None] * len(data)
        mult_signal = 2 / (signal + 1)

        for i in range(len(data)):
            if i == slow + signal - 2 and macd_line[i]:
                signal_line[i] = sum(m for m in macd_line[i-signal+1:i+1] if m) / signal
            elif i > slow + signal - 2 and macd_line[i]:
                signal_line[i] = macd_line[i] * mult_signal + signal_line[i-1] * (1 - mult_signal)

        # Add to data
        for i in range(len(data)):
            data[i]["MACD"] = round(macd_line[i], 4) if macd_line[i] else None
            data[i]["MACD_Signal"] = round(signal_line[i], 4) if signal_line[i] else None
            if macd_line[i] and signal_line[i]:
                data[i]["MACD_Hist"] = round(macd_line[i] - signal_line[i], 4)
            else:
                data[i]["MACD_Hist"] = None

        return data

    @staticmethod
    def add_bollinger(data: list, period: int = 20, std_dev: float = 2.0) -> list:
        """Bollinger Bands."""
        for i in range(len(data)):
            if i < period - 1:
                data[i]["BB_Upper"] = None
                data[i]["BB_Middle"] = None
                data[i]["BB_Lower"] = None
                data[i]["BB_Width"] = None
            else:
                closes = [d["close"] for d in data[i-period+1:i+1]]
                sma = sum(closes) / period
                variance = sum((c - sma) ** 2 for c in closes) / period
                std = variance ** 0.5

                upper = sma + std_dev * std
                lower = sma - std_dev * std
                width = ((upper - lower) / sma * 100) if sma else 0

                data[i]["BB_Upper"] = round(upper, 2)
                data[i]["BB_Middle"] = round(sma, 2)
                data[i]["BB_Lower"] = round(lower, 2)
                data[i]["BB_Width"] = round(width, 2)

        return data

    @staticmethod
    def add_vwap(data: list) -> list:
        """Volume Weighted Average Price."""
        cumulative_tp_vol = 0
        cumulative_vol = 0

        for i in range(len(data)):
            tp = (data[i]["high"] + data[i]["low"] + data[i]["close"]) / 3
            cumulative_tp_vol += tp * data[i]["volume"]
            cumulative_vol += data[i]["volume"]

            if cumulative_vol > 0:
                data[i]["VWAP"] = round(cumulative_tp_vol / cumulative_vol, 2)
            else:
                data[i]["VWAP"] = None

        return data

    @staticmethod
    def compute_all(data: list) -> list:
        """Apply all indicators."""
        data = IndicatorEngine.add_sma(data)
        data = IndicatorEngine.add_ema(data)
        data = IndicatorEngine.add_rsi(data)
        data = IndicatorEngine.add_macd(data)
        data = IndicatorEngine.add_bollinger(data)
        data = IndicatorEngine.add_vwap(data)
        return data

