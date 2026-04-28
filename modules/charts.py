import plotly.graph_objects as go
import pandas as pd

def candlestick_chart(df, symbol):
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name=symbol
    )])

    fig.update_layout(
        title=f"{symbol} Price Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )
    return fig

def moving_average_chart(df, symbol):
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close Price', line=dict(color='cyan')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], name='20 Day MA', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], name='50 Day MA', line=dict(color='red')))

    fig.update_layout(
        title=f"{symbol} Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark"
    )
    return fig