"""
Investment Research Agent - Streamlit Version
Features:
- Enter a stock symbol (e.g., AAPL)
- Fetch stock data from Yahoo Finance
- Fetch news using NewsAPI
- Plot price trend and volume
- Display a summarized report
- API keys are loaded from .env
"""

import os
import yfinance as yf
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from dotenv import load_dotenv

# -----------------------
# Load .env variables
# -----------------------
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path, encoding='utf-8')

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # placeholder if you want LLM integration later

if not NEWS_API_KEY:
    st.warning("NEWS_API_KEY is not loaded from .env. News analysis will be skipped.")

# -----------------------
# Helper functions
# -----------------------

def fetch_stock_data(ticker):
    """Fetch last 6 months stock data using yfinance"""
    try:
        data = yf.download(ticker, period="6mo", auto_adjust=True)
        if data.empty:
            st.error("No stock data found for this ticker.")
            return None
        return data
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return None

def fetch_news(ticker, api_key, limit=5):
    """Fetch latest news for the company using NewsAPI"""
    if not api_key:
        return []

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={ticker}&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"pageSize={limit}&"
        f"apiKey={api_key}"
    )
    try:
        response = requests.get(url)
        if response.status_code != 200:
            st.warning(f"NewsAPI returned status {response.status_code}")
            return []
        articles = response.json().get("articles", [])
        news_list = [f"{art['title']} ({art['source']['name']})" for art in articles]
        return news_list
    except Exception as e:
        st.warning(f"Failed to fetch news: {e}")
        return []

def plot_stock_data(data, ticker):
    """Plot closing price and volume safely"""
    st.subheader(f"{ticker} Price & Volume Trends (Last 6 Months)")

    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Closing price (line)
    sns.lineplot(x=data.index, y=data['Close'].values.flatten(), ax=ax[0])
    ax[0].set_ylabel("Closing Price")
    ax[0].set_title(f"{ticker} Closing Price")

    # Volume (bar)
    ax[1].bar(data.index, data['Volume'].values.flatten(), color='orange')
    ax[1].set_ylabel("Volume")
    ax[1].set_title(f"{ticker} Volume")

    # Rotate x-axis labels
    plt.setp(ax[1].xaxis.get_majorticklabels(), rotation=45)
    plt.tight_layout()
    st.pyplot(fig)


def generate_report(ticker, data, news):
    report = {}
    if data is not None and not data.empty:
        # Ensure scalar float
        report["last_close"] = float(data['Close'].iloc[-1])
        report["highest"] = float(data['Close'].max())
        report["lowest"] = float(data['Close'].min())
    report["news"] = news
    return report



# -----------------------
# Streamlit UI
# -----------------------

def main():
    st.title("📈 Investment Research Agent")
    st.write("Powered by Agentic AI concepts (multi-agent inspired)")

    # Stock ticker input
    ticker = st.text_input("Enter Stock Symbol", value="AAPL").upper()

    if st.button("Run Analysis") and ticker:
        # Step 1: Fetch stock data
        st.info(f"Fetching stock data for {ticker}...")
        stock_data = fetch_stock_data(ticker)
        
        # Step 2: Fetch news
        st.info(f"Fetching latest news for {ticker}...")
        news_list = fetch_news(ticker, NEWS_API_KEY)
        
        # Step 3: Plot stock charts
        if stock_data is not None:
            plot_stock_data(stock_data, ticker)

        # Step 4: Generate report
        report = generate_report(ticker, stock_data, news_list)

        st.subheader("📊 Market Analysis Report")
        if stock_data is not None:
            st.write(f"Last Closing Price: ${report['last_close']:.2f}")
            st.write(f"Highest Price (6mo): ${report['highest']:.2f}")
            st.write(f"Lowest Price (6mo): ${report['lowest']:.2f}")

        st.subheader("📰 Latest News")
        if news_list:
            for i, item in enumerate(news_list, start=1):
                st.write(f"{i}. {item}")
        else:
            st.write("No news found or API key missing.")

if __name__ == "__main__":
    main()
