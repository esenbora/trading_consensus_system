import random

class DataFeed:
    def get_market_data(self, ticker):
        """
        Fetches market data for a given ticker.
        Mock implementation.
        """
        # Simulate API call latency or failure if needed
        base_price = random.uniform(100, 50000) if ticker == "BTC-USD" else random.uniform(10, 200)
        return {
            "ticker": ticker,
            "price": round(base_price, 2),
            "volume": random.randint(100000, 10000000),
            "change_24h": round(random.uniform(-5.0, 5.0), 2),
            "rsi": round(random.uniform(30, 70), 2)
        }

    def get_news(self, ticker):
        """
        Fetches recent news for a given ticker.
        Mock implementation.
        """
        headlines = [
            f"{ticker} shows strong momentum.",
            f"Analysts are skeptical about {ticker}'s recent rally.",
            f"New regulation could impact {ticker}.",
            f"Institutional interest in {ticker} is growing."
        ]
        return random.sample(headlines, 2)
