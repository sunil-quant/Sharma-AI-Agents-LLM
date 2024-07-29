# main.py

from textwrap import dedent
from autogen.cache import Cache
from agents import trade_strategy_optimizer, user_proxy
from config import company, file_path, start_date, end_date

task = dedent(f"""
    Based on {company}'s stock data from {start_date} to {end_date} in the file at {file_path}, determine the possible optimal parameters for a MACD Strategy over this period.
    First, ask the backtesting_specialist to plot a candlestick chart of the stock price data with MACD indicators to visually carefully inspect the price movements and make an initial assessment.
    Then, ask the backtesting_specialist to backtest the MACD (short_ema,long_ema and signal_ema) strategy parameters using the backtesting tool, and report results back for further optimization.
""")

with Cache.disk() as cache:
    user_proxy.initiate_chat(
        recipient=trade_strategy_optimizer, message=task, max_turns=3, summary_method="last_msg"
    )
