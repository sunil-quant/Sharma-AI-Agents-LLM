# data_processing.py

# This file defines a class `MACDDataProcessor` used for processing stock market data, 
# specifically for calculating the Moving Average Convergence Divergence (MACD) indicator.
# The class includes methods to filter data by date, calculate Exponential Moving Averages (EMAs),
# and compute the MACD along with its components like the signal line and histogram.

import pandas as pd  # Importing pandas for data manipulation
from config import file_path, start_date, end_date  # Importing configuration variables

class MACDDataProcessor:
    def __init__(self, csv_file_path: str):
        # Initialize the processor by loading the data from a CSV file and setting the date column as the index
        self.data = pd.read_csv(csv_file_path, parse_dates=['date'])
        self.data.set_index('date', inplace=True)

    def filter_data(self, start_date: str, end_date: str):
        # Filter the data to include only the rows between start_date and end_date
        self.filtered_data = self.data.loc[start_date:end_date]

    def calculate_ema(self, period: int):
        # Calculate the Exponential Moving Average (EMA) for the specified period
        return self.filtered_data['close'].ewm(span=period, adjust=False).mean()

    def calculate_macd(self):
        # Calculate the MACD components:
        ema_short = self.calculate_ema(12)
        ema_long = self.calculate_ema(26)
        macd = ema_short - ema_long
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        return ema_short, ema_long, macd, signal, histogram

    def get_filtered_data(self):
        # Return the filtered data as a dictionary
        return self.filtered_data.to_dict()

    def get_macd_components(self):
        # Calculate and return the MACD components as dictionaries
        ema_short, ema_long, macd, signal, histogram = self.calculate_macd()
        return {
            'ema_short': ema_short.to_dict(),
            'ema_long': ema_long.to_dict(),
            'macd': macd.to_dict(),
            'signal': signal.to_dict(),
            'histogram': histogram.to_dict()
        }

    def inspect_data(self):
        # A utility method to inspect the filtered data and the MACD components
        print("Filtered Data Info:")
        print(self.filtered_data.info())  # Show summary information of the filtered data
        ema_short, ema_long, macd, signal, histogram = self.calculate_macd()  # Calculate MACD components
        # Print the lengths of the various calculated series to ensure they are consistent
        print("EMA Short Length:", len(ema_short))
        print("EMA Long Length:", len(ema_long))
        print("MACD Length:", len(macd))
        print("Signal Length:", len(signal))
        print("Histogram Length:", len(histogram))
        # Print the first few rows of the data and MACD components for a quick check
        print("Filtered Data Head:\n", self.filtered_data.head())
        print("EMA Short Head:\n", ema_short.head())
        print("EMA Long Head:\n", ema_long.head())
        print("MACD Head:\n", macd.head())
        print("Signal Head:\n", signal.head())
        print("Histogram Head:\n", histogram.head())