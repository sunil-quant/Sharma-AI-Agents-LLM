# tools.py

from typing import Annotated
from plotting import MACDPlotter
from IPython.display import Image, display
from backtesting import BackTraderUtils

def plot_macd_tool(
    csv_file_path: Annotated[str, "Path to CSV file containing historical stock data"],
    start_date: Annotated[str, "Start date of the historical data in 'YYYY-MM-DD' format"],
    end_date: Annotated[str, "End date of the historical data in 'YYYY-MM-DD' format"],
    save_path: Annotated[str, "File path where the plot should be saved"],
    plot_type: Annotated[str, "Type of the plot (e.g., 'candle', 'line')"] = "candle",
    plot_style: Annotated[str, "Style of the plot (e.g., 'default', 'yahoo')"] = "default",
    show_nontrading: Annotated[bool, "Whether to show non-trading days on the chart"] = False
) -> str:
    plotter = MACDPlotter(csv_file_path)
    return plotter.plot_macd(start_date, end_date, save_path, plot_type, plot_style, show_nontrading)

def display_image_tool(file_path: Annotated[str, "Path to the image file to be displayed"]):
    try:
        display(Image(filename=file_path))
        return f"Displayed image from {file_path}"
    except Exception as e:
        return f"Failed to display image from {file_path}: {e}"

def backtest_macd_tool(
    csv_file_path: Annotated[str, "Path to CSV file containing historical stock data"],
    start_date: Annotated[str, "Start date of the backtest in 'YYYY-MM-DD' format"],
    end_date: Annotated[str, "End date of the backtest in 'YYYY-MM-DD' format"],
    strategy_params: Annotated[str, "JSON string of strategy parameters, e.g., '{\"short_ema\": 12, \"long_ema\": 26, \"signal_ema\": 9}'"] = "",
    cash: Annotated[float, "Initial cash for backtesting"] = 10000.0,
    save_fig: Optional[Annotated[str, "File path to save the backtest result plot"]] = None,
) -> str:
    utils = BackTraderUtils()
    return utils.back_test_macd(csv_file_path, start_date, end_date, strategy_params, cash, save_fig)

def get_backtesting_result():
    global backtesting_result
    if backtesting_result is None:
        return {"error": "No backtesting results available."}
    return backtesting_result
