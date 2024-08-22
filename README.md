# Sharma-AI-Agents-LLM

This project explores AI agents with LLMs to develop investment/trading strategies. 

## Project Structure

- **config.py**: Contains configuration settings, including the company's stock data file path, date range, and language model configurations.
- **data_processing.py**: Defines the `MACDDataProcessor` class for processing stock data, filtering it by date, and calculating MACD indicators.
- **plotting.py**: Contains the `MACDPlotter` class to generate and save MACD plots with candlestick charts, EMAs, and histogram.
- **backtesting.py**: Defines the `MACDStrategy` class and the `BackTraderUtils` utility class for backtesting the MACD strategy using the Backtrader library.
- **tools.py**: Provides utility functions (`plot_macd_tool`, `display_image_tool`, `backtest_macd_tool`, `get_backtesting_result`) to interact with the plotting and backtesting functionalities.
- **agents.py**: Configures agents responsible for optimizing the MACD strategy (`Trade_Strategy_Optimizer`) and handling backtesting tasks(`Backtesting_Specialist`).
- **main.py**: The entry point of the project. It initializes the agents and triggers the process of optimizing the MACD trading strategy.
- **requirements.txt**: Lists the Python dependencies required to run the project.
- **README.md**: This file, providing an overview and instructions for the project.

## Setup

### Prerequisites

- Python 3.8 or later
- pip (Python package installer)
- git (for version control)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/sunil-quant/Sharma-AI-Agents-LLM.git
   cd Sharma-AI-Agents-LLM

2. **Install the required Python packages**:

    ```bash
    pip install -r requirements.txt

3. **Verify the installation**:

Ensure all the necessary packages are installed by running:
    ```bash
    python -m pip check