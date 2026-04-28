import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go

def predict_price(df, days=30):
    df = df[['Date', 'Close']].copy()
    df['Date_Ordinal'] = pd.to_datetime(df['Date']).map(lambda x: x.toordinal())

    scaler = MinMaxScaler()
    df['Close_Scaled'] = scaler.fit_transform(df[['Close']])

    X = df['Date_Ordinal'].values.reshape(-1, 1)
    y = df['Close_Scaled'].values

    model = LinearRegression()
    model.fit(X, y)

    # Predict future dates
    last_date = pd.to_datetime(df['Date'].iloc[-1])
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, days+1)]
    future_ordinals = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)

    future_scaled = model.predict(future_ordinals)
    future_prices = scaler.inverse_transform(future_scaled.reshape(-1, 1)).flatten()

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Close'],
        name='Historical Price',
        line=dict(color='cyan')
    ))
    fig.add_trace(go.Scatter(
        x=future_dates, y=future_prices,
        name='Predicted Price',
        line=dict(color='orange', dash='dash')
    ))
    fig.update_layout(
        title="Price Prediction (Next 30 Days)",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark"
    )

    return fig, round(future_prices[-1], 2)