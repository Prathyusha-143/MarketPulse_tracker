import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_stock_insights(stock_info, symbol):
    prompt = f"""
    You are a financial analyst. Analyze this stock data for {symbol} and give a brief 4-5 line insight:
    
    Company: {stock_info['name']}
    Current Price: {stock_info['current_price']}
    Open: {stock_info['open']}
    High: {stock_info['high']}
    Low: {stock_info['low']}
    Volume: {stock_info['volume']}
    Market Cap: {stock_info['market_cap']}
    52 Week High: {stock_info['52_week_high']}
    52 Week Low: {stock_info['52_week_low']}
    
    Give a short, clear analysis in simple English.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def chat_with_ai(messages):
    response = client.chat.completions.create(
       model="llama-3.3-70b-versatile",
        messages=messages
    )
    return response.choices[0].message.content