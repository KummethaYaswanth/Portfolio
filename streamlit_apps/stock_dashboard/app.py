import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="Stock Price Dashboard",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("📈 Stock Price Dashboard")
st.markdown("*A simple dashboard to visualize stock price trends*")

# Sidebar for stock selection
st.sidebar.header("Stock Selection")
stocks = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA"]
selected_stock = st.sidebar.selectbox("Choose a stock:", stocks)

# Generate mock data
@st.cache_data
def generate_mock_data(stock_symbol, days=30):
    """Generate mock stock data for demonstration"""
    dates = [datetime.now() - timedelta(days=i) for i in range(days, 0, -1)]
    
    # Starting price based on stock
    base_prices = {"AAPL": 150, "GOOGL": 2800, "MSFT": 300, "TSLA": 200, "AMZN": 3200, "NVDA": 450}
    base_price = base_prices.get(stock_symbol, 100)
    
    prices = []
    current_price = base_price
    
    for _ in dates:
        # Random walk with slight upward bias
        change = random.uniform(-0.05, 0.07) * current_price
        current_price += change
        prices.append(round(current_price, 2))
    
    return pd.DataFrame({
        'Date': dates,
        'Price': prices,
        'Volume': [random.randint(1000000, 10000000) for _ in dates]
    })

# Generate and display data
data = generate_mock_data(selected_stock)

# Display current price
current_price = data['Price'].iloc[-1]
prev_price = data['Price'].iloc[-2]
change = current_price - prev_price
change_pct = (change / prev_price) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label=f"{selected_stock} Current Price",
        value=f"${current_price:.2f}",
        delta=f"{change_pct:.2f}%"
    )

with col2:
    st.metric(
        label="24h Change",
        value=f"${change:.2f}",
        delta=f"{change:.2f}"
    )

with col3:
    st.metric(
        label="Volume",
        value=f"{data['Volume'].iloc[-1]:,}"
    )

# Plot the stock price
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['Price'],
    mode='lines',
    name=selected_stock,
    line=dict(color='#00ff88', width=2)
))

fig.update_layout(
    title=f"{selected_stock} Price Trend (Last 30 Days)",
    xaxis_title="Date",
    yaxis_title="Price ($)",
    template="plotly_dark",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# Show data table
st.subheader("📊 Recent Data")
st.dataframe(data.tail(10), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("💡 *This is a demo app with simulated data for portfolio purposes*") 