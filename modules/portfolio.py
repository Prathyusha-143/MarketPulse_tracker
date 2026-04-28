import pandas as pd
import os
from modules.stock_data import get_stock_info

PORTFOLIO_FILE = "data/portfolio.csv"

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        return pd.read_csv(PORTFOLIO_FILE)
    else:
        return pd.DataFrame(columns=["symbol", "quantity", "buy_price"])

def save_portfolio(df):
    df.to_csv(PORTFOLIO_FILE, index=False)

def add_stock(symbol, quantity, buy_price):
    df = load_portfolio()
    new_row = pd.DataFrame([[symbol.upper(), quantity, buy_price]],
                           columns=["symbol", "quantity", "buy_price"])
    df = pd.concat([df, new_row], ignore_index=True)
    save_portfolio(df)

def remove_stock(symbol):
    df = load_portfolio()
    df = df[df["symbol"] != symbol.upper()]
    save_portfolio(df)

def get_portfolio_summary():
    df = load_portfolio()
    if df.empty:
        return df

    summary = []
    for _, row in df.iterrows():
        try:
            info = get_stock_info(row["symbol"])
            current_price = info["current_price"]
            invested = row["buy_price"] * row["quantity"]
            current_value = current_price * row["quantity"]
            pnl = current_value - invested
            pnl_pct = (pnl / invested) * 100

            summary.append({
                "Symbol": row["symbol"],
                "Quantity": row["quantity"],
                "Buy Price": row["buy_price"],
                "Current Price": current_price,
                "Invested": round(invested, 2),
                "Current Value": round(current_value, 2),
                "P&L": round(pnl, 2),
                "P&L %": round(pnl_pct, 2)
            })
        except:
            pass

    return pd.DataFrame(summary)