# backtesting.py

import backtrader as bt
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from typing import Optional, Dict, Annotated
from config import backtesting_result, file_path, start_date, end_date

class MACDStrategy(bt.Strategy):
    params = (('short_ema', 12), ('long_ema', 26), ('signal_ema', 9),)

    def __init__(self):
        self.macd = bt.indicators.MACD(
            self.data.close,
            period_me1=self.params.short_ema,
            period_me2=self.params.long_ema,
            period_signal=self.params.signal_ema
        )
        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

    def next(self):
        if self.crossover > 0:
            self.buy()
        elif self.crossover < 0:
            self.sell()

class BackTraderUtils:
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
        cerebro = bt.Cerebro()
        strategy_class = MACDStrategy
        try:
            strategy_params_dict = json.loads(strategy_params) if strategy_params else {}
        except json.JSONDecodeError:
            return "Error: Invalid JSON format for strategy_params."

        cerebro.addstrategy(strategy_class, **strategy_params_dict)

        try:
            df = pd.read_csv(csv_file_path, parse_dates=['date'])
        except FileNotFoundError:
            return f"Error: File not found at {csv_file_path}."
        except pd.errors.ParserError:
            return "Error: Failed to parse CSV file."

        df['datetime'] = pd.to_datetime(df['date'])
        df.set_index('datetime', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']]

        df = df.loc[start_date:end_date]

        if len(df) < max(strategy_params_dict.get('short_ema', 12), strategy_params_dict.get('long_ema', 26), strategy_params_dict.get('signal_ema', 9)):
            return "Error: Not enough data available for the specified date range to calculate MACD."

        if df.empty:
            return "Error: No data available for the specified date range."

        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data)

        cerebro.broker.setcash(cash)

        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe_ratio")
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="draw_down")
        cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trade_analyzer")

        stats_dict: Dict[str, any] = {"Starting Portfolio Value": cerebro.broker.getvalue()}

        results = cerebro.run()
        first_strategy = results[0]

        stats_dict["Final Portfolio Value"] = cerebro.broker.getvalue()
        stats_dict["Sharpe Ratio"] = (
            first_strategy.analyzers.sharpe_ratio.get_analysis()
        )
        stats_dict["Drawdown"] = first_strategy.analyzers.draw_down.get_analysis()
        stats_dict["Returns"] = first_strategy.analyzers.returns.get_analysis()
        stats_dict["Trade Analysis"] = (
            first_strategy.analyzers.trade_analyzer.get_analysis()
        )

        if save_fig:
            directory = os.path.dirname(save_fig)
            if directory:
                os.makedirs(directory, exist_ok=True)
            plt.figure(figsize=(16, 10))
            cerebro.plot()
            plt.savefig(save_fig)
            plt.close()

        backtesting_result = stats_dict

        return "Back Test Finished. Results: \n" + json.dumps(stats_dict, indent=2)
