# config.py

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

company = "AAKASH"
start_date = "2022-01-01"
end_date = "2024-01-01"
file_path = f'../../data/DailyData/{company}.csv'
# Global variable to store the backtesting results
backtesting_result = None

def load_config(filter_model: str):
    return autogen.config_list_from_json(
        "./CONFIG.json",
        filter_dict={"model": [filter_model]},
    )

config_list_4o = load_config("gpt-4o")
config_list = load_config("gpt-4o")

llm_config_4o = {"config_list": config_list_4o, "max_tokens": 300, "temperature": 0.0}
llm_config = {"config_list": config_list, "max_tokens": 300, "temperature": 0.0}
