import yfinance as yf
import pandas as pd

def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    
    # Try multiple price fields
    price = (
        info.get("currentPrice") or
        info.get("regularMarketPrice") or
        info.get("previousClose") or
        stock.fast_info.get("last_price") or
        0
    )
    
    return {
        "name": info.get("longName", symbol),
        "current_price": price,
        "open": info.get("open") or info.get("regularMarketOpen") or 0,
        "high": info.get("dayHigh") or info.get("regularMarketDayHigh") or 0,
        "low": info.get("dayLow") or info.get("regularMarketDayLow") or 0,
        "volume": info.get("volume") or info.get("regularMarketVolume") or 0,
        "market_cap": info.get("marketCap") or 0,
        "52_week_high": info.get("fiftyTwoWeekHigh") or 0,
        "52_week_low": info.get("fiftyTwoWeekLow") or 0,
    }

def get_historical_data(symbol, period="6mo"):
    stock = yf.Ticker(symbol)
    df = stock.history(period=period)
    df.reset_index(inplace=True)
    return df