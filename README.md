# Sharma-AI-Agents-LLM

This project explores AI agents with LLMs to develop investment/trading strategies. 

## Project Structure

- **config.py**: Contains configuration settings, including the company's stock data file path, date range, and language model configurations.
- **data_processing.py**: Defines the `MACDDataProcessor` class for processing stock data, filtering it by date, and calculating MACD indicators.
- **plotting.py**: Contains the `MACDPlotter` class to generate and save MACD plots with candlestick charts, EMAs, and histogram.
- **backtesting.py**: Defines the `MACDStrategy` class and the `BackTraderUtils` utility class for backtesting the MACD strategy using the Backtrader library.
- **tools.py**: Provides utility functions (`plot_macd_tool`, `display_image_tool`, `backtest_macd_tool`, `get_backtesting_result`) to interact with the plotting and backtesting functionalities.
- **agents.py**: Configures agents responsible for optimizing the MACD strategy (`Trade_Strategy_Optimizer`) and handling backtesting tasks (`Backtesting_Specialist`).
- **main.py**: The entry point of the project. It initializes the agents and triggers the process of optimizing the MACD trading strategy.
- **requirements.txt**: Lists the Python dependencies required to run the project.
- **CONFIG.json**: Contains configuration settings for various LLM models used in the project.
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

    python -m pip check

## Jupyter Notebooks

- **autogen_agent_macd_notebook.ipynb**: Walks through the MACD trading strategy optimization using the multi-agent system. Note: You need to add your OpenAI API key to the CONFIG.json file for it to work correctly.
- **analysis_vision_models_macd_notebook.ipynb**: Analyzes and observes different LLM vision models (e.g., GPT-4v, LLava) in their ability to interpret the Moving Average Convergence Divergence (MACD) indicator.
- **backtest_macd_notebook.ipynb**: Tests the backtesting capability of the MACD trading strategy using historical stock data for YESBANK with the Backtrader framework.

## Launch the Notebook

The notebook has been tested on Binder. However, please note that the Binder link is temporary. To ensure continuous access, you may need to add the GitHub repository URL to Binder or run the notebook locally.

Launch the Notebook
To use Binder with this notebook, follow these steps:

- Go to Binder(https://mybinder.org/).
- Enter the GitHub URL of this repository: https://github.com/sunil-quant/Sharma-AI-Agents-LLM.
- Specify Git ref (branch, tag, or commit) as 'main'
- Click on "Launch" to open the notebook.

Current link for Interactive version of the Jupyter notebook using Binder():
[![Binder](https://mybinder.org/badge_logo.svg)](https://hub.binder.curvenote.dev/user/sunil-quant-sharma-ai-agents-llm-rr4hyr09/lab/workspaces/auto-W/tree/src/notebooks/autogen_agent_macd_notebook.ipynb)

Note: You will need to add your OpenAI API key to the CONFIG.json file for the notebook to work correctly.