# main.py

# This file serves as the entry point for executing the multi-agent system designed to optimize a MACD trading strategy.

from textwrap import dedent  # For formatting the multi-line task string
from autogen.cache import Cache  # For managing caching during the agent interaction
from agents import trade_strategy_optimizer, user_proxy  # Importing the agents used in the interaction
from config import company, file_path, start_date, end_date  # Importing relevant configuration variables

# Define the task for the trade_strategy_optimizer agent, specifying the objectives to be achieved.
task = dedent(f"""
    Based on {company}'s stock data from {start_date} to {end_date} in the file at {file_path}, determine the possible optimal parameters for a MACD Strategy over this period.
    First, ask the backtesting_specialist to plot a candlestick chart of the stock price data with MACD indicators to visually inspect the price movements and make an initial assessment.
    Then, ask the backtesting_specialist to backtest the MACD (short_ema, long_ema, and signal_ema) strategy parameters using the backtesting tool, and report results back for further optimization.
""")

# Execute the task using a disk cache to manage the session data.
with Cache.disk() as cache:
    user_proxy.initiate_chat(
        recipient=trade_strategy_optimizer,  # The agent that will receive and handle the task
        message=task,  # The task description provided to the agent
        max_turns=3,  # The maximum number of interactions (turns) allowed for this task
        summary_method="last_msg"  # Method for summarizing the chat at the end of the interaction
    )
