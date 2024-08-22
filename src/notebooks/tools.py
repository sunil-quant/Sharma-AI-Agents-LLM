# tools.py

# This file provides utility functions that wrap around the core functionalities for plotting MACD charts,
# displaying images, running backtests on historical stock data, and retrieving backtesting results.

from typing import Annotated  # For adding descriptive type annotations to function parameters
from plotting import MACDPlotter  # Importing the MACDPlotter class for creating MACD plots
from IPython.display import Image, display  # For displaying images in IPython environments 
from backtesting import BackTraderUtils  # Importing utility class for running backtests

def plot_macd_tool(
    csv_file_path: Annotated[str, "Path to CSV file containing historical stock data"],
    start_date: Annotated[str, "Start date of the historical data in 'YYYY-MM-DD' format"],
    end_date: Annotated[str, "End date of the historical data in 'YYYY-MM-DD' format"],
    save_path: Annotated[str, "File path where the plot should be saved"],
    plot_type: Annotated[str, "Type of the plot (e.g., 'candle', 'line')"] = "candle",
    plot_style: Annotated[str, "Style of the plot (e.g., 'default', 'yahoo')"] = "default",
    show_nontrading: Annotated[bool, "Whether to show non-trading days on the chart"] = False
) -> str:
    # Function to generate and save an MACD plot using the MACDPlotter class
    plotter = MACDPlotter(csv_file_path)
    return plotter.plot_macd(start_date, end_date, save_path, plot_type, plot_style, show_nontrading)

def display_image_tool(file_path: Annotated[str, "Path to the image file to be displayed"]):
    # Function to display an image from a specified file path
    try:
        display(Image(filename=file_path))
        return f"Displayed image from {file_path}"
    except Exception as e:
        # Handle errors that may occur during image display
        return f"Failed to display image from {file_path}: {e}"

def backtest_macd_tool(
    csv_file_path: Annotated[str, "Path to CSV file containing historical stock data"],
    start_date: Annotated[str, "Start date of the backtest in 'YYYY-MM-DD' format"],
    end_date: Annotated[str, "End date of the backtest in 'YYYY-MM-DD' format"],
    strategy_params: Annotated[str, "JSON string of strategy parameters, e.g., '{\"short_ema\": 12, \"long_ema\": 26, \"signal_ema\": 9}'"] = "",
    cash: Annotated[float, "Initial cash for backtesting"] = 10000.0,
    save_fig: Optional[Annotated[str, "File path to save the backtest result plot"]] = None,
) -> str:
    # Function to run a backtest on historical stock data using the MACD strategy
    utils = BackTraderUtils()
    return utils.back_test_macd(csv_file_path, start_date, end_date, strategy_params, cash, save_fig)

def get_backtesting_result():
    # Function to retrieve the most recent backtesting results
    global backtesting_result  # Refers to the backtesting result stored globally
    if backtesting_result is None:
        # Return an error message if no backtesting results are available
        return {"error": "No backtesting results available."}
    return backtesting_result
