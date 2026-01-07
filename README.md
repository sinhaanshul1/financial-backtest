# Algorithmic Trading Backtest Engine

A flexible Python backtesting framework for algorithmic trading strategies with real-time portfolio tracking, performance visualization, and multi-asset support.

## Overview

This project provides a modular backtesting engine that allows you to:
- Test trading strategies against historical market data
- Track portfolio performance across multiple assets simultaneously
- Visualize cash balance, holdings, and total portfolio value over time
- Easily implement and compare different trading strategies

Currently implements a **Moving Average Crossover Strategy** with plans to add more strategies.

## Features

### Backtest Engine
- **Multi-asset support**: Test strategies across multiple tickers simultaneously
- **Real-time portfolio tracking**: Monitors cash, positions, and total value at each time step
- **Historical data integration**: Uses `yfinance` to pull real market data
- **Flexible timeframes**: Supports daily, hourly, or minute-level data
- **Transaction validation**: Prevents invalid trades (insufficient cash/shares)
- **Performance reporting**: Detailed final portfolio breakdown with P&L

### Moving Average Crossover Strategy
- **Dual moving average system**: Configurable short and long windows
- **Per-ticker logic**: Independently tracks signals for each asset
- **Bullish crossover**: Buys when short MA crosses above long MA
- **Bearish crossover**: Sells when short MA crosses below long MA
- **Signal tracking**: Avoids redundant trades in same direction

### Visualization
Three built-in plotting functions:
- **Total portfolio value**: Overall account performance over time
- **Cash balance**: Available cash throughout backtest
- **Individual holdings**: Quantity of each asset held over time

## Technical Stack

- **Data Source**: `yfinance` (Yahoo Finance API)
- **Data Processing**: `pandas`
- **Visualization**: `matplotlib`
- **Data Structures**: Python `deque` for efficient rolling windows

## Installation

```bash
pip install yfinance pandas matplotlib
```

## Usage

### Running a Backtest

```python
from backtest_engine import BacktestEngine
from moving_average_strategy import MovingAverageStrategy

# Define tickers to trade
tickers = ["AAPL", "NVDA", "GOOG", "TSLA", "AMZN"]

# Initialize strategy (5-day vs 30-day MA crossover)
strategy = MovingAverageStrategy(
    short_window=5, 
    long_window=30, 
    quantity=5
)

# Create backtest engine with initial capital
engine = BacktestEngine(initial_capital=50000)

# Run backtest
engine.run_backtest(
    strategy=strategy,
    tickers=tickers,
    start_date='2023-01-05',
    end_date='2025-01-05'
)

# View results
engine.print_final_report()
engine.get_portfolio().plot_total_balance()
engine.get_portfolio().plot_cash_balance()
engine.get_portfolio().plot_holdings()
```

### Creating Custom Strategies

The framework is designed for easy strategy implementation. Any strategy class must implement an `on_bar()` method:

```python
class CustomStrategy:
    def __init__(self, param1, param2):
        # Initialize strategy parameters
        pass
    
    def on_bar(self, bar):
        """
        Called for each time step in the backtest.
        
        Args:
            bar: Dict of {ticker: {'Open', 'High', 'Low', 'Close', 'Volume'}}
        
        Returns:
            List of order dicts: [
                {'ticker': 'AAPL', 'action': 'BUY', 'quantity': 10},
                {'ticker': 'TSLA', 'action': 'SELL', 'quantity': 5}
            ]
        """
        actions = []
        # Your strategy logic here
        return actions
```

### Example Output

```
===========
Final Portfolio Report: 
Initial Capital: 50000
Positions: 
  - 25 shares of AAPL @ 195.32 -> 4883.00
  - 15 shares of NVDA @ 142.18 -> 2132.70
  - 10 shares of GOOG @ 168.45 -> 1684.50
Cash remaining: 38245.80
Total Portfolio Value: 46946.00

Delta: -3054.00
```

## Architecture

### BacktestEngine
The core engine that:
- Downloads historical data via `yfinance`
- Iterates through time steps (bars)
- Calls strategy's `on_bar()` for each bar
- Validates and executes orders
- Tracks portfolio state

### Portfolio
Manages the trading account:
- Maintains cash balance and positions
- Validates trade feasibility (sufficient cash/shares)
- Records historical snapshots for visualization
- Calculates total portfolio value

### Strategy (Pluggable)
User-defined logic that:
- Receives market data for each time step
- Generates trading signals (BUY/SELL orders)
- Maintains internal state (indicators, signals, etc.)

## Current Strategy: Moving Average Crossover

**Logic:**
1. Maintains short-term (default: 5-day) and long-term (default: 30-day) moving averages
2. **Buy Signal**: Short MA crosses above long MA (bullish momentum)
3. **Sell Signal**: Short MA crosses below long MA (bearish momentum)

**Parameters:**
- `short_window`: Number of periods for short moving average
- `long_window`: Number of periods for long moving average
- `quantity`: Number of shares to trade per signal

**Example Configuration:**
```python
# Conservative: slower signals, fewer trades
strategy = MovingAverageStrategy(short_window=20, long_window=50, quantity=10)

# Aggressive: faster signals, more trades
strategy = MovingAverageStrategy(short_window=5, long_window=15, quantity=5)
```

## Planned Enhancements

### Additional Strategies
- [ ] Mean Reversion (Bollinger Bands, RSI)
- [ ] Momentum (MACD, Rate of Change)
- [ ] Volume-based (OBV, Volume Profile)
- [ ] Machine Learning (predictive models, reinforcement learning)

### Engine Features
- [ ] Transaction costs and slippage modeling
- [ ] Shorting support
- [ ] Position sizing algorithms (Kelly Criterion, risk parity)
- [ ] Stop-loss and take-profit orders
- [ ] Walk-forward optimization
- [ ] Strategy comparison framework
- [ ] Risk metrics (Sharpe ratio, max drawdown, win rate)
- [ ] Export results to CSV/JSON

### Visualization
- [ ] Candlestick charts with signal overlays
- [ ] Drawdown charts
- [ ] Trade markers on price charts
- [ ] Strategy performance heatmaps

## Limitations & Considerations

- **No transaction costs**: Current version assumes zero fees/slippage
- **No shorting**: Can only hold long positions
- **Simplified fills**: Assumes all orders fill at close price
- **Look-ahead bias risk**: Be careful not to use future data in strategy logic
- **Survivorship bias**: Uses current ticker universe (doesn't account for delistings)

## Data Source

Market data is sourced from Yahoo Finance via the `yfinance` library. Data quality and availability depends on Yahoo Finance's API.

## License

MIT License

## Author

Anshul Sinha

---

*Disclaimer: This is for educational and research purposes only. Past performance does not guarantee future results. Do not use for actual trading without proper risk management and testing.*