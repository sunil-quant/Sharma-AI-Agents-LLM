# agents.py

from textwrap import dedent
from autogen import AssistantAgent, UserProxyAgent, register_function
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from autogen.cache import Cache
from tools import plot_macd_tool, display_image_tool, backtest_macd_tool, get_backtesting_result
from config import file_path, start_date, end_date

trade_strategy_optimizer = MultimodalConversableAgent(
    name="Trade_Strategy_Optimizer",
    system_message=dedent(
        """
        You are a trading strategy optimizer who inspects financial charts and optimizes trading strategies.
        You have been tasked with developing a Moving average convergence/divergence (MACD) trading strategy.
        You have the following main actions to take:
        1. Ask the Backtesting_Specialist to plot historical stock price data with designated MACD indicators.
        2. Inspect the stock price chart carefully and determine MACD (short_ema, long_ema, and signal_ema) parameters.
        3. Highlight the exact points/periods where the MACD line crosses the Signal line and interpret their significance critically.
        4. Provide a logical explanation for the suggested parameters based on observed trends.
        5. Ask the Backtesting_Specialist to backtest the MACD trading strategy with designated parameters to evaluate its performance.
        6. Inspect the backtest result obtained from Backtesting_Specialist and from variable {backtesting_result}, analyze key performance metrics (e.g., drawdown, returns, Sharpe ratio, trade analysis).
        7. Based on the analysis, optimize the MACD parameters iteratively until satisfactory performance is achieved or until the maximum number of iterations (max_turns) is reached.
        8. Define acceptable performance benchmarks (e.g., minimum profit factor, maximum drawdown). If the strategy meets these benchmarks at any iteration, summarize the results and terminate the optimization early.
        9. Summarize the results and provide the best parameters at the end of the optimization process.
        10. Reply TERMINATE when you think the strategy is good enough.
        """
    ),
    llm_config=llm_config_4o,
)

backtesting_specialist = AssistantAgent(
    name="Backtesting_Specialist",
    system_message=dedent(
        f"""
        You are a backtesting specialist with a strong command of quantitative analysis tools.
        You have two main tasks to perform, choose one each time you are asked by the Trade_Strategy_Optimizer:
        1. Plot historical stock price data for {company} in the file at {file_path} with MACD indicators (short_ema, long_ema, and signal_ema) according to the Trade_Strategy_Optimizer's need.
        2. Backtest the MACD trading strategy with designated parameters (short_ema, long_ema, and signal_ema) and save the results as an image file.

        For both tasks, after the tool calling, you should do as follows:
            1. Display the created and saved image file using the `display_image_tool` tool.
            2. Call the `get_backtesting_result` tool to retrieve the backtesting results,and store it in stored in the global variable `backtesting_result`.
            3. Provide a summary of the backtesting results including key metrics such as total returns, drawdown, Sharpe ratio, and trade analysis.
            4. Assume the saved image file is "test.png" and summary of backtesting results is stored in the global variable. Share both the image and `backtesting_result` ask to Optimize the MACD parameters (short_ema, long_ema, and signal_ema) based on this image <img test.png>, and based on Backtest results in the `backtesting_result` variable. TERMINATE."
        """
    ),
    llm_config=llm_config,
)

backtesting_specialist_executor = UserProxyAgent(
    name="Backtesting_Specialist_Executor",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "coding",
        "use_docker": False,
    },
)

register_function(
    plot_macd_tool,
    caller=backtesting_specialist,
    executor=backtesting_specialist_executor,
    name="plot_macd_tool",
    description="Plots the MACD chart with EMA, MACD histogram, and signals, and saves the plot to a file.",
)

register_function(
    backtest_macd_tool,
    caller=backtesting_specialist,
    executor=backtesting_specialist_executor,
    name="backtest_macd_tool",
    description="Backtests a MACD trading strategy on historical stock data from a CSV file.",
)

register_function(
    display_image_tool,
    caller=backtesting_specialist,
    executor=backtesting_specialist_executor,
    name="display_image_tool",
    description="Displays an image from the given file path using IPython.display.",
)

register_function(
    get_backtesting_result,
    caller=backtesting_specialist,
    executor=backtesting_specialist_executor,
    name="get_backtesting_result",
    description="Retrieves the backtesting results stored in the global variable."
)

def reflection_message_analyst(recipient, messages, sender, config):
    print("Reflecting Trade_Strategy_Optimizer's response ...")
    last_msg = recipient.chat_messages_for_summary(sender)[-1]["content"]
    return (
        "Message from Trade_Strategy_Optimizer is as follows:"
        + last_msg
        + "\n\nBased on this information, conduct a backtest on the specified stock and MACD strategy, and report your backtesting results back to the Trade_Strategy_Optimizer."
    )
