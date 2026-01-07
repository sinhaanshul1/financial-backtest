import yfinance
import matplotlib.pyplot as plt
import pandas as pd


class Portfolio():
    def __init__(self, positions=None, cash=0, tickers=[]):
        self.positions = positions if positions is not None else {}
        self.cash = cash
        self._timestamps = []
        self._total_balance = []
        self._cash_history = []
        self._positions_history = {}
        self.last_price = {}
        for ticker in tickers:
            self._positions_history[ticker] = []
            self.last_price[ticker] = 0
            self.positions[ticker] = 0
        
    
    def update_positions(self, orders, tickers_ohlcv, time):
        for order in orders:
            ticker = order['ticker']
            quantity = order['quantity']
            price = tickers_ohlcv[ticker]['Close']
            self.last_price[ticker] = price
            if order['action'] == 'SELL':
                quantity *= -1
            if self.cash - quantity * price < 0:
                print(quantity)
                print("Not enough cash to execute the trade.")
                continue
            if self.positions.get(ticker, 0) + quantity < 0:
                print("Not enough shares to sell.")
                continue
            if ticker in self.positions:
                self.positions[ticker] += quantity
            else:
                self.positions[ticker] = quantity
            self.cash -= quantity * price
        print("TIME: ", time)
        self._timestamps.append(pd.Timestamp(time))
        self._cash_history.append(self.cash)
        total_balance = self.cash
        for ticker in self.last_price:
            total_balance += self.positions[ticker] * self.last_price[ticker]
        self._total_balance.append(total_balance)
        for ticker in self._positions_history:
            if ticker in self.positions:
                self._positions_history[ticker].append(self.positions[ticker])
            else:
                self._positions_history[ticker].append(0)

    def get_cash(self):
        return self.cash
    
    def get_positions(self):
        return self.positions
    
    def plot_portfolio(self):

        print(self._timestamps[:5])
        print(self._total_balance[:5])
        print(self._cash_history[:5])
        print(self._positions_history[:5])
        plt.figure(figsize=(12, 6))
        plt.xlim(self._timestamps[0], self._timestamps[-1])
        plt.ylim(9000, 10500)
        plt.plot(self._timestamps, self._total_balance, label="Total Portfolio Value")
        plt.plot(self._timestamps, self._cash_history, label="Cash Balance")
        plt.plot(self._timestamps, self._positions_history, label="Positions Value")

        plt.title("Backtest Performance")
        plt.xlabel("Time")
        plt.ylabel("Value ($)")
        plt.legend()
        plt.grid(True)

        plt.show()

    
    def plot_total_balance(self):
        plt.figure("Total", figsize=(12, 6))
        plt.xlim(self._timestamps[0], self._timestamps[-1])
        plt.ylim(min(self._total_balance)  - 100, max(self._total_balance) + 100)
        plt.plot(self._timestamps, self._total_balance, label="Total Portfolio Value")
        plt.title("Total Portfolio Performance")
        plt.xlabel("Time")
        plt.ylabel("Value ($)")
        plt.grid(True)
        plt.draw()
        plt.show()

    def plot_cash_balance(self):
        plt.figure("Cash", figsize=(12, 6))
        plt.xlim(self._timestamps[0], self._timestamps[-1])
        plt.ylim(min(self._cash_history)  - 100, max(self._cash_history) + 100)
        plt.plot(self._timestamps, self._cash_history, label="Cash Balance Value")
        plt.title("Cash Balance Performance")
        plt.xlabel("Time")
        plt.ylabel("Value ($)")
        plt.grid(True)
        plt.draw()

    def plot_holdings(self):
        plt.figure("Holdings", figsize=(12, 6))
        
        max_holdings = 0
        for ticker in self._positions_history:
            if max(self._positions_history[ticker]) > max_holdings:
                max_holdings = max(self._positions_history[ticker])
            plt.plot(self._timestamps, self._positions_history[ticker], label=ticker)
        plt.xlim(self._timestamps[0], self._timestamps[-1])
        plt.ylim(0, max_holdings + 5)
        plt.title("Positions Performance")
        plt.xlabel("Time")
        plt.ylabel("Quantity")
        plt.grid(True)
        plt.legend()
        plt.draw()
        
    
    


class BacktestEngine():
    def __init__(self, initial_capital=0):
        self.capital = initial_capital
        
        self._last_close_price = {}

    def run_backtest(self, strategy, tickers: list[str], start_date: str, end_date: str):
        self.portfolio = Portfolio(cash=self.capital, tickers=tickers)
        print("Downloading data...")
        # data = yfinance.download(ticker, interval="1m", start=start_date, end=end_date)
        data = yfinance.download(tickers, interval="1d", start="2023-01-05", end="2025-01-05", auto_adjust=True)
        print(f'Downloaded {len(data)} rows of data  from {start_date} to {end_date}')
        print("Starting backtest...")
        for index, row in data.iterrows():
            print(index)
            tickers_ohlcv = {}
            for ticker in tickers:
                ohlcv = {
                    'Open': row[('Open', ticker)],
                    'High': row[('High', ticker)],
                    'Low': row[('Low', ticker)],
                    'Close': row[('Close', ticker)],
                    'Volume': row[('Volume', ticker)],
                }
                tickers_ohlcv[ticker] = ohlcv
                self._last_close_price[ticker] = ohlcv['Close']
            orders = strategy.on_bar(tickers_ohlcv)
            print("INDEX: ", index)
            self.portfolio.update_positions(orders, tickers_ohlcv, index)

        print("Backtest completed.")

    def get_portfolio(self):
        return self.portfolio

    def print_final_report(self):
        print("\n===========")
        print("Final Portfolio Report: ")
        print("Inital Capital: ", self.capital)
        print("Positions: ")
        total_invested = 0
        for ticker, quantity in self.portfolio.get_positions().items():
            total_invested += quantity * self._last_close_price[ticker]
            print(f"  - {quantity} shares of {ticker} @ {self._last_close_price[ticker]} -> {quantity * self._last_close_price[ticker]}")
        print("Cash remaining: ", self.portfolio.get_cash())
        print(f"Total Portfolio Value: {self.portfolio.get_cash() + total_invested}")

        print("\nDelta: ", (self.portfolio.get_cash() + total_invested) - self.capital)


if __name__ == "__main__":
    data = yfinance.download("AAPL", interval="1m", start="2025-11-15", end="2025-11-22")
    engine = BacktestEngine(data, 10000)
    engine.run_backtest(None)
