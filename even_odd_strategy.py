from backtest_engine import BacktestEngine
from collections import deque

class MovingAverageStrategy:
    def __init__(self, short_window=5, long_window=20, quantity=5):
        self.short_window = short_window
        self.long_window = long_window
        self.quantity = quantity

        # price history per ticker
        self.prices = {}

        # track last signal to avoid repeated buys/sells
        self.last_signal = {}

    def on_bar(self, bar):
        actions = []

        for ticker in bar:
            close_price = bar[ticker]['Close']

            # initialize storage
            if ticker not in self.prices:
                self.prices[ticker] = deque(maxlen=self.long_window)
                self.last_signal[ticker] = None

            # update price history
            self.prices[ticker].append(close_price)

            # need enough data
            if len(self.prices[ticker]) < self.long_window:
                continue

            prices = list(self.prices[ticker])

            short_ma = sum(prices[-self.short_window:]) / self.short_window
            long_ma = sum(prices) / self.long_window

            # Bullish crossover
            if short_ma > long_ma and self.last_signal[ticker] != "BUY":
                actions.append({
                    'ticker': ticker,
                    'action': "BUY",
                    'quantity': self.quantity
                })
                # self.last_signal[ticker] = "BUY"

            # Bearish crossover
            elif short_ma < long_ma and self.last_signal[ticker] != "SELL":
                actions.append({
                    'ticker': ticker,
                    'action': "SELL",
                    'quantity': self.quantity
                })
                # self.last_signal[ticker] = "SELL"

        return actions

if __name__ == "__main__":
    tickers = ["AAPL", 'NVDA', "GOOG", "RIVN", "NKE", "TSLA", "INFY", "WBD", "FOLD", "UBER", "CVX", "AMZN", "VNDA", "MSFT", "META", "JPM", "DIS"]
    strategy = MovingAverageStrategy(short_window=5, long_window=30, quantity=5)
    engine = BacktestEngine(initial_capital=50000)
    engine.run_backtest(strategy, tickers, '2025-01-01', '2022-12-31')
    engine.print_final_report()
    engine.get_portfolio().plot_cash_balance()
    engine.get_portfolio().plot_holdings()
    engine.get_portfolio().plot_total_balance()