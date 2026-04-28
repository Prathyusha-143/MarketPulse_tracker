import streamlit as st
import plotly.express as px
from modules.stock_data import get_stock_info, get_historical_data
from modules.charts import candlestick_chart, moving_average_chart
from modules.signals import get_signals
from modules.news_sentiment import get_news_sentiment
from modules.portfolio import load_portfolio, add_stock, remove_stock, get_portfolio_summary
from modules.ml_prediction import predict_price
from modules.ai_assistant import get_stock_insights, chat_with_ai

# Page Config
st.set_page_config(
    page_title="MarketPulse Tracker",
    page_icon="📈",
    layout="wide"
)

st.title("📈 MarketPulse Tracker")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "💼 Portfolio",
    "🔮 Prediction",
    "📰 News & Sentiment",
    "💬 AI Assistant"
])

# ─────────────────────────────────────────
# TAB 1 — DASHBOARD
# ─────────────────────────────────────────
with tab1:
    st.header("📊 Stock Dashboard")
    symbol = st.text_input("Enter Stock Symbol (e.g. AAPL, RELIANCE.NS)", value="AAPL")

    if symbol:
        with st.spinner("Fetching data..."):
            try:
                info = get_stock_info(symbol)
                df = get_historical_data(symbol)
                signals = get_signals(df)

                # Stock Info
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Current Price", f"${info['current_price']}")
                col2.metric("High", f"${info['high']}")
                col3.metric("Low", f"${info['low']}")
                col4.metric("Volume", f"{info['volume']:,}")

                st.markdown("---")

                # Signal
                st.subheader("🚦 Buy/Sell Signal")
                st.markdown(f"## {signals['signal']}")
                st.write(signals['reason'])
                col1, col2, col3 = st.columns(3)
                col1.metric("RSI", signals['rsi'])
                col2.metric("BB High", signals['bb_high'])
                col3.metric("BB Low", signals['bb_low'])

                st.markdown("---")

                # Charts
                st.subheader("🕯️ Candlestick Chart")
                st.plotly_chart(candlestick_chart(df, symbol), use_container_width=True)

                st.subheader("📉 Moving Averages")
                st.plotly_chart(moving_average_chart(df, symbol), use_container_width=True)

                st.markdown("---")

                # AI Insights
                st.subheader("🧠 AI Insights")
                with st.spinner("Generating AI insights..."):
                    insights = get_stock_insights(info, symbol)
                    st.info(insights)

            except Exception as e:
                st.error(f"Error fetching data: {e}")

# ─────────────────────────────────────────
# TAB 2 — PORTFOLIO
# ─────────────────────────────────────────
with tab2:
    st.header("💼 My Portfolio")

    # Add Stock
    st.subheader("➕ Add Stock")
    col1, col2, col3 = st.columns(3)
    with col1:
        p_symbol = st.text_input("Symbol", key="p_symbol")
    with col2:
        p_qty = st.number_input("Quantity", min_value=1, value=1, key="p_qty")
    with col3:
        p_price = st.number_input("Buy Price", min_value=0.0, value=0.0, key="p_price")

    if st.button("Add to Portfolio"):
        if p_symbol:
            add_stock(p_symbol, p_qty, p_price)
            st.success(f"{p_symbol.upper()} added to portfolio!")

    st.markdown("---")

    # Portfolio Summary
    st.subheader("📊 Portfolio Summary")
    summary = get_portfolio_summary()

    if summary.empty:
        st.info("No stocks in portfolio yet. Add some above!")
    else:
        st.dataframe(summary, use_container_width=True)

        # P&L Chart
        fig = px.pie(summary, values='Current Value',
                     names='Symbol', title='Portfolio Allocation')
        st.plotly_chart(fig, use_container_width=True)

        # Remove Stock
        st.subheader("➖ Remove Stock")
        remove_symbol = st.selectbox("Select stock to remove", summary['Symbol'].tolist())
        if st.button("Remove"):
            remove_stock(remove_symbol)
            st.success(f"{remove_symbol} removed!")
            st.rerun()

# ─────────────────────────────────────────
# TAB 3 — PREDICTION
# ─────────────────────────────────────────
with tab3:
    st.header("🔮 Price Prediction")
    pred_symbol = st.text_input("Enter Stock Symbol", value="AAPL", key="pred")

    if pred_symbol:
        with st.spinner("Running ML model..."):
            try:
                df = get_historical_data(pred_symbol, period="1y")
                fig, predicted_price = predict_price(df)
                st.plotly_chart(fig, use_container_width=True)
                st.success(f"📌 Predicted price after 30 days: **${predicted_price}**")
                st.warning("⚠️ This is based on Linear Regression and is for educational purposes only. Not financial advice!")
            except Exception as e:
                st.error(f"Error: {e}")

# ─────────────────────────────────────────
# TAB 4 — NEWS & SENTIMENT
# ─────────────────────────────────────────
with tab4:
    st.header("📰 News & Sentiment")
    news_query = st.text_input("Enter Stock Name (e.g. Apple, Reliance, Tesla)", value="Apple")

    if news_query:
        with st.spinner("Fetching news..."):
            news = get_news_sentiment(news_query)
            if news:
                for item in news:
                    st.markdown(f"**{item['sentiment']}** — [{item['title']}]({item['link']})")
                    st.caption(item['published'])
                    st.markdown("---")
            else:
                st.info("No news found!")

# ─────────────────────────────────────────
# TAB 5 — AI ASSISTANT
# ─────────────────────────────────────────
with tab5:
    st.header("💬 AI Stock Assistant")
    st.write("Ask me anything about stocks, markets, or investing!")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful stock market assistant. Answer questions clearly and concisely."}
        ]

    # Display chat history
    for msg in st.session_state.messages[1:]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    # User input
    user_input = st.chat_input("Ask about any stock...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        with st.spinner("Thinking..."):
            response = chat_with_ai(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)