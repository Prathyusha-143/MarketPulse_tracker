import ta
import pandas as pd

def get_signals(df):
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()

    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()

    bb = ta.volatility.BollingerBands(df['Close'])
    df['BB_High'] = bb.bollinger_hband()
    df['BB_Low'] = bb.bollinger_lband()

    latest = df.iloc[-1]
    rsi = latest['RSI']

    if rsi < 30:
        signal = "🟢 BUY"
        reason = f"RSI is {rsi:.2f} — Stock is oversold"
    elif rsi > 70:
        signal = "🔴 SELL"
        reason = f"RSI is {rsi:.2f} — Stock is overbought"
    else:
        signal = "🟡 HOLD"
        reason = f"RSI is {rsi:.2f} — Stock is neutral"

    return {
        "signal": signal,
        "reason": reason,
        "rsi": round(rsi, 2),
        "macd": round(latest['MACD'], 4),
        "bb_high": round(latest['BB_High'], 2),
        "bb_low": round(latest['BB_Low'], 2)
    }