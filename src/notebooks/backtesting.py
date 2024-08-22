# backtesting.py

# This file defines classes and functions for performing backtesting on historical stock data using the 
# Moving Average Convergence Divergence (MACD) strategy. It utilizes the Backtrader library to simulate
# trading strategies and analyze their performance.

import backtrader as bt  # Backtrader is used for backtesting trading strategies
import pandas as pd  # For data manipulation
import json  # For handling JSON data, particularly for strategy parameters
import os  # For file and directory operations
import matplotlib.pyplot as plt  # For plotting backtesting results
from typing import Optional, Dict, Annotated  # For type annotations and optional parameters
from config import backtesting_result, file_path, start_date, end_date  # Import configuration variables

class MACDStrategy(bt.Strategy):
    # Define a basic MACD trading strategy using Backtrader's strategy class
    params = (('short_ema', 12), ('long_ema', 26), ('signal_ema', 9),)

    def __init__(self):
        # Initialize the MACD indicator and a crossover indicator for buy/sell signals
        self.macd = bt.indicators.MACD(
            self.data.close,
            period_me1=self.params.short_ema,
            period_me2=self.params.long_ema,
            period_signal=self.params.signal_ema
        )
        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

    def next(self):
        # Implement the trading logic: Buy on MACD crossover above the signal line, sell on crossover below
        if self.crossover > 0:
            self.buy()
        elif self.crossover < 0:
            self.sell()

class BackTraderUtils:
    # Utility class for running the backtest with the MACD strategy
    def back_test_macd(
        self,
        csv_file_path: Annotated[str, "Path to CSV file containing historical stock data"],
        start_date: Annotated[str, "Start date of the backtest in 'YYYY-MM-DD' format"],
        end_date: Annotated[str, "End date of the backtest in 'YYYY-MM-DD' format"],
        strategy_params: Annotated[str, "JSON string of strategy parameters, e.g., '{\"short_ema\": 12, \"long_ema\": 26, \"signal_ema\": 9}'"] = "",
        cash: Annotated[float, "Initial cash for backtesting"] = 10000.0,
        save_fig: Optional[Annotated[str, "File path to save the backtest result plot"]] = None,
    ) -> str:
        """
        Use the Backtrader library to backtest the MACD strategy on historical stock data from a CSV file.
        """

        # Initialize the Backtrader engine
        cerebro = bt.Cerebro()
        strategy_class = MACDStrategy

        # Load strategy parameters from the provided JSON string
        try:
            strategy_params_dict = json.loads(strategy_params) if strategy_params else {}
        except json.JSONDecodeError:
            return "Error: Invalid JSON format for strategy_params."

        cerebro.addstrategy(strategy_class, **strategy_params_dict)

        # Load historical stock data from CSV file
        try:
            df = pd.read_csv(csv_file_path, parse_dates=['date'])
        except FileNotFoundError:
            return f"Error: File not found at {csv_file_path}."
        except pd.errors.ParserError:
            return "Error: Failed to parse CSV file."

        # Prepare the data for Backtrader
        df['datetime'] = pd.to_datetime(df['date'])
        df.set_index('datetime', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']]

        # Filter data within the specified date range
        df = df.loc[start_date:end_date]

        # Ensure there's enough data for the specified MACD periods
        if len(df) < max(strategy_params_dict.get('short_ema', 12), strategy_params_dict.get('long_ema', 26), strategy_params_dict.get('signal_ema', 9)):
            return "Error: Not enough data available for the specified date range to calculate MACD."

        if df.empty:
            return "Error: No data available for the specified date range."

        # Rename columns to match Backtrader's expected format
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

        # Create a Backtrader data feed from the dataframe
        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data)

        # Set initial cash for the backtest
        cerebro.broker.setcash(cash)

        # Add analyzers to evaluate strategy performance
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe_ratio")
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="draw_down")
        cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trade_analyzer")

        # Initialize a dictionary to store backtesting results
        stats_dict: Dict[str, any] = {"Starting Portfolio Value": cerebro.broker.getvalue()}

        # Run the backtest
        results = cerebro.run()
        first_strategy = results[0]

        # Capture the results in the dictionary
        stats_dict["Final Portfolio Value"] = cerebro.broker.getvalue()
        stats_dict["Sharpe Ratio"] = first_strategy.analyzers.sharpe_ratio.get_analysis()
        stats_dict["Drawdown"] = first_strategy.analyzers.draw_down.get_analysis()
        stats_dict["Returns"] = first_strategy.analyzers.returns.get_analysis()
        stats_dict["Trade Analysis"] = first_strategy.analyzers.trade_analyzer.get_analysis()

        # Save a plot of the backtest results if a file path is provided
        if save_fig:
            directory = os.path.dirname(save_fig)
            if directory:
                os.makedirs(directory, exist_ok=True)
            plt.figure(figsize=(16, 10))
            cerebro.plot()
            plt.savefig(save_fig)
            plt.close()

        # Store the results in the global backtesting_result variable
        backtesting_result = stats_dict

        # Return the backtesting results as a formatted JSON string
        return "Back Test Finished. Results: \n" + json.dumps(stats_dict, indent=2)