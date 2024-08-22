# config.py
# This configuration file sets up the environment and necessary configurations for running backtesting and trading analysis. 

# Agent-related imports
import autogen
from autogen import AssistantAgent, UserProxyAgent, register_function
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from autogen.cache import Cache

# Data manipulation and handling
import pandas as pd

# Plotting and visualization
import matplotlib.pyplot as plt
import mplfinance as mpf
from IPython.display import Image, display

# Backtesting and trading analysis
import backtrader as bt

# Standard library imports
import json
import os
from textwrap import dedent
from typing import Optional, Dict, Annotated

# Configuration for backtesting
company = "AAKASH"  # The company for which financial data will be analyzed
start_date = "2022-01-01"  # Start date for the backtest
end_date = "2024-01-01"  # End date for the backtest
file_path = f'../../data/DailyData/{company}.csv'  # Path to the data file

# Global variable to store backtesting results
backtesting_result = None

# Function to load specific configurations from a JSON file
def load_config(filter_model: str):
    return autogen.config_list_from_json(
        "./CONFIG.json",  # Path to the configuration file
        filter_dict={"model": [filter_model]},  # Filter configurations based on the specified model
    )

# Load configurations for the 'gpt-4o' model
config_list_4o = load_config("gpt-4o")
config_list = load_config("gpt-4o")  

# Language model configuration settings
llm_config_4o = {"config_list": config_list_4o, "max_tokens": 300, "temperature": 0.0}  # Specific to 'gpt-4o'
llm_config = {"config_list": config_list, "max_tokens": 300, "temperature": 0.0}  # General settings